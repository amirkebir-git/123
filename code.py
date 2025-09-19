import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import requests
import threading
import time
import pygame
from io import BytesIO

# پخش موسیقی
def play_music(url):
    pygame.mixer.init()
    response = requests.get(url)
    music_data = BytesIO(response.content)
    pygame.mixer.music.load(music_data)
    pygame.mixer.music.play()

# نمایش متن داخلی
def show_internal_text(root, url):
    response = requests.get(url)
    text = response.text
    text_widget = ScrolledText(root, wrap=tk.WORD, bg="black", fg="white", font=("Arial", 14))
    text_widget.pack(expand=True, fill=tk.BOTH)
    text_widget.insert(tk.END, text)
    text_widget.configure(state='disabled')

# انیمیشن متن اولیه
def animate_text(label, root, internal_text_url, music_url):
    threading.Thread(target=play_music, args=(music_url,), daemon=True).start()
    time.sleep(2)
    for i in range(20, 0, -1):
        label.config(font=("Arial", i*3))
        time.sleep(0.05)
    label.destroy()
    show_internal_text(root, internal_text_url)

def main():
    root = tk.Tk()
    root.title("Nickel Server")
    root.geometry("800x600")
    root.configure(bg="black")

    text_label = tk.Label(root, text="تیم نویسنده نیکل سرور", fg="red", bg="black", font=("Arial", 60))
    text_label.pack(expand=True)

    internal_text_url = "https://raw.githubusercontent.com/amirkebir-git/123/refs/heads/main/te.txt"
    music_url = "https://github.com/amirkebir-git/123/raw/refs/heads/main/music%201.mp3"

    threading.Thread(target=animate_text, args=(text_label, root, internal_text_url, music_url), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()
