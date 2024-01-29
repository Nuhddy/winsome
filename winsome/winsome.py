import sys
import threading

import pywintypes
import win32file
import win32gui
import win32pipe

import window


def pipe_server():
    print('[Starting server...]')
    BUF_SIZE = 1024

    while True:
        pipe = win32pipe.CreateNamedPipe(
            r'\\.\pipe\Winsome',
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            1, BUF_SIZE, BUF_SIZE,
            0,
            None)

        try:
            win32pipe.ConnectNamedPipe(pipe, None)

            while True:
                resp = win32file.ReadFile(pipe, BUF_SIZE)

                message = resp[1].decode()
                if not message:
                    continue

                command = message.split()
                print('command:', command)

                if command[0] == 'exit':
                    print('[Server stopped]')
                    return False

                break

        except pywintypes.error as e:
            if e.args[0] == 2:
                print('No pipe, trying again...')
                time.sleep(1)
            elif e.args[0] == 109:
                print('Broken pipe, exiting...')

        finally:
            win32file.CloseHandle(pipe)


def winsome_init():
    windows = []
    win32gui.EnumWindows(window.process_hwnd, windows)
    window.arrange_windows(windows)


if __name__ == '__main__':
    threading.Thread(target=pipe_server).start()
    winsome_init()
