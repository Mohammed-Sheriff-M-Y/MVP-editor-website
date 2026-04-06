# -------- How to Use Page (Notebook Style) --------
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line


class HowToUsePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Root layout
        main_layout = BoxLayout(orientation="vertical", padding=0, spacing=0)

        # Background - light cream color like notebook
        with main_layout.canvas.before:
            Color(0.95, 0.94, 0.92, 1)  # Cream/notebook color
            self.bg = Rectangle(size=main_layout.size, pos=main_layout.pos)

        main_layout.bind(size=self.update_bg, pos=self.update_bg)

        # Header
        header = BoxLayout(
            size_hint_y=None,
            height=90,
            padding=(30, 15),
            orientation="vertical",
            spacing=5
        )
        with header.canvas.before:
            Color(0.1, 0.3, 0.5, 1)  # Dark blue like notebook cover
            Rectangle(size=header.size, pos=header.pos)

        title = Label(
            text="MVP EDITOR",
            font_size=42,
            bold=True,
            color=(1, 1, 1, 1),
        )
        subtitle = Label(
            text="Complete User Guide & Instructions",
            font_size=14,
            color=(0.8, 0.8, 1, 1),
            italic=True
        )
        header.add_widget(title)
        header.add_widget(subtitle)
        main_layout.add_widget(header)

        # Scrollable content area
        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=20,
            padding=30
        )
        content.bind(minimum_height=content.setter('height'))

        # Section 1: Overview
        content.add_widget(self.create_card(
            "📖 WELCOME TO MVP EDITOR",
            "MVP Editor is a professional-grade photo and video editing application designed for "
            "both beginners and experienced creators. Whether you're editing family photos or creating "
            "professional video content, our intuitive interface makes it easy to achieve stunning results.\n\n"
            "KEY FEATURES:\n"
            "→ User-friendly editing tools\n"
            "→ Fast processing and rendering\n"
            "→ Multiple file format support\n"
            "→ Instant preview functionality\n"
            "→ Undo/Redo for complete control\n\n"
            "SUPPORTED FORMATS:\n"
            "Photos: JPG, PNG, BMP, GIF\n"
            "Videos: MP4, MOV, AVI, MKV"
        ))

        # Section 2: Main Menu
        content.add_widget(self.create_card(
            "🏠 MAIN MENU - YOUR STARTING POINT",
            "When you launch MVP Editor, you'll see the beautiful main menu with three key options:\n\n"
            "1️⃣ PHOTO EDITING BUTTON\n"
            "   Click this to enter the photo editing workspace. This is perfect for:\n"
            "   → Enhancing personal photos and memories\n"
            "   → Creating social media content\n"
            "   → Adjusting lighting and colors\n"
            "   → Cropping and resizing images\n"
            "   → Applying filters and effects\n\n"
            "2️⃣ VIDEO EDITING BUTTON\n"
            "   Click this to enter the video editing workspace. Ideal for:\n"
            "   → Creating vlogs and tutorials\n"
            "   → Editing home videos\n"
            "   → Adding effects and transitions\n"
            "   → Professional video production\n"
            "   → Audio management and music addition\n\n"
            "❓ HELP ICON (? BUTTON)\n"
            "   Located in the top-right corner of the main menu. Click anytime to access "
            "this comprehensive guide and learn about all features."
        ))

        # Section 3: Photo Editing
        content.add_widget(self.create_card(
            "📷 PHOTO EDITING - COMPLETE FEATURES GUIDE",
            "FEATURE 1: ADD PHOTO\n"
            "   → Opens file browser to select image from your device\n"
            "   → Displays selected photo on editing canvas\n"
            "   → Supports JPG, PNG, BMP, GIF formats\n"
            "   → Shows file size and dimensions\n\n"
            "FEATURE 2: CROP\n"
            "   → Remove unwanted areas from your photo\n"
            "   → Adjust aspect ratio (square, 16:9, 4:3, custom)\n"
            "   → Preview before applying\n"
            "   → Perfect for framing subjects\n\n"
            "FEATURE 3: ROTATE\n"
            "   → Rotate 90 degrees clockwise\n"
            "   → Rotate 90 degrees counter-clockwise\n"
            "   → Rotate 180 degrees (flip)\n"
            "   → Perfect for fixing wrongly oriented photos\n\n"
            "FEATURE 4: FILTERS\n"
            "   → Black & White: Classic monochrome effect\n"
            "   → Sepia: Vintage, aged paper look\n"
            "   → Vintage: Retro film aesthetic\n"
            "   → Cool: Blue-tinted, cold appearance\n"
            "   → Warm: Orange-tinted, warm sunshine look\n\n"
            "FEATURE 5: BRIGHTNESS\n"
            "   → Increase or decrease overall brightness\n"
            "   → Adjust contrast levels\n"
            "   → Fix over/under exposed photos\n"
            "   → Real-time preview of changes\n\n"
            "FEATURE 6: RESIZE\n"
            "   → Change width and height dimensions\n"
            "   → Maintain aspect ratio option\n"
            "   → Custom size input\n"
            "   → Perfect for web and social media\n\n"
            "FEATURE 7: EXPORT\n"
            "   → Save edited photo to your device\n"
            "   → Choose file location\n"
            "   → Set quality and format\n"
            "   → Download to specified folder\n\n"
            "FEATURE 8 & 9: UNDO / REDO\n"
            "   → UNDO: Revert last action or change\n"
            "   → REDO: Restore action you just undid\n"
            "   → Use multiple times for complete control"
        ))

        # Section 4: Video Editing
        content.add_widget(self.create_card(
            "🎬 VIDEO EDITING - COMPLETE FEATURES GUIDE",
            "FEATURE 1: ADD VIDEO\n"
            "   → Browse and select video from device\n"
            "   → Supports MP4, MOV, AVI, MKV formats\n"
            "   → Displays video preview and duration\n"
            "   → Shows file size and resolution\n\n"
            "FEATURE 2: TRIM\n"
            "   → Cut unnecessary content from beginning\n"
            "   → Cut unwanted content from end\n"
            "   → Keep only the important parts\n"
            "   → Real-time preview while trimming\n\n"
            "FEATURE 3: CUT\n"
            "   → Remove specific sections from middle\n"
            "   → Extract only the content you want\n"
            "   → Precise time-based cutting\n"
            "   → Smooth transitions after cut\n\n"
            "FEATURE 4: SPLIT\n"
            "   → Divide video into multiple segments\n"
            "   → Edit each segment separately\n"
            "   → Combine segments back together\n"
            "   → Perfect for organizing content\n\n"
            "FEATURE 5: AUDIO\n"
            "   → Extract audio from video\n"
            "   → Remove audio track completely\n"
            "   → Replace with different audio\n"
            "   → Adjust volume levels\n\n"
            "FEATURE 6: EFFECTS\n"
            "   → Apply visual effects\n"
            "   → Speed up or slow down video\n"
            "   → Add blurs and transitions\n"
            "   → Enhance video appearance\n\n"
            "FEATURE 7: TRANSITIONS\n"
            "   → Fade in/out effects\n"
            "   → Slide transitions\n"
            "   → Dissolve effects\n"
            "   → Smooth clip connections\n\n"
            "FEATURE 8: MUSIC\n"
            "   → Add background music\n"
            "   → Include sound effects\n"
            "   → Adjust audio volume\n"
            "   → Synchronize with video pace\n\n"
            "FEATURE 9: PREVIEW\n"
            "   → Watch edited video before saving\n"
            "   → Check quality and effects\n"
            "   → Verify transitions and timing\n"
            "   → No resource usage for playback\n\n"
            "FEATURE 10: EXPORT\n"
            "   → Save final edited video\n"
            "   → Choose quality settings\n"
            "   → Select output format\n"
            "   → Download to device\n\n"
            "FEATURE 11 & 12: UNDO / REDO\n"
            "   → UNDO: Revert last editing action\n"
            "   → REDO: Restore undone action\n"
            "   → Multiple undo/redo support"
        ))

        # Section 5: Step-by-Step Workflow
        content.add_widget(self.create_card(
            "⚙️ STEP-BY-STEP EDITING WORKFLOW",
            "PHOTO EDITING WORKFLOW:\n\n"
            "STEP 1: START\n"
            "   → From the main menu, click 'PHOTO EDITING'\n"
            "   → Enter the photo editing workspace\n"
            "   → See the editing interface with all tools\n\n"
            "STEP 2: UPLOAD\n"
            "   → Click 'ADD PHOTO' button\n"
            "   → Browse your device for image\n"
            "   → Select and confirm\n"
            "   → Photo loads on canvas\n\n"
            "STEP 3: EDIT\n"
            "   → Use available tools as needed\n"
            "   → Crop to frame subject\n"
            "   → Adjust brightness if needed\n"
            "   → Apply filters for style\n"
            "   → Rotate if necessary\n"
            "   → Resize for intended use\n\n"
            "STEP 4: REVIEW\n"
            "   → Look at preview of changes\n"
            "   → Verify quality and appearance\n"
            "   → Check colors and composition\n\n"
            "STEP 5: UNDO IF NEEDED\n"
            "   → Click 'UNDO' if something wrong\n"
            "   → Revert multiple steps if needed\n"
            "   → Use 'REDO' to restore changes\n\n"
            "STEP 6: EXPORT\n"
            "   → Click 'EXPORT' when satisfied\n"
            "   → Choose location to save\n"
            "   → Photo is saved to device\n\n"
            "STEP 7: RETURN\n"
            "   → Click 'BACK TO MENU'\n"
            "   → Return to main interface\n"
            "   → Ready to edit another photo\n\n\n"
            "VIDEO EDITING WORKFLOW:\n\n"
            "Follows same pattern as photos but with additional steps:\n"
            "→ Add Video → Trim/Cut/Split → Add Effects → Add Music → "
            "Preview → Export → Return to Menu"
        ))

        # Section 6: Pro Tips
        content.add_widget(self.create_card(
            "💡 PRO TIPS & BEST PRACTICES",
            "EDITING TECHNIQUES:\n\n"
            "✓ Start with basic adjustments (crop, brightness)\n"
            "   Before applying filters and effects\n\n"
            "✓ Use UNDO liberally - experiment freely\n"
            "   No permanent changes until you export\n\n"
            "✓ Preview frequently\n"
            "   Check progress after each major edit\n\n"
            "✓ Layer multiple edits\n"
            "   Combine crop, filter, and brightness for best results\n\n"
            "✓ Maintain aspect ratio when resizing\n"
            "   Prevents distortion of subjects\n\n"
            "ADVANCED TECHNIQUES:\n\n"
            "✓ For videos: Always preview before export\n"
            "   Catch issues before final save\n\n"
            "✓ Test combinations of filters\n"
            "   Different filters work better on different photos\n\n"
            "✓ Use brightness strategically\n"
            "   Can salvage poorly lit photos\n\n"
            "✓ Organize your edits\n"
            "   Work on one aspect at a time\n\n"
            "EXPORT BEST PRACTICES:\n\n"
            "✓ Always EXPORT to save permanently\n"
            "   Undo/Redo only work in current session\n\n"
            "✓ Choose appropriate quality for use\n"
            "   Web: Medium quality\n"
            "   Printing: High quality\n"
            "   Social Media: Optimized quality\n\n"
            "✓ Keep original files\n"
            "   Export with different name\n"
            "   Preserve original if needed\n\n"
            "✓ Verify file before closing\n"
            "   Confirm export completed successfully"
        ))

        # Section 7: Troubleshooting
        content.add_widget(self.create_card(
            "🔧 TROUBLESHOOTING & SOLUTIONS",
            "PROBLEM: File Won't Upload\n"
            "SOLUTION:\n"
            "   → Check file format is supported (JPG, PNG, MP4, etc.)\n"
            "   → Verify file path is correct\n"
            "   → Try with smaller file size\n"
            "   → Check sufficient storage space available\n"
            "   → Close and restart app\n\n"
            "PROBLEM: Edit Didn't Save\n"
            "SOLUTION:\n"
            "   → Remember: EXPORT to save permanently\n"
            "   → UNDO removes changes only in current session\n"
            "   → Always click EXPORT before closing app\n"
            "   → Check export location is accessible\n\n"
            "PROBLEM: App Running Slow\n"
            "SOLUTION:\n"
            "   → Close unnecessary background programs\n"
            "   → Free up device storage space\n"
            "   → Try editing smaller files first\n"
            "   → Reduce preview quality temporarily\n"
            "   → Restart the application\n\n"
            "PROBLEM: Export Quality Too Low\n"
            "SOLUTION:\n"
            "   → Select maximum quality in export settings\n"
            "   → Use original format when possible\n"
            "   → Check image resolution before editing\n"
            "   → Don't resize smaller than needed\n\n"
            "PROBLEM: Video Playback Issues\n"
            "SOLUTION:\n"
            "   → Ensure video format is supported\n"
            "   → Try smaller video file\n"
            "   → Update app to latest version\n"
            "   → Check device codec support\n\n"
            "QUICK FIXES:\n"
            "   → Stuck? Click 'BACK' and start fresh\n"
            "   → Lost changes? Use REDO immediately\n"
            "   → Confused? Click ? icon for help\n"
            "   → Need to reset? Close and reopen app"
        ))

        # Section 8: Keyboard Shortcuts & Reference
        content.add_widget(self.create_card(
            "⌨️ QUICK REFERENCE & KEYBOARD GUIDE",
            "PHOTO EDITING INTERFACE:\n\n"
            "TOP ROW:\n"
            "   [ADD PHOTO] [CROP] [ROTATE]\n"
            "   Use to load, frame, and orient images\n\n"
            "MIDDLE ROW:\n"
            "   [FILTERS] [BRIGHTNESS] [RESIZE]\n"
            "   Enhance appearance and adjust dimensions\n\n"
            "BOTTOM ROW:\n"
            "   [EXPORT] [UNDO] [REDO]\n"
            "   Save work and manage changes\n\n\n"
            "VIDEO EDITING INTERFACE:\n\n"
            "EDITING BUTTONS:\n"
            "   [ADD] [TRIM] [CUT] [SPLIT]\n"
            "   Control video structure and length\n\n"
            "ENHANCEMENT BUTTONS:\n"
            "   [AUDIO] [EFFECTS] [TRANSITIONS] [MUSIC]\n"
            "   Add polish and professional touches\n\n"
            "OUTPUT BUTTONS:\n"
            "   [PREVIEW] [EXPORT] [UNDO] [REDO]\n"
            "   Review and save your work\n\n\n"
            "FILE FORMAT REFERENCE:\n\n"
            "IMAGES:\n"
            "   JPG - Best for photos, smaller file size\n"
            "   PNG - Lossless quality, larger files\n"
            "   BMP - Uncompressed, rarely used\n"
            "   GIF - Animated or simple graphics\n\n"
            "VIDEOS:\n"
            "   MP4 - Most compatible, great quality\n"
            "   MOV - Apple format, high quality\n"
            "   AVI - Windows format, good quality\n"
            "   MKV - Advanced container, all features\n\n\n"
            "COMMON BUTTON MEANINGS:\n"
            "   ✕ or X = Close / Cancel\n"
            "   ✓ or ✔ = Confirm / Accept\n"
            "   ↺ = Undo previous action\n"
            "   ↻ = Redo undone action\n"
            "   ← = Go back to previous screen"
        ))

        # Add spacing at end
        content.add_widget(Label(size_hint_y=None, height=20))

        scroll.add_widget(content)
        main_layout.add_widget(scroll)

        # Footer with Back Button
        footer = BoxLayout(
            size_hint_y=None,
            height=70,
            padding=15,
            spacing=10
        )
        with footer.canvas.before:
            Color(0.1, 0.3, 0.5, 1)
            Rectangle(size=footer.size, pos=footer.pos)

        back_btn = Button(
            text="← BACK TO MENU",
            background_normal="",
            background_color=(0.15, 0.6, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=16,
            bold=True
        )
        back_btn.bind(on_press=self.go_back)
        footer.add_widget(back_btn)

        main_layout.add_widget(footer)
        self.add_widget(main_layout)

    def create_card(self, title, content):
        """Create a clean notebook-style card without boxes"""
        card_container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=15,
            padding=(30, 20, 30, 20)
        )

        # Title with emoji (no box)
        title_label = Label(
            text=title,
            font_size=18,
            bold=True,
            color=(0.15, 0.35, 0.6, 1),  # Dark blue
            halign="left",
            valign="top",
            size_hint_y=None,
            height=50
        )
        card_container.add_widget(title_label)

        # Content with proper spacing - FIXED FOR TEXT WRAPPING
        content_label = Label(
            text=content,
            font_size=12,
            color=(0.2, 0.2, 0.2, 1),
            halign="left",
            valign="top",
            markup=False,
            text_size=(700, None),  # Set fixed width for wrapping
            line_height=1.7,
            size_hint_y=None
        )
        
        # Force texture update to calculate proper height
        content_label.texture_update()
        content_label.height = max(content_label.texture_size[1] + 50, 150)

        card_container.add_widget(content_label)

        # Add divider
        divider = Label(size_hint_y=None, height=2)
        with divider.canvas.before:
            Color(0.85, 0.84, 0.82, 1)
            Rectangle(size=divider.size, pos=divider.pos)

        card_container.add_widget(divider)
        card_container.size_hint_y = None
        card_container.height = title_label.height + content_label.height + divider.height + 60

        return card_container

    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def go_back(self, instance):
        print("Returning to main menu...")
        self.manager.current = 'index'


