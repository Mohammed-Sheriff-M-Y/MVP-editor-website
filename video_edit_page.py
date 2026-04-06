# Video Editing Page
import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView

# Handle both relative and direct imports
try:
    from .backend_module import bm
except ImportError:
    from backend_module import bm


class VideoEditPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        
        # White background
        with main_layout.canvas.before:
            Color(0, 0, 0, 1)
            self.bg = Rectangle(size=main_layout.size, pos=main_layout.pos)
        
        main_layout.bind(size=self.update_bg, pos=self.update_bg)
        
        # Title
        title = Label(
            text="VIDEO EDITING",
            font_size=28,
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=0.15
        )
        main_layout.add_widget(title)
        
        # Subtitle
        self.video_subtitle = Label(
            text="Select a video editing option",
            font_size=14,
            color=(1, 1, 1, 1),
            size_hint_y=0.1
        )
        main_layout.add_widget(self.video_subtitle)
        
        # Top bar for uploaded videos (shown above options)
        self.video_top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        main_layout.add_widget(self.video_top_bar)

        # Separate Add Video button above options
        add_video_btn = Button(text='Add Video', size_hint_y=None, height=50, background_normal='', background_color=(0.2,0.6,0.9,1), color=(1,1,1,1))
        add_video_btn.bind(on_press=lambda inst: self.open_filechooser_upload('video'))
        main_layout.add_widget(add_video_btn)

        # Unified action button sizing
        ACTION_BTN_HEIGHT = 60
        OPTION_HEIGHT = 70

        # Grid layout for editing options
        grid = GridLayout(cols=3, spacing=15, padding=15, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        options = [
            ("Trim", "trim"),
            ("Cut", "cut"),
            ("Split", "split"),
            ("Audio", "audio"),
            ("Effects", "effects"),
            ("Transitions", "transitions"),
            ("Music", "music"),
            ("Export", "export"),
            ("Undo", "undo"),
            ("Redo", "redo"),
            ("Settings", "settings"),
            ("Preview", "preview"),
        ]
        
        # Uniform button style: WHITE background with black text and icons
        OPTION_HEIGHT = 70
        OPTION_FONT = 16
        OPTION_BG = (1, 1, 1, 1)  # WHITE buttons

        for label, operation in options:
            btn = Button(
            text=label,
                size_hint_x=1,
                size_hint_y=None,
                height=OPTION_HEIGHT,
                background_normal="",
                background_color=OPTION_BG,
                color=(0, 0, 0, 1),  # BLACK text for white buttons
                font_size=OPTION_FONT,
                bold=True
            )
            btn.bind(on_press=lambda _x, op=operation, text=label: self.on_option_press(op, text))
            grid.add_widget(btn)
        
        # Video list area
        self.base_api = 'http://127.0.0.1:5000/api'
        self.video_list_container = BoxLayout(orientation='vertical', size_hint_y=0.25)
        self.video_list_label = Label(text='Uploaded Videos: (loading...)', size_hint_y=None, height=30, color=(1,1,1,1))
        self.video_list_scroll = ScrollView()
        self.video_list_grid = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        self.video_list_grid.bind(minimum_height=self.video_list_grid.setter('height'))
        self.video_list_scroll.add_widget(self.video_list_grid)
        self.video_list_container.add_widget(self.video_list_label)
        self.video_list_container.add_widget(self.video_list_scroll)

        # Process and Download buttons (single row)
        video_action_row = BoxLayout(size_hint_y=None, height=ACTION_BTN_HEIGHT + 10, spacing=10, padding=10)
        self.process_video_btn = Button(text='Process', size_hint_x=0.5, size_hint_y=None, height=ACTION_BTN_HEIGHT, background_normal="", background_color=(0.2, 0.6, 0.9, 1), color=(1, 1, 1, 1))
        self.download_video_btn = Button(text='Download', size_hint_x=0.5, size_hint_y=None, height=ACTION_BTN_HEIGHT, background_normal="", background_color=(0.2, 0.8, 0.4, 1), color=(1, 1, 1, 1))
        self.process_video_btn.bind(on_press=self.on_process_video_click)
        self.download_video_btn.bind(on_press=self.on_download_video_click)
        video_action_row.add_widget(self.process_video_btn)
        video_action_row.add_widget(self.download_video_btn)

        # Clear and Done buttons
        video_secondary_action_row = BoxLayout(size_hint_y=None, height=ACTION_BTN_HEIGHT + 10, spacing=10, padding=10)
        self.clear_video_btn = Button(text='Clear', size_hint_x=0.5, size_hint_y=None, height=ACTION_BTN_HEIGHT, background_normal="", background_color=(0.7, 0.2, 0.2, 1), color=(1, 1, 1, 1))
        self.done_video_btn = Button(text='Done', size_hint_x=0.5, size_hint_y=None, height=ACTION_BTN_HEIGHT, background_normal="", background_color=(0.3, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        self.clear_video_btn.bind(on_press=self.on_clear_videos_click)
        self.done_video_btn.bind(on_press=self.on_save_video_click)
        video_secondary_action_row.add_widget(self.clear_video_btn)
        video_secondary_action_row.add_widget(self.done_video_btn)
        
        # ScrollView for options
        scroll_view = ScrollView(size_hint=(1, 0.42))
        scroll_view.add_widget(grid)
        main_layout.add_widget(scroll_view)
        main_layout.add_widget(self.video_list_container)
        main_layout.add_widget(video_action_row)
        main_layout.add_widget(video_secondary_action_row)
        
        # Back button
        back_btn = Button(
            text="← BACK TO MENU",
            size_hint_y=None,
            height=50,
            background_normal="",
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1),
            font_size=16,
            bold=True
        )
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
        self.selected_video = None
        self.selected_operation = 'trim'
        
        # Refresh initial list (use local backend module)
        self.refresh_videos()
    
    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
    
    def on_option_press(self, operation, option_text):
        self.selected_operation = operation
        self.video_subtitle.text = f"Selected option: {option_text}"
        popup = Popup(
            title='Option Selected',
            content=Label(text=f'Operation set to: {option_text}'),
            size_hint=(0.6, 0.3)
        )
        popup.open()

    def open_filechooser_upload(self, file_type='video'):
        fc = FileChooserListView(path='.', filters=['*.mp4','*.avi','*.mov','*.mkv'])
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(fc)
        btn_layout = BoxLayout(size_hint_y=None, height=40)
        select_btn = Button(text='Upload', size_hint_x=0.5)
        cancel_btn = Button(text='Cancel', size_hint_x=0.5)

        def do_upload(instance):
            if fc.selection:
                filepath = fc.selection[0]
                popup.dismiss()
                self.upload_file_to_api(filepath, file_type)

        def do_cancel(instance):
            popup.dismiss()

        select_btn.bind(on_press=do_upload)
        cancel_btn.bind(on_press=do_cancel)
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        popup_layout.add_widget(btn_layout)
        popup = Popup(title='Select video to upload', content=popup_layout, size_hint=(0.9, 0.9))
        popup.open()

    def upload_file_to_api(self, filepath, file_type='video'):
        try:
            if file_type == 'video':
                data = bm.upload_video(filepath)
            else:
                data = bm.upload_photo(filepath)
            if data.get('success'):
                popup = Popup(title='Upload Success', content=Label(text=data.get('message', 'Uploaded')), size_hint=(0.6,0.3))
                popup.open()
                if file_type == 'video':
                    self.refresh_videos()
            else:
                popup = Popup(title='Upload Error', content=Label(text=str(data.get('error', 'upload failed'))), size_hint=(0.8,0.4))
                popup.open()
        except Exception as e:
            popup = Popup(title='Upload Exception', content=Label(text=str(e)), size_hint=(0.8,0.4))
            popup.open()

    def refresh_videos(self):
        try:
            data = bm.list_videos()
            videos = data.get('videos', [])
            # Update top bar with newest videos
            self.video_top_bar.clear_widgets()
            for v in videos[:8]:
                fn = v.get('filename', '')
                btn = Button(text=fn, size_hint_x=None, width=140, halign='left', color=(1,1,1,1))
                btn.bind(on_press=lambda inst, fn=fn: self.select_video(fn))
                self.video_top_bar.add_widget(btn)

            # Update list below as well
            self.video_list_grid.clear_widgets()
            self.video_list_label.text = f'Uploaded Videos: ({len(videos)})'
            for v in videos:
                row = BoxLayout(size_hint_y=None, height=36)
                name = Label(text=v.get('filename', ''), size_hint_x=0.75, color=(1,1,1,1), halign='left')
                size_label = Label(text=self._format_size(v.get('size', 0)), size_hint_x=0.25, color=(1,1,1,1))
                row.bind(on_touch_down=lambda x, fn=v.get('filename'): self.select_video(fn))
                row.add_widget(name)
                row.add_widget(size_label)
                self.video_list_grid.add_widget(row)
        except Exception as e:
            self.video_list_label.text = 'Uploaded Videos: (error)'

    def _format_size(self, size_bytes):
        try:
            size = float(size_bytes)
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} PB"
        except Exception:
            return '0 B'
    
    def select_video(self, filename):
        self.selected_video = filename
        try:
            # hide subtitle when a video is selected
            self.video_subtitle.text = ''
        except Exception:
            pass
    
    def on_process_video_click(self, instance):
        if self.selected_video:
            self.process_video_api(self.selected_video, self.selected_operation)
        else:
            popup = Popup(title='Info', content=Label(text='Please select a video first'), size_hint=(0.6,0.3))
            popup.open()
    
    def on_download_video_click(self, instance):
        if self.selected_video:
            self.download_file_api(self.selected_video, 'video')
        else:
            popup = Popup(title='Info', content=Label(text='Please select a video first'), size_hint=(0.6,0.3))
            popup.open()

    def process_video_api(self, filename, operation='trim'):
        try:
            resp = bm.process_video(filename, operation)
            if resp.get('success'):
                popup = Popup(title='Process Started', content=Label(text='Video processing completed.'), size_hint=(0.6,0.3))
                popup.open()
                self.refresh_videos()
            else:
                popup = Popup(title='Process Error', content=Label(text=str(resp.get('error', resp))), size_hint=(0.8,0.4))
                popup.open()
        except Exception as e:
            popup = Popup(title='Process Exception', content=Label(text=str(e)), size_hint=(0.8,0.4))
            popup.open()

    def on_save_video_click(self, instance):
        if self.selected_video:
            self.save_media_api(self.selected_video, 'video')
        else:
            popup = Popup(title='Info', content=Label(text='Please select a video to save'), size_hint=(0.6,0.3))
            popup.open()

    def on_clear_videos_click(self, instance):
        self.selected_video = None
        response = bm.clear_media('video')
        if response.get('success'):
            self.video_top_bar.clear_widgets()
            self.video_list_grid.clear_widgets()
            self.video_list_label.text = f"Uploaded Videos: (cleared {response.get('removed', 0)})"
            self.video_subtitle.text = 'Select a video editing option'
            return

        popup = Popup(
            title='Clear Error',
            content=Label(text=str(response.get('error', 'clear failed'))),
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def download_file_api(self, filename, file_type='video'):
        save_dir = os.path.join(os.path.dirname(__file__), '..', 'downloads')
        response = bm.download_media(file_type, filename, save_dir)
        if response.get('success'):
            popup = Popup(title='Downloaded', content=Label(text=f"Saved to {response.get('path')}"), size_hint=(0.8, 0.4))
            popup.open()
            return

        popup = Popup(title='Download Error', content=Label(text=str(response.get('error', 'download failed'))), size_hint=(0.8, 0.4))
        popup.open()

    def save_media_api(self, filename, media='video'):
        response = bm.save_media(media, filename)
        if response.get('success'):
            popup = Popup(
                title='Saved',
                content=Label(text=f"Saved as {response.get('saved_filename')}."),
                size_hint=(0.7, 0.3)
            )
            popup.open()
            self.refresh_videos()
            return

        popup = Popup(title='Save Error', content=Label(text=str(response.get('error', 'save failed'))), size_hint=(0.8, 0.4))
        popup.open()
    
    def go_back(self, instance):
        print("Going back to main menu...")
        self.manager.current = 'index'
