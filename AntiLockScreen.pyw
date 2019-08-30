#!/usr/bin/env pythonw3
#-*- coding=utf-8 -*-

import os, os.path
import wx
import threading

from alslib.app import AntiLockScreenApp
from alslib.core import AntiLockScreen
from alslib.core import WTSMonitor

STATUS = 'Beta'
VERNUM = '0.0.1'
VERSION = ' '.join((VERNUM, STATUS))
SCRIPT_PATH = os.path.split(__file__)[0]
ICO_RUN = os.path.join(SCRIPT_PATH, 'res', 'lockscreen_blue.ico')
ICO_STOP = os.path.join(SCRIPT_PATH, 'res', 'lockscreen_red.ico')
CONF_PATH = os.path.join(SCRIPT_PATH, 'config.ini')

def main():
    # Create Application
    app = AntiLockScreenApp(VERSION, ICO_RUN, ICO_STOP, CONF_PATH)
    
    # Load Configurations
    confinfo = app.load_conf()
    pausetime = confinfo['PauseTime']
    antimethod = confinfo['AntiMethod']

    # Create Anti-LockScreen Thread
    als = AntiLockScreen(pausetime, app, antimethod)
    als.start()
    
    # Bind Restart and Pause Menu
    app.tbicon.Bind(wx.EVT_MENU, als.pause, id = app.tbicon.ID_PAUSE)
    app.tbicon.Bind(wx.EVT_MENU, als.restart, id = app.tbicon.ID_RESTART)
    
    # Create WTS-Monitor Thread
    wtsm = WTSMonitor(als)
    th_wtsm = threading.Thread(target=wtsm.start)
    th_wtsm.start()

    # Run Application
    app.run_loop()

if __name__ == '__main__':
    main()