#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compatibility entrypoint for the Kivy desktop app.

This file intentionally delegates to `index_main.py` so there is a single
source of truth for screen/page wiring.
"""

import os
import sys

# Keep frontend folder importable when launched from workspace root.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from index_main import MVPEditorApp


def _ensure_windows_console() -> None:
    if os.name != 'nt':
        return
    try:
        import ctypes
        if ctypes.windll.kernel32.GetConsoleWindow() == 0:
            ctypes.windll.kernel32.AllocConsole()
            sys.stdout = open('CONOUT$', 'w', encoding='utf-8', buffering=1)
            sys.stderr = open('CONOUT$', 'w', encoding='utf-8', buffering=1)
            try:
                sys.stdin = open('CONIN$', 'r', encoding='utf-8')
            except Exception:
                pass
    except Exception:
        pass


if __name__ == '__main__':
    _ensure_windows_console()

    app = MVPEditorApp()
    print('=' * 60)
    print('MVP EDITOR APP STARTED!')
    print('=' * 60)
    print('MAIN MENU:')
    print("  - Click 'PHOTO EDITING' for photo edit options")
    print("  - Click 'VIDEO EDITING' for video edit options")
    print('\nPHOTO EDITING OPTIONS (8 options):')
    print('  - Add Photo, Crop, Rotate, Filters')
    print('  - Brightness, Resize, Export, Undo, Redo')
    print('\nVIDEO EDITING OPTIONS (12 options):')
    print('  - Add Video, Trim, Cut, Split')
    print('  - Audio, Effects, Transitions, Music')
    print('  - Export, Undo, Redo, Settings, Preview')
    print("\nEach editing page has a 'BACK TO MENU' button")
    print('=' * 60)
    app.run()
