# MVP Editor App - Main Application File
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# Import all page modules
try:
    from .index_page import IndexPage
    from .photo_edit_page import PhotoEditPage
    from .video_edit_page import VideoEditPage
except ImportError:
    from index_page import IndexPage
    from photo_edit_page import PhotoEditPage
    from video_edit_page import VideoEditPage


class MVPEditorApp(App):
    def build(self):
        sm = ScreenManager()
        
        # Add all screens
        index = IndexPage(name='index')
        photo = PhotoEditPage(name='photo')
        video = VideoEditPage(name='video')
        
        sm.add_widget(index)
        sm.add_widget(photo)
        sm.add_widget(video)
        
        return sm


if __name__ == '__main__':
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
