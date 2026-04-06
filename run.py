#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MVP Editor App - Entry Point
Run this script to start the application
"""
import sys
import os

# Add the parent directory to the path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from index_main import MVPEditorApp

if __name__ == '__main__':
    # Ensure a console is available on Windows when the user runs the
    # program by double-clicking (pythonw or missing console). This
    # allocates a console and redirects stdio to it so prints are visible.
    if os.name == 'nt':
        try:
            import ctypes
            # If there's no console window, allocate one
            if ctypes.windll.kernel32.GetConsoleWindow() == 0:
                ctypes.windll.kernel32.AllocConsole()
                sys.stdout = open('CONOUT$', 'w', encoding='utf-8', buffering=1)
                sys.stderr = open('CONOUT$', 'w', encoding='utf-8', buffering=1)
                try:
                    sys.stdin = open('CONIN$', 'r', encoding='utf-8')
                except Exception:
                    pass
        except Exception:
            # If anything fails, continue silently — stdout may still work.
            pass

    app = MVPEditorApp()
    print("=" * 60)
    print("MVP EDITOR APP STARTED!")
    print("=" * 60)
    print("MAIN MENU:")
    print("  - Click 'PHOTO EDITING' for photo edit options")
    print("  - Click 'VIDEO EDITING' for video edit options")
    print("\nPHOTO EDITING OPTIONS (8 options):")
    print("  - Add Photo, Crop, Rotate, Filters")
    print("  - Brightness, Resize, Export, Undo, Redo")
    print("\nVIDEO EDITING OPTIONS (12 options):")
    print("  - Add Video, Trim, Cut, Split")
    print("  - Audio, Effects, Transitions, Music")
    print("  - Export, Undo, Redo, Settings, Preview")
    print("\nEach editing page has a 'BACK TO MENU' button")
    print("=" * 60)
    app.run()
