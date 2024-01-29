import ctypes
from ctypes.wintypes import DWORD, RECT

import win32api
import win32con
import win32gui


def decompose_style(combined_style, styles):
    for style in styles:
        if combined_style & style:
            return True

    return False


def process_hwnd(hwnd, out):
    if not win32gui.IsWindowVisible(hwnd):
        return

    # if minimized
    if win32gui.IsIconic(hwnd):
        return

    # if weird window style
    style = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
    ex_style = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    combined_style = style | ex_style
    undesired_styles = [
        win32con.WS_OVERLAPPED,
        win32con.WS_POPUP,
    ]
    if decompose_style(combined_style, undesired_styles):
        return

    out.append(hwnd)


def get_monitors():
    monitors = []
    for monitor in win32api.EnumDisplayMonitors():
        monitors.append(win32api.GetMonitorInfo(monitor[0]))
    return monitors


def get_extended_frame_bounds(hwnd):
    dwmapi = ctypes.windll.dwmapi
    DWMWA_EXTENDED_FRAME_BOUNDS = 9
    rect = RECT()

    dwmapi.DwmGetWindowAttribute(
            hwnd,
            DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
            ctypes.byref(rect),
            ctypes.sizeof(rect))

    return (rect.left, rect.top, rect.right, rect.bottom)


def get_window_padding(hwnd):
    frame = win32gui.GetWindowRect(hwnd)
    ex_frame = get_extended_frame_bounds(hwnd)

    x0 = frame[0] - ex_frame[0]
    y0 = frame[1] - ex_frame[1]
    x1 = frame[2] - ex_frame[2]
    y1 = frame[3] - ex_frame[3]

    return (x0, y0, x1, y1)


def get_workspace_gaps():
    gaps = {
        'inner': 6,
        'outer': 6,
    }
    return gaps


def arrange_windows(windows):
    for window in windows:
        monitors = get_monitors()
        monitor = monitors[0]
        workarea = monitor['Work']

        gaps = get_workspace_gaps()

        wa_x0 = workarea[0] + gaps['outer']
        wa_y0 = workarea[1] + gaps['outer']
        wa_x1 = workarea[2] - gaps['outer']
        wa_y1 = workarea[3] - gaps['outer']
        wa_w = wa_x1 - wa_x0
        wa_h = wa_y1 - wa_y0

        padding = get_window_padding(window)

        offset = [0, 0, 0, 0]

        offset_x0 = padding[0] + offset[0] + gaps['inner']
        offset_y0 = padding[1] + offset[1] + gaps['inner']
        offset_x1 = padding[2] - offset[2] - gaps['inner']
        offset_y1 = padding[3] - offset[3] - gaps['inner']

        win_x0 = wa_x0 + offset_x0
        win_y0 = wa_y0 + offset_y0
        win_x1 = wa_x1 + offset_x1
        win_y1 = wa_y1 + offset_y1
        win_w = win_x1 - win_x0
        win_h = win_y1 - win_y0

        win32gui.MoveWindow(window, round(win_x0), round(win_y0), round(win_w), round(win_h), True)
