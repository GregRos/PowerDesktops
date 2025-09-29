import keyboard
from win32con import VK_CAPITAL
from win32api import GetKeyState


def force_caps_off():
    if GetKeyState(VK_CAPITAL) == 1:
        keyboard.press_and_release("capslock")
