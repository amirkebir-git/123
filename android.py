import threading
import time
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock, mainthread
from kivy.core.audio import SoundLoader

INTERNAL_TEXT_URL = "https://raw.githubusercontent.com/amirkebir-git/123/refs/heads/main/te.txt"
MUSIC_URL = "https://github.com/amirkebir-git/123/raw/refs/heads/main/music%201.mp3"

class AnimatedTextApp(App):
    def build(self):
        self.root_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.text_label = Label(text="Nickel Server Team", font_size=60, color=(1,0,0,1))
        self.root_layout.add_widget(self.text_label)

        # Start animation in thread
        threading.Thread(target=self.animate_text, daemon=True).start()

        return self.root_layout

    def animate_text(self):
        # Play music
        threading.Thread(target=self.play_music, daemon=True).start()
        time.sleep(2)  # initial delay

        # Animate shrinking text
        for size in range(60, 0, -3):
            Clock.schedule_once(lambda dt, s=size: self.text_label.setter('font_size')(self.text_label, s))
            time.sleep(0.05)

        # Remove label and show text from URL
        Clock.schedule_once(lambda dt: self.root_layout.remove_widget(self.text_label))
        self.show_internal_text()

    def play_music(self):
        sound = SoundLoader.load(MUSIC_URL)
        if sound:
            sound.play()

    @mainthread
    def show_internal_text(self):
        try:
            response = requests.get(INTERNAL_TEXT_URL)
            text = response.text
        except:
            text = "Error fetching text from the internet!"

        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, padding=10)
        grid.bind(minimum_height=grid.setter('height'))

        label = Label(text=text, size_hint_y=None, font_size=20, color=(1,1,1,1), text_size=(self.root_layout.width-40, None))
        label.bind(texture_size=label.setter('size'))
        grid.add_widget(label)

        scroll.add_widget(grid)
        self.root_layout.add_widget(scroll)

if __name__ == "__main__":
    AnimatedTextApp().run()
