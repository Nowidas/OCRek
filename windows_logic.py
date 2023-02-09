import sys
import ctypes
from ctypes import wintypes
import win32con

byref = ctypes.byref
user32 = ctypes.windll.user32

TLUMACZ_MOD = True
ON_OFF = True

HOTKEYS = {
    # 1 : (ord('Q'), win32con.MOD_WIN | win32con.MOD_SHIFT | 0x4000),
    1: (win32con.VK_F4, 0),
}


def get_TLUMACZ_MOD():
    return False


def get_ON_OFF():
    global ON_OFF
    return ON_OFF


def set_ON_OFF(val):
    global ON_OFF
    # print('tlumacz mod: on') if val else print('tlumacz mod: off')
    ON_OFF = val


def handle_f4():
    global TLUMACZ_MOD
    set_ON_OFF(False) if get_ON_OFF() else set_ON_OFF(True)


HOTKEY_ACTIONS = {1: handle_f4}


def registerKeys():
    for id, (vk, modifiers) in HOTKEYS.items():
        # print ("Registering id", id, "for key", vk)
        if not user32.RegisterHotKey(None, id, modifiers, vk):
            # print ("Unable to register id", id)
            pass


def waitloop():
    try:
        msg = wintypes.MSG()
        while user32.GetMessageA(byref(msg), None, 0, 0) != 0:
            if msg.message == win32con.WM_HOTKEY:
                action_to_take = HOTKEY_ACTIONS.get(msg.wParam)
                if action_to_take:
                    action_to_take()
            user32.TranslateMessage(byref(msg))
            user32.DispatchMessageA(byref(msg))
    finally:
        for id in HOTKEYS.keys():
            user32.UnregisterHotKey(None, id)


def init_getmessageinput():
    msg = wintypes.MSG()
    return msg


def getmessageinput(msg):
    if user32.PeekMessageA(byref(msg), None, 0, 0, 0x0001) != 0:
        if msg.message == win32con.WM_HOTKEY:
            action_to_take = HOTKEY_ACTIONS.get(msg.wParam)
            if action_to_take:
                action_to_take()
        user32.TranslateMessage(byref(msg))
        user32.DispatchMessageA(byref(msg))
