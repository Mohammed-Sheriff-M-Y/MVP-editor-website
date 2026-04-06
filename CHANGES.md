# MVP Editor - Button Color & Icon Update

## Quick Start Simplification (Feb 2026)

- Added `start.cmd` as a single easy launcher for Windows.
- `start.cmd` shows a simple menu:
	- `1` = Start Web App
	- `2` = Start Desktop App (Kivy)
	- `3` = Exit
- Startup now auto-detects `.venv-1` or `.venv` and only creates `.venv` if needed.
- Updated `start-web.cmd` and `start-kivy.cmd` to use the same auto-detect logic.

### Recommended way to run now

From project root, run:

```bat
start.cmd
```

## Changes Made

### PhotoEditPage & VideoEditPage Button Styling

#### Before:
- **Button Color**: Dark gray `(0.12, 0.12, 0.12, 1)`
- **Text Color**: White `(1, 1, 1, 1)`
- **Icon Size**: 24pt
- **Layout**: Icons and text inside buttons

#### After:
- **Button Color**: WHITE `(1, 1, 1, 1)` ✅
- **Text Color**: BLACK `(0, 0, 0, 1)` for visibility on white
- **Icon Size**: 28pt (larger for better visibility)
- **Layout**: Icons and text inside buttons with proper spacing

---

## Button Options & Icons

### Photo Editing (PhotoEditPage)
| Icon | Label | Function |
|------|-------|----------|
| 📷 | Add Photo | Upload new photos |
| ✂️ | Crop | Crop photos |
| 🔄 | Rotate | Rotate photos |
| 🎨 | Filters | Apply filters |
| ✨ | Brightness | Adjust brightness |
| 🔍 | Resize | Resize photos |
| 💾 | Export | Export/save photos |
| ↩️ | Undo | Undo actions |

### Video Editing (VideoEditPage)
| Icon | Label | Function |
|------|-------|----------|
| 📹 | Add Video | Upload new videos |
| ✂️ | Trim | Trim videos |
| 🎬 | Cut | Cut segments |
| 🎞️ | Split | Split videos |
| 🔊 | Audio | Audio controls |
| 🎨 | Effects | Add effects |
| ⚡ | Transitions | Add transitions |
| 🎵 | Music | Add music |
| 💾 | Export | Export videos |
| ↩️ | Undo | Undo actions |
| ⚙️ | Settings | Video settings |
| 📊 | Preview | Preview video |

---

## Technical Details

### Updated Code Structure
```python
# All option buttons now use:
OPTION_BG = (1, 1, 1, 1)  # WHITE background
color=(0, 0, 0, 1)         # BLACK text
font_size=28               # Larger icons
```

### Icon Display Format
- Icons are extracted from button text using emoji detection
- Format: `"📷 Add Photo"` → Icon: 📷, Label: "Add Photo"
- Icons displayed at 28pt, text at 16pt
- Horizontal layout with 10px spacing between icon and text

---

## Frontend Status
✅ Syntax validated (no errors)
✅ Backend running at `http://127.0.0.1:5000`
✅ All API endpoints functional
✅ White buttons with black text implemented
✅ Icons properly displayed

## Running the Application

### Start Backend
```bash
cd "c:\Users\eve1\MVP Editor app"
python backend.py
```

### Run Kivy Frontend
```bash
python index.py
```

### Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```
