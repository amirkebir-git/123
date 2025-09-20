import tkinter as tk
import requests
import threading
import time
from tkinter import messagebox
from datetime import datetime

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

def run_process():
    update_status("در حال بررسی اینترنت ...")
    time.sleep(2)
    if not check_connection():
        update_status("خطا در اتصال به اینترنت")
        return

    update_status("در حال متصل شدن به سرور ...")
    time.sleep(2)
    if not check_server():
        update_status("خطا در اتصال به سرور")
        return

    update_status("در حال اجرا ...")
    time.sleep(5)
    show_final_message()

def update_status(msg):
    status_label.config(text=msg)

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
        font=("B Titr", 16, "bold"),
        justify="center"
    )
    final_label.pack(pady=50)

    exit_button = tk.Button(root, text="خروج", font=("B Titr", 14, "bold"), command=root.destroy)
    exit_button.pack(pady=20)

# ساخت پنجره اصلی
root = tk.Tk()
root.title("Nickel Server")
root.geometry("800x500")

status_label = tk.Label(root, text="...", font=("B Titr", 14))
status_label.pack(pady=200)

start_check()

root.mainloop()
