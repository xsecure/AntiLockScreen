 #!/usr/bin/env python3
#-*- coding=utf-8 -*-

import os
import time
import threading
import win32con
import win32gui
import win32ts
from pynput import keyboard, mouse

class WTSMonitor(object):
    WTS_CONSOLE_CONNECT = 0x1
    WTS_CONSOLE_DISCONNECT = 0x2
    WTS_REMOTE_CONNECT = 0x3
    WTS_REMOTE_DISCONNECT = 0x4
    WTS_SESSION_LOGON = 0x5
    WTS_SESSION_LOGOFF = 0x6
    WTS_SESSION_LOCK = 0x7
    WTS_SESSION_UNLOCK = 0x8
    WTS_SESSION_REMOTE_CONTROL = 0x9
    WTS_SESSION_CREATE = 0xA
    WTS_SESSION_TERMINATE = 0xB

    WM_WTSSESSION_CHANGE = 0x2B1

    CLASS_NAME = "WTSMonitor"
    WND_NAME = "WTS Event Monitor"

    def __init__(self, als):
        self._als = als
        wc = win32gui.WNDCLASS()
        wc.hInstance = hInst = win32gui.GetModuleHandle(None)
        wc.lpszClassName = self.CLASS_NAME
        wc.lpfnWndProc = self.WndProc
        self.classAtom = win32gui.RegisterClass(wc)
        self.hWnd = win32gui.CreateWindow(self.classAtom, self.WND_NAME,
                                          0, 0, 0, win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT, 0, 0,
                                          hInst, None)
        win32gui.UpdateWindow(self.hWnd)
        win32ts.WTSRegisterSessionNotification(self.hWnd,
                                               win32ts.NOTIFY_FOR_ALL_SESSIONS)

    def start(self):
        win32gui.PumpMessages()

    def stop(self):
        win32gui.PostQuitMessage(0)

    def WndProc(self, hWnd, message, wParam, lParam):
        if message == self.WM_WTSSESSION_CHANGE:
            self.OnSession(wParam, lParam)

    def OnSession(self, event, sessionID):
        if event in (6, 7) and self._als.need_break == False:
            self._als.stop()
        elif event in (5, 8) and self._als.need_break == True:
            self._als.start(True)

class AntiLockScreen(object):
    AM_MOVE = 0
    AM_CLICK = 1
    AM_SCROLL = 2
    def __init__(self, pausetime, app, anti_method=0):
        self._app = app
        self._am = anti_method
        self.pausetime = pausetime
        self.need_break = False
        self.origin_t = time.time()

    def reload(self, pausetime):
        self.pausetime = pausetime

    def _set_origin_time(self, t=None):
        if t is None:
            t = time.time()
        self.origin_t = t
    
    def _anti_lockscreen(self):
        mctrl = mouse.Controller()
        refresh = min(self.pausetime / 1000, 1)
        refresh = max(refresh, 0.1)
        self._set_origin_time()
        t_diff = 0
        while True:
            if self.need_break:
                self._app.mouseinfo.SetValue('')
                break
            time.sleep(refresh)
            current_pos = mctrl.position
            current_t = time.time()
            t_diff = current_t - self.origin_t
            if self._app.frame.IsShown():
                self._app.mouseinfo.SetValue('鼠标位置：%s\n停留时间：%.2f' % (current_pos, t_diff))
            if t_diff > self.pausetime:
                if self._am == self.AM_CLICK:
                    mctrl.click(mouse.Button.left)
                elif self._am == self.AM_SCROLL:
                    mctrl.scroll(0,2)
                else:    
                    mctrl.move(-1, -1)
                self._set_origin_time()
    
    def _mm_on_move(self, x, y):
        self._set_origin_time()
        if self.need_break:
            return False
        
    def _mm_on_click(self, x, y, button, pressed):
        self._set_origin_time()
        if self.need_break:
            return False
        
    def _mm_on_scroll(self, x, y, dx, dy):
        self._set_origin_time()
        if self.need_break:
            return False
    
    def _mouse_monitor(self):
        with mouse.Listener(on_move=self._mm_on_move,
                            on_click=self._mm_on_click,
                            on_scroll=self._mm_on_scroll) as listener:
            listener.join()
    
    def _km_on_press(self, key):
        self._set_origin_time()
        if self.need_break:
            return False

    def _key_monitor(self):
        with keyboard.Listener(on_press=self._km_on_press) as listener:
            listener.join()

    def start(self, switch_icon=False):
        self._app.tbicon.set_icon(self._app.ico_run, switch_icon)
        self.need_break = False
        th_als = threading.Thread(target=self._anti_lockscreen)
        th_als.start()
        th_mm = threading.Thread(target=self._mouse_monitor)
        th_mm.start()
        th_km = threading.Thread(target=self._key_monitor)
        th_km.start()

    def restart(self, event):
        self._app.tbicon.is_paused = False
        self.start(True)

    def stop(self):
        self._app.tbicon.set_icon(self._app.ico_stop, True)
        self.need_break = True
    
    def pause(self, event):
        self._app.tbicon.is_paused = True
        self.stop()