# Photo Editing Page
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


class PhotoEditPage(Screen):
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
            text="PHOTO EDITING",
            font_size=28,
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=0.15
        )
        main_layout.add_widget(title)
        
        # Subtitle
        self.photo_subtitle = Label(
            text="Select an editing option",
            font_size=14,
            color=(1, 1, 1, 1),
            size_hint_y=0.1
        )
        main_layout.add_widget(self.photo_subtitle)
        
        # Grid layout for editing options
        # Showing label and top bar (display uploaded photos under subtitle)
        self.photo_top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        main_layout.add_widget(self.photo_top_bar)

        # Separate Add Photo button placed above the options grid
        add_photo_btn = Button(text='Add Photo', size_hint_y=None, height=50, background_normal='', background_color=(0.2,0.6,0.9,1), color=(1,1,1,1))
        add_photo_btn.bind(on_press=lambda inst: self.open_filechooser_upload('photo'))
        main_layout.add_widget(add_photo_btn)

        # Unified action button sizing
        ACTION_BTN_HEIGHT = 60
        OPTION_HEIGHT = 70

        grid = GridLayout(cols=3, spacing=15, padding=15, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        options = [
            ("Crop", "crop"),
            ("Rotate", "rotate"),
            ("Filters", "filters"),
            ("Brightness", "brightness"),
            ("Resize", "resize"),
            ("Export", "export"),
            ("Undo", "undo"),
            ("Redo", "redo"),
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
        
        # Photo list area
        self.photo_list_container = BoxLayout(orientation='vertical', size_hint_y=0.3)
        self.photo_list_label = Label(text='Uploaded Photos: (loading...)', size_hint_y=None, height=30, color=(1,1,1,1))
        self.photo_list_scroll = ScrollView()
        self.photo_list_grid = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        self.photo_list_grid.bind(minimum_height=self.photo_list_grid.setter('height'))
        self.photo_list_scroll.add_widget(self.photo_list_grid)
        self.photo_list_container.add_widget(self.photo_list_label)
        self.photo_list_container.add_widget(self.photo_list_scroll)
        
        # Process and Download buttons (single row) - match inner button height
        btn_layout = BoxLayout(size_hint_y=None, height=ACTION_BTN_HEIGHT + 10, spacing=10, padding=10)
        self.process_photo_btn = Button(text='Process', size_hint_x=0.5, size_hint_y=None, height=ACTION_BTN_HEIGHT, background_normal="", background_color=(0.2, 0.6, 0.9, 1), color=(1, 1, 1, 1))
        self.download_photo_btn = Button(text='Download', size_hint_x=0.5, size_hint_y=None, height=ACTION_BTN_HEIGHT, background_normal="", background_color=(0.2, 0.8, 0.4, 1), color=(1, 1, 1, 1))
        self.process_photo_btn.bind(on_press=self.on_process_photo_click)
        self.download_photo_btn.bind(on_press=self.on_download_photo_click)
        btn_layout.add_widget(self.process_photo_btn)
        btn_layout.add_widget(self.download_photo_btn)

        # Clear and Done buttons
        secondary_btn_layout = BoxLayout(size_hint_y=None, height=ACTION_BTN_HEIGHT + 10, spacing=10, padding=10)
        self.clear_photo_btn = Button(text='Clear', size_hint_x=0.5, size_hint_y=None, height=ACTION_BTN_HEIGHT, background_normal="", background_color=(0.7, 0.2, 0.2, 1), color=(1, 1, 1, 1))
        self.done_photo_btn = Button(text='Done', size_hint_x=0.5, size_hint_y=None, height=ACTION_BTN_HEIGHT, background_normal="", background_color=(0.3, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        self.clear_photo_btn.bind(on_press=self.on_clear_photos_click)
        self.done_photo_btn.bind(on_press=self.on_save_photo_click)
        secondary_btn_layout.add_widget(self.clear_photo_btn)
        secondary_btn_layout.add_widget(self.done_photo_btn)
        
        # ScrollView for options
        scroll_view = ScrollView(size_hint=(1, 0.5))
        scroll_view.add_widget(grid)
        main_layout.add_widget(scroll_view)
        main_layout.add_widget(self.photo_list_container)
        main_layout.add_widget(btn_layout)
        main_layout.add_widget(secondary_btn_layout)
        
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
        self.selected_photo = None
        self.selected_operation = 'rotate'
        
        # Refresh initial list (use local backend module)
        self.refresh_photos()
    
    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
    
    def on_option_press(self, operation, option_text):
        self.selected_operation = operation
        self.photo_subtitle.text = f"Selected option: {option_text}"
        popup = Popup(
            title='Option Selected',
            content=Label(text=f'Operation set to: {option_text}'),
            size_hint=(0.6, 0.3)
        )
        popup.open()

    def open_filechooser_upload(self, file_type='photo'):
        # file_type: 'photo' or 'video'
        fc = FileChooserListView(path='.', filters=['*.png', '*.jpg', '*.jpeg', '*.gif'] if file_type=='photo' else ['*.mp4','*.avi','*.mov','*.mkv'])
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
        popup = Popup(title='Select file to upload', content=popup_layout, size_hint=(0.9, 0.9))
        popup.open()

    def upload_file_to_api(self, filepath, file_type='photo'):
        try:
            if file_type == 'photo':
                data = bm.upload_photo(filepath)
            else:
                data = bm.upload_video(filepath)
            if data.get('success'):
                popup = Popup(title='Upload Success', content=Label(text=data.get('message', 'Uploaded')), size_hint=(0.6,0.3))
                popup.open()
                if file_type == 'photo':
                    self.refresh_photos()
            else:
                popup = Popup(title='Upload Error', content=Label(text=str(data.get('error', 'upload failed'))), size_hint=(0.8,0.4))
                popup.open()
        except Exception as e:
            popup = Popup(title='Upload Exception', content=Label(text=str(e)), size_hint=(0.8,0.4))
            popup.open()

    def refresh_photos(self):
        try:
            data = bm.list_photos()
            photos = data.get('photos', [])
            # Update top bar (show newest first)
            self.photo_top_bar.clear_widgets()
            for p in photos[:8]:
                fn = p.get('filename', '')
                btn = Button(text=fn, size_hint_x=None, width=140, halign='left', color=(1,1,1,1))
                btn.bind(on_press=lambda inst, fn=fn: self.select_photo(fn))
                self.photo_top_bar.add_widget(btn)

            # Update list below as well
            self.photo_list_grid.clear_widgets()
            self.photo_list_label.text = f'Uploaded Photos: ({len(photos)})'
            for p in photos:
                row = BoxLayout(size_hint_y=None, height=36)
                name = Label(text=p.get('filename', ''), size_hint_x=1, color=(1,1,1,1))
                row.bind(on_touch_down=lambda x, fn=p.get('filename'): self.select_photo(fn))
                row.add_widget(name)
                self.photo_list_grid.add_widget(row)
        except Exception as e:
            self.photo_list_label.text = 'Uploaded Photos: (error)'
    
    def select_photo(self, filename):
        self.selected_photo = filename
        try:
            # hide subtitle when a photo is selected
            self.photo_subtitle.text = ''
        except Exception:
            pass
    
    def on_process_photo_click(self, instance):
        if self.selected_photo:
            self.process_photo_api(self.selected_photo, self.selected_operation)
        else:
            popup = Popup(title='Info', content=Label(text='Please select a photo first'), size_hint=(0.6,0.3))
            popup.open()
    
    def on_download_photo_click(self, instance):
        if self.selected_photo:
            self.download_file_api(self.selected_photo, 'photo')
        else:
            popup = Popup(title='Info', content=Label(text='Please select a photo first'), size_hint=(0.6,0.3))
            popup.open()

    def process_photo_api(self, filename, operation='rotate'):
        try:
            resp = bm.process_photo(filename, operation)
            if resp.get('success'):
                popup = Popup(title='Process Started', content=Label(text='Processing completed.'), size_hint=(0.6,0.3))
                popup.open()
                # refresh list to show processed filenames
                self.refresh_photos()
            else:
                popup = Popup(title='Process Error', content=Label(text=str(resp.get('error', resp))), size_hint=(0.8,0.4))
                popup.open()
        except Exception as e:
            popup = Popup(title='Process Exception', content=Label(text=str(e)), size_hint=(0.8,0.4))
            popup.open()

    def on_save_photo_click(self, instance):
        if self.selected_photo:
            self.save_media_api(self.selected_photo, 'photo')
        else:
            popup = Popup(title='Info', content=Label(text='Please select a photo to save'), size_hint=(0.6,0.3))
            popup.open()

    def on_clear_photos_click(self, instance):
        self.selected_photo = None
        response = bm.clear_media('photo')
        if response.get('success'):
            self.photo_top_bar.clear_widgets()
            self.photo_list_grid.clear_widgets()
            self.photo_list_label.text = f"Uploaded Photos: (cleared {response.get('removed', 0)})"
            self.photo_subtitle.text = 'Select an editing option'
            return

        popup = Popup(
            title='Clear Error',
            content=Label(text=str(response.get('error', 'clear failed'))),
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def download_file_api(self, filename, file_type='photo'):
        save_dir = os.path.join(os.path.dirname(__file__), '..', 'downloads')
        response = bm.download_media(file_type, filename, save_dir)
        if response.get('success'):
            popup = Popup(title='Downloaded', content=Label(text=f"Saved to {response.get('path')}"), size_hint=(0.8, 0.4))
            popup.open()
            return

        popup = Popup(title='Download Error', content=Label(text=str(response.get('error', 'download failed'))), size_hint=(0.8, 0.4))
        popup.open()

    def save_media_api(self, filename, media='photo'):
        response = bm.save_media(media, filename)
        if response.get('success'):
            popup = Popup(
                title='Saved',
                content=Label(text=f"Saved as {response.get('saved_filename')}."),
                size_hint=(0.7, 0.3)
            )
            popup.open()
            self.refresh_photos()
            return

        popup = Popup(title='Save Error', content=Label(text=str(response.get('error', 'save failed'))), size_hint=(0.8, 0.4))
        popup.open()
    
    def go_back(self, instance):
        print("Going back to main menu...")
        self.manager.current = 'index'
