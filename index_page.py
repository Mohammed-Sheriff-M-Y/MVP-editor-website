# Index Page - Main Menu
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, Line
import os


class IndexPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Root layout
        root = BoxLayout(orientation="horizontal", padding=30, spacing=20)

        # Light grey background
        with root.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.bg = Rectangle(size=root.size, pos=root.pos)

        root.bind(size=self.update_bg, pos=self.update_bg)

        # -------- Left Side (Logo) --------
        left = BoxLayout(
            orientation="vertical",
            size_hint=(0.45, 1),
            padding=20,
            spacing=15
        )

        # Left side background
        with left.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.left_bg = Rectangle(size=left.size, pos=left.pos)
        
        left.bind(size=self.update_left_bg, pos=self.update_left_bg)

        # Logo container
        logo_container = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20,
            size_hint_y=0.7
        )

        # Create a round logo container and place image or emoji inside
        from kivy.uix.widget import Widget

        logo_widget = Widget(size_hint_y=0.7)
        with logo_widget.canvas.before:
            Color(1, 1, 1, 1)
            logo_ellipse = Line(circle=(0, 0, 0), width=0)

        def _update_logo_canvas(inst, *a):
            logo_widget.canvas.before.clear()
            with logo_widget.canvas.before:
                Color(1, 1, 1, 1)
                from kivy.graphics import Ellipse
                Ellipse(pos=inst.pos, size=inst.size)

        logo_widget.bind(pos=_update_logo_canvas, size=_update_logo_canvas)

        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
        
        logo_loaded = False
        if os.path.exists(logo_path):
            try:
                img = Image(source=logo_path)
                img.size_hint = (None, None)
                img.size = (logo_widget.width * 0.8 if logo_widget.width else 180, logo_widget.height * 0.8 if logo_widget.height else 180)
                logo_widget.add_widget(img)
                logo_container.add_widget(logo_widget)
                logo_loaded = True
                
                def _resize_img(inst, *a):
                    if img in logo_widget.children:
                        img.size = (inst.width * 0.8, inst.height * 0.8)
                        img.pos = (inst.x + (inst.width - img.width) / 2, inst.y + (inst.height - img.height) / 2)
                
                logo_widget.bind(size=_resize_img, pos=_resize_img)
            except Exception as e:
                print(f"Error loading logo image: {e}")
        
        if not logo_loaded:
            emoji = Label(text="🎬", font_size=72, color=(0, 0, 0, 1), size_hint=(1, 1))
            logo_widget.add_widget(emoji)
            logo_container.add_widget(logo_widget)
            
            def _center_emoji(inst, *a):
                if emoji in logo_widget.children:
                    emoji.center = inst.center
            
            logo_widget.bind(size=_center_emoji, pos=_center_emoji)

        left_title = Label(
            text="MVP\nEDITOR",
            font_size=24,
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=0.3
        )
        logo_container.add_widget(left_title)

        left.add_widget(logo_container)

        # Bottom text on left
        bottom_text = Label(
            text="Friendly Editing\nTools",
            font_size=12,
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=0.3
        )
        left.add_widget(bottom_text)

        # -------- Right Side (Menu) --------
        right = BoxLayout(
            orientation="vertical",
            size_hint=(0.55, 1),
            padding=40,
            spacing=30
        )

        right.add_widget(Label(
            text="Welcome",
            font_size=32,
            color=(1, 1, 1, 1),
            bold=True
        ))

        right.add_widget(Label(
            text="Select an editing mode",
            font_size=16,
            color=(1, 1, 1, 1)
        ))

        btn_photo = Button(
            text="PHOTO EDITING",
            size_hint=(1, None),
            height=60,
            background_normal="",
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )

        btn_video = Button(
            text="VIDEO EDITING",
            size_hint=(1, None),
            height=60,
            background_normal="",
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )

        btn_photo.bind(on_press=self.go_to_photo)
        btn_video.bind(on_press=self.go_to_video)

        right.add_widget(btn_photo)
        right.add_widget(btn_video)

        root.add_widget(left)
        root.add_widget(right)

        self.add_widget(root)

    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def update_left_bg(self, *args):
        self.left_bg.size = self.size
        self.left_bg.pos = self.pos

    def go_to_photo(self, instance):
        print("Opening Photo Editing page...")
        self.manager.current = 'photo'

    def go_to_video(self, instance):
        print("Opening Video Editing page...")
        self.manager.current = 'video'
