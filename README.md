# Winsome

An attempt at a dynamic window manager for Windows 11. Unusable in current state.

*winsome* is the server that runs the window manager and only responds messages received on a named pipe.

*losesome* is the client program that writes messages on *winsome's* named pipe.

Hotkeys should be handled by a third-party program like [AutoHotkey](https://www.autohotkey.com/).

# Usage

Running winsome:
```
python winsome.py
```

Interacting with winsome via losesome:
```
python losesome.py COMMAND [ARGS...]
```
