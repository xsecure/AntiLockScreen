# AntiLockScreen
[README](https://github.com/xsecure/AntiLockScreen/blob/master/README.md) | 
[说明文档](https://github.com/xsecure/AntiLockScreen/blob/master/README_zh.md)  
一款使用Python3编写的带有图形界面的防锁屏小程序。  
依赖问题请参考[requirements.txt](https://github.com/xsecure/AntiLockScreen/blob/master/requirements.txt)文件。

## 功能
就只是防锁屏而已

## 机制
监控任何鼠标或键盘的动作。如果超过5分钟（300秒）无任何动作，则启动防锁屏动作。  
你可以用如下方式定义“无动作时间”的数值：
> &#91;COMMON&#93;  
> pausetime = &#123; 默认为300。单位：秒 &#125;

你还可以用如下方式定义程序采用哪种“防锁屏动作”：
> &#91;COMMON&#93;  
> antimethod = &#123; 默认为0。你可自选：0、1、2三种 &#125;

"antimethod=0" 意味着 “移动鼠标”。  
"antimethod=1" 意味着 “点击鼠标”。  
"antimethod=2" 意味着 “滚动鼠标滚轮”。  
虽然默认选项是 “移动鼠标” ，但某些环境下 “移动鼠标” 操作时无效的。所以我 **_更倾向于 “滚动鼠标滚轮” (antimethod=2)_**。  

## 其他特性
* 启动后，程序默认会最小化到系统托盘（又被称为任务栏）。
* 双击托盘图标可以显示 / 隐藏程序界面。
* 点击“关闭按钮”会 **_隐藏_** 程序界面到系统托盘（ **并非退出** 程序）。
* 右键点击托盘图标会弹出菜单：
    * 恢复 (默认为禁用): 恢复监控。程序暂停时会被启用。
    * 暂停：暂停监控。程序暂停时会被禁用。
    * 重载配置：重新载入配置文件。
    * 退出：退出程序。