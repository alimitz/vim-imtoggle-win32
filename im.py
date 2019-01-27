import win32api,win32gui,win32con,win32process
import os
import time
import sys
from enum import Enum
import pickle

class Lan(Enum):
    """
    语言代码值参考：https://msdn.microsoft.com/en-us/library/cc233982.aspx
    """
    en = 0x4090409
    zh = 0x8040804
    jj = -0x1fdff7fc

def EnumWndProc( hwnd, extra ):
    windows = extra
    temp=[]
    temp.append(hex(hwnd))
    temp.append(win32gui.GetClassName(hwnd))
    temp.append(win32gui.GetWindowText(hwnd))
    windows[hwnd] = temp
  
def EnumWindows():
    windows = {}
    win32gui.EnumWindows(EnumWndProc, windows)
    print("-------------------------------------------------------------------")
    print("-------------------------------------------------------------------")
    for item in windows :
        print(windows[item])
    print("-------------------------------------------------------------------")
    print("-------------------------------------------------------------------")

lan = Lan.jj
filename = os.environ['VIM_HOME'] + 'vimim.data'
# 获取vim窗口
vim_hwnd=win32gui.FindWindow('Vim',None)
if vim_hwnd == 0:
    print("error: vim window not found")
    sys.exit("error: vim window not found")

if len(sys.argv) == 2:
    if sys.argv[1] == "pim":
        # 获取系统输入法列表
        im_list = win32api.GetKeyboardLayoutList()
        im_list = list(map(hex, im_list))
        print(im_list)
    elif sys.argv[1] == "pwin":
        # 获取当前所有windows窗口列表
        EnumWindows()
    elif sys.argv[1] == "restore":
        # 恢复输入法
        f = open(filename, 'rb')
        old_vim_im = pickle.load(f)
        f.close()
        exec("lan = lan.%s" % (old_vim_im))
        print("lan.name -- %s, lan.value -- %x, old_vim_im -- %s" % (lan.name,lan.value,old_vim_im))
        win32api.SendMessage(
            vim_hwnd,
            win32con.WM_INPUTLANGCHANGEREQUEST,
            0,
            lan.value)
    elif sys.argv[1] in Lan.__members__:
        # 保存原输入法
        t,p = win32process.GetWindowThreadProcessId(vim_hwnd)
        old_vim_im = win32api.GetKeyboardLayout(t)
        f = open(filename, 'wb')
        pickle.dump(Lan(old_vim_im).name, f)
        f.close()

        # 转换输入法
        exec("lan = lan.%s" % (sys.argv[1]))
        print("lan.name -- %s, lan.value -- %x, sys.argv[1] -- %s" % (lan.name,lan.value,sys.argv[1]))
        win32api.SendMessage(
            vim_hwnd,
            win32con.WM_INPUTLANGCHANGEREQUEST,
            0,
            lan.value)
    else:
        print("error im type: valid im type -- en/zh/jj")
        sys.exit("error im type: valid im type -- en/zh/jj")
else:
    print("error para numbers: more than one para is inputed")
