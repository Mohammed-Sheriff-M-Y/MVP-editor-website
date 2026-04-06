# Frontend Code Structure - Refactored

## Overview
The frontend code has been reorganized into separate, modular files for better maintainability and organization.

## File Structure

```
frontend/
├── __init__.py                 # Package initialization
├── index_main.py              # Main application entry point
├── backend_module.py          # Shared backend setup and file operations
├── index_page.py              # Main menu page (IndexPage class)
├── photo_edit_page.py         # Photo editing page (PhotoEditPage class)
├── video_edit_page.py         # Video editing page (VideoEditPage class)
├── logo.png                   # Logo image
└── [other files]
```

## Files Description

### 1. **index_main.py** - Main Application Entry Point
- Contains `MVPEditorApp` class
- Manages screen navigation
- Initialize all pages (Index, Photo, Video)
- Run the application with `python index_main.py`

### 2. **backend_module.py** - Shared Backend Module
- Contains all file operation functions
- Photo operations: upload_photo, list_photos, process_photo, get_photo_file_path
- Video operations: upload_video, list_videos, process_video, get_video_file_path
- Handles file management and directory creation
- Imported by all page modules

### 3. **index_page.py** - Main Menu Page
- `IndexPage` class - The welcome/main menu screen
- Contains logo display and welcome message
- Buttons to navigate to Photo or Video editing pages
- Left sidebar with branding

### 4. **photo_edit_page.py** - Photo Editing Page
- `PhotoEditPage` class - Photo editing interface
- Features:
  - Add Photo button
  - 8 editing options (Crop, Rotate, Filters, Brightness, Resize, Export, Undo, Redo)
  - List of uploaded photos
  - Process and Download buttons
  - Clear all photos (with file deletion)
  - Back to Menu button

### 5. **video_edit_page.py** - Video Editing Page
- `VideoEditPage` class - Video editing interface
- Features:
  - Add Video button
  - 12 editing options (Trim, Cut, Split, Audio, Effects, etc.)
  - List of uploaded videos
  - Process and Download buttons
  - Clear all videos (with file deletion)
  - Back to Menu button

### 6. **__init__.py** - Package Initialization
- Makes frontend a proper Python package
- Exports all main classes and modules
- Allows importing from frontend package

## How to Run

### Option 1: Run the main application
```bash
cd frontend
python index_main.py
```

### Option 2: Run from parent directory (if properly set up)
```bash
python -m frontend.index_main
```

## Code Organization Benefits

1. **Modularity** - Each page has its own file, making it easy to modify individual pages
2. **Maintainability** - Easier to find and update specific functionality
3. **Reusability** - Components can be imported and used independently
4. **Scalability** - New pages can be added easily following the same pattern
5. **Collaboration** - Multiple developers can work on different pages simultaneously
6. **Testing** - Individual modules can be tested in isolation

## File Dependencies

```
index_main.py
├── index_page.py
├── photo_edit_page.py
│   └── backend_module.py
└── video_edit_page.py
    └── backend_module.py
```

## Important Notes

- All imports use relative imports (from .module_name)
- Backend operations are centralized in backend_module.py
- Clear button now deletes actual files, not just the UI
- All functionality from the original index.py is preserved
