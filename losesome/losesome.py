import sys

import pywintypes
import win32file
import win32pipe


def pipe_client(command):
    handle = win32file.CreateFile(
        r'\\.\pipe\Winsome',
        win32file.GENERIC_READ | win32file.GENERIC_WRITE,
        0,
        None,
        win32file.OPEN_EXISTING,
        0,
        None)

    try:
        res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
        if res == 0:
            print('SetNamedPipeHandleState return code:', res)

        data = ' '.join(command)
        win32file.WriteFile(handle, data.encode())

    except pywintypes.error as e:
        if e.args[0] == 2:
            print('No pipe, trying again...')
            time.sleep(1)
        elif e.args[0] == 109:
            print('Broken pipe, exiting...')

    finally:
        win32file.WriteFile(handle, 'END'.encode())
        win32file.CloseHandle(handle)


def main():
    args = sys.argv

    if len(args) < 2:
        print('need more args')
        sys.exit(1)

    pipe_client(args[1:])


if __name__ == '__main__':
    main()
