#!/usr/bin/env pythonw3
#-*- coding=utf-8 -*-

import os
import wx, wx.adv
from collections import OrderedDict

from configparser import ConfigParser
from .utils import make_str, make_bytes

class ALSConfig(ConfigParser):
    def __init__(self, configpath):
        super(ALSConfig, self).__init__()
        self.confpath = configpath
        no_bom_data = None
        if not os.path.isfile(configpath):
            no_bom_data = ''
        else:
            with open(configpath, 'r') as fp:
                data = fp.read()
                if data[:3] == '\xef\xbb\xbf':
                    no_bom_data = data[3:]
        if no_bom_data is not None:
            with open(configpath, 'w') as fp:
                fp.write(no_bom_data)
        self.read(self.confpath)

    def getx(self, section, option=None, default=None, forcetype=None):
        if option is None:
            try:
                ret = self.options(section)
            except:
                ret = ['']
        else:
            try:
                ret = self.get(section, option)
            except:
                ret = default
        if isinstance(ret, bytes):
            ret = make_str(ret)
        if forcetype:
            try:
                ret = forcetype(ret)
            except:
                ret = default
        return ret
        
    def load_all(self):
        ret = OrderedDict()
        ret['PauseTime'] = self.getx('COMMON', 'pausetime', 300, int)
        ret['AntiMethod'] = self.getx('COMMON', 'antimethod', 0, int)
        return ret

class ALSTaskBarIcon(wx.adv.TaskBarIcon):
    ID_CLOSE = wx.NewId()
    ID_PAUSE = wx.NewId()
    ID_RELOAD = wx.NewId()
    ID_RESTART = wx.NewId()
    def __init__(self, app):
        super(ALSTaskBarIcon, self).__init__()
        self._app = app
        self._frame = app.frame
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self._switch_taskbar)
        self.Bind(wx.EVT_MENU, self._reload, id = self.ID_RELOAD)
        self.Bind(wx.EVT_MENU, self._exit, id = self.ID_CLOSE)
        self.is_paused = False

    def set_icon(self, icon_path, is_switch=False):
        if is_switch:
            self.RemoveIcon()
        self.SetIcon(wx.Icon(icon_path, type=wx.BITMAP_TYPE_ICO),
                            'Anti-LockScreen')

    def _switch_taskbar(self, event):
        if self._frame.IsIconized():
            self._frame.Iconize(False)
        if not self._frame.IsShown():
            self._frame.Show(True)
        else:
            self._frame.Hide()
        self._frame.Raise()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_RESTART, '恢复', 'Restart Application!')
        menu.Enable(self.ID_RESTART, self.is_paused)
        menu.Append(self.ID_PAUSE, '暂停', 'Pause Application!')
        menu.Enable(self.ID_PAUSE, not self.is_paused)
        menu.AppendSeparator()
        menu.Append(self.ID_RELOAD, '重载配置', 'Reload the Configurations!')
        menu.AppendSeparator()
        menu.Append(self.ID_CLOSE, '退出', 'Exit this application!')
        return menu

    def _reload(self, event):
        confinfo = self._app.load_conf()
        pausetime = confinfo['PauseTime']
        antimethod = confinfo['AntiMethod']

    def _exit(self, event):
        self.RemoveIcon()
        self.Destroy()
        self._frame.Destroy()
        os._exit(0)

class AntiLockScreenApp(object):
    FIXED_SIZE = (400, 200)
    def __init__(self, v, ico_run, ico_stop, confpath=None):
        # Read Configuration
        if confpath is None:
            confpath = 'config.ini'
        self._confpath = confpath
        
        # Create App
        self.app = wx.App()
        # Create and Set Frame
        self.frame = wx.Frame(None, size = self.FIXED_SIZE,
                              title = '防锁屏工具 v%s' % v,
                              style =  wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.frame.Bind(wx.EVT_CLOSE, self._hide_to_bar)
        # Create TaskBarIcon
        self.tbicon = ALSTaskBarIcon(self)
        self.ico_run = ico_run
        self.ico_stop = ico_stop
        # Create Panel(Background)
        self.bkg = wx.Panel(self.frame)
        self.draw_ui()

    def load_conf(self):
        conf = ALSConfig(self._confpath)
        conf_ret = conf.load_all()
        confinfo = ' | '.join(['%s:%s' % (k, conf_ret[k]) for k in conf_ret])
        self.confinfo.SetValue(confinfo)
        return conf_ret

    def _hide_to_bar(self, event):
        self.frame.Hide()

    def draw_ui(self):
        self.confinfo = wx.TextCtrl(self.bkg, style=wx.TE_READONLY)
        confsbs = wx.StaticBoxSizer(wx.HORIZONTAL, self.bkg, '配置信息')
        confsbs.Add(self.confinfo, proportion=1, flag=wx.LEFT, border=5)

        self.mouseinfo = wx.TextCtrl(self.bkg, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_NO_VSCROLL)
        mousesbs = wx.StaticBoxSizer(wx.HORIZONTAL, self.bkg, '鼠标状态')
        mousesbs.Add(self.mouseinfo, proportion=1, flag=wx.LEFT, border=5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(confsbs, proportion=0, flag=wx.EXPAND|wx.ALL, border=5)
        vbox.Add(mousesbs, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
        self.bkg.SetSizer(vbox)

    def run_loop(self):
        # Debug - Show frame
        # Releas - Hide frame
        #self.frame.Show()
        self.app.MainLoop()