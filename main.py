# import keyboard
#
#
# def foo():
#     print('World')
#
# def hook(key):
#     print(key)
#
# keyboard.add_hotkey('Ctrl + 1', lambda: print('Hello'))
# keyboard.add_hotkey('Ctrl + 2', foo)
# # keyboard.add_hotkey('print screen', foo)
# keyboard.add_hotkey('snapshot', foo)
#
# keyboard.wait('Ctrl + Q')

import pygetwindow as gw
import win32con
import win32gui
import win32ui
from PIL import Image
from window.WindowFabric import WindowFabric
from random import randint
import os


for window in WindowFabric.getOpenedWindows():

    # if window.getTitle() == "Параметры":
    #     window.show()

    try:
        window.image(window.getTitle(), str(randint(1, 100))+".png")
    except Exception as e:
        print(f"Error: {e}")

    print(window.getTitle())

names = []

def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        n = win32gui.GetWindowText(hwnd)
        if n:
            names.append(n)

win32gui.EnumWindows(winEnumHandler, None)