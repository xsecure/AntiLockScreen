# AntiLockScreen
[README](https://github.com/fatedier/frp/blob/master/README.md)
 | 
[说明文档](https://github.com/fatedier/frp/blob/master/README_zh.md)  
A GUI python3 project "Anti-LockScreen"

## Feature
Just anti-lockscreen!

## Mechanism
Monitor any mouse or keyboard action. If there is no action for more than 5 minutes (300 seconds), the anti-lockscreen action is activated.  
You can customize "no action time" in the configuration file as follows:
> \[COMMON\]  
> pausetime = \{ 300 by default. Unit: second \}

You can also customize the "anti-lockscreen action" to be used as follows:
> \[COMMON\]  
> antimethod = \{ 0 by default. You can choose 0/1/2. \}

"antimethod=0" means "MOVE MOUSE".  
"antimethod=1" means "CLICK MOUSE".  
"antimethod=2" means "SCROLL MOUSE".  
Although the default is "MOVE MOUSE", in some environments, "MOVE MOUSE" is invalid. So **_I prefer "SCROLL MOUSE" (antimethod=2)_**.  

## Other Characteristics
* The application will minimize to the System Tray (Task Bar) by default after it is started.
* Double-click the tray icon to show / hide the application GUI.
* Clicking the "CLOSE BUTTON" will **_HIDE_** the appliction GUI to the System Tray (**NOT EXIT** the application).
* The application will pop up operation menu when you right click on the tray icon:
    * RESTART (disabled by default): Restart the monitor. Enabled when the application is paused.
    * PAUSE: Pause the monitor. Disabled when the application is paused.
    * RELOAD: Reload the configuration file.
    * EXIT: Exit the application.