import tkinter as tk
from tkinter import messagebox
import requests
import threading
import time
import math

def check_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except:
        return False

def check_server():
    try:
        requests.get("https://nickelserver.sbs/", timeout=5)
        return True
    except:
        return False

def start_check():
    threading.Thread(target=run_process).start()
    animate_circle()  # شروع انیمیشن

def run_process():
    update_status("در حال بررسی اینترنت ...")
    time.sleep(2)
    if not check_connection():
        update_status("❌ خطا در اتصال به اینترنت")
        messagebox.showerror("خطا", "اتصال به اینترنت برقرار نشد ❌")
        stop_animation()
        return

    update_status("در حال متصل شدن به سرور ...")
    time.sleep(2)
    if not check_server():
        update_status("❌ خطا در اتصال به سرور")
        messagebox.showerror("خطا", "ارتباط با سرور Nickel برقرار نشد ❌")
        stop_animation()
        return

    update_status("در حال اجرا ...")
    time.sleep(5)
    stop_animation()
    show_final_message()

def update_status(msg):
    status_label.config(text=msg)

# --- انیمیشن دایره ---
angle = 0
running_animation = True
def animate_circle():
    global angle, running_animation
    if not running_animation:
        return
    canvas.delete("all")
    x = 50 * math.cos(math.radians(angle)) + 100
    y = 50 * math.sin(math.radians(angle)) + 100
    canvas.create_oval(x-15, y-15, x+15, y+15, fill="blue")
    angle += 10
    root.after(50, animate_circle)

def stop_animation():
    global running_animation
    running_animation = False
    canvas.delete("all")

# --- پیام پایانی ---
def show_final_message():
    for widget in root.winfo_children():
        widget.destroy()

    text = """باسلام
نیکل سرور در حال آپدیت میباشد

شنبه ۲۹ شهریور ۱۴۰۴ شمسی
20 September 2025 میلادی
۲۷ ربیع الاول ۱۴۴۷ قمری
"""
    final_label = tk.Label(
        root,
        text=text,
        font=("B Titr", 36, "bold"),
        justify="center",
        fg="darkred",
        bg="white"
    )
    final_label.pack(expand=True)

    exit_button = tk.Button(root, text="خروج", font=("B Titr", 24, "bold"), command=root.destroy, bg="red", fg="white")
    exit_button.pack(pady=50)

# --- ساخت پنجره اصلی ---
root = tk.Tk()
root.title("Nickel Server")
root.configure(bg="white")
root.attributes("-fullscreen", True)  # فول‌اسکرین واقعی

status_label = tk.Label(root, text="...", font=("B Titr", 30, "bold"), bg="white")
status_label.pack(pady=50)

canvas = tk.Canvas(root, width=200, height=200, bg="white", highlightthickness=0)
canvas.pack()

start_check()

root.mainloop()
