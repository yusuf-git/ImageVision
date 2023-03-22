from time import sleep
import pyautogui
#import win32api
#from win32con import *

#Scroll one up
#win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, 1, 0)

#Scroll one down
#win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, -1, 0)

#Scroll one to the right
#win32api.mouse_event(MOUSEEVENTF_HWHEEL, x, y, 1, 0)

#Scroll one to the left
#win32api.mouse_event(MOUSEEVENTF_HWHEEL, x, y, -1, 0)

#sleep(4)
#pyautogui.scroll(-4, 200,200)


import win32api 
import win32con
import ctypes
from ctypes import windll, CFUNCTYPE, c_int, c_void_p, wintypes

 

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
user32.CallNextHookEx.argtypes = [ctypes.wintypes.HHOOK,c_int, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM]

 

def LowLevelMouseProc(nCode, wParam, lParam):
    if wParam == win32con.WM_MOUSEWHEEL:
        print("mousewheel triggerd!")
    return user32.CallNextHookEx(hook_id, nCode, wParam, lParam)

 

if __name__ == '__main__':
    CMPFUNC = CFUNCTYPE(c_void_p, c_int, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)
    user32.SetWindowsHookExW.argtypes = [c_int,CMPFUNC,ctypes.wintypes.HINSTANCE,ctypes.wintypes.DWORD]
    pointer = CMPFUNC(LowLevelMouseProc)
    hook_id = user32.SetWindowsHookExW(win32con.WH_MOUSE_LL,pointer,win32api.GetModuleHandle(None), 0)
    msg = ctypes.wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
        user32.TranslateMessage(msg)
        user32.DispatchMessageW(msg)
