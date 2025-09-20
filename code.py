import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import threading
import time
import math
import json
import base64
import random
import smtplib

# --- اطلاعات GitHub ---
GITHUB_TOKEN = "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"
REPO_OWNER = "amirkebir-git"
REPO_NAME = "user"
FILE_PATH = "user.txt"

# --- توابع GitHub ---
def read_github_file():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        content = r.json()['content']
        decoded = base64.b64decode(content).decode()
        try:
            return json.loads(decoded)
        except:
            return []
    else:
        return []

def update_github_file(new_data, message="Update users"):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        messagebox.showerror("خطا", "خطا در دریافت SHA فایل GitHub")
        return False
    sha = r.json()['sha']
    content = base64.b64encode(json.dumps(new_data).encode()).decode()
    data = {"message": message, "content": content, "sha": sha}
    r = requests.put(url, headers=headers, json=data)
    return r.status_code in [200, 201]

# --- توابع ایمیل ---
def send_verification_email(to_email):
    sender = "nickelproject6432@gmail.com"
    password = "xklk nvzx anyg epfc"
    code = str(random.randint(100000, 999999))
    subject = "Verification Code"
    body = f"Your verification code is: {code}"
    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, to_email, message)
    return code

# --- ثبت‌نام و ورود ---
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    email = entry_email.get()
    users = read_github_file()
    
    for u in users:
        if u.get('username') == username:
            messagebox.showerror("خطا", "Username قبلا ثبت شده")
            return
        if u.get('email') == email:
            messagebox.showerror("خطا", "Email قبلا ثبت شده")
            return
    
    code = send_verification_email(email)
    code_input = simpledialog.askstring("Email Verification", f"Enter the code sent to {email}:")
    if code_input != code:
        messagebox.showerror("خطا", "کد تایید ایمیل اشتباه است")
        return
    
    users.append({"username": username, "password": password, "email": email})
    if update_github_file(users, "Add new user"):
        messagebox.showinfo("موفق", "ثبت‌نام با موفقیت انجام شد")
        login_frame.destroy()
        start_check()
    else:
        messagebox.showerror("خطا", "ثبت‌نام موفقیت‌آمیز نبود")

def login_user():
    username = entry_username.get()
    password = entry_password.get()
    users = read_github_file()
    
    for u in users:
        if u.get('username') == username and u.get('password') == password:
            messagebox.showinfo("موفق", "ورود موفقیت‌آمیز بود")
            login_frame.destroy()
            start_check()
            return
    messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است")

# --- ساخت فرم Tkinter ثبت‌نام و ورود ---
root = tk.Tk()
root.title("Nickel Server")
root.configure(bg="white")
root.attributes("-fullscreen", True)

login_frame = tk.Frame(root, bg="white")
login_frame.pack(expand=True)

tk.Label(login_frame, text="Username:", font=("B Titr", 20), bg="white").grid(row=0, column=0, pady=10)
entry_username = tk.Entry(login_frame, font=("B Titr", 20))
entry_username.grid(row=0, column=1, pady=10)

tk.Label(login_frame, text="Password:", font=("B Titr", 20), bg="white").grid(row=1, column=0, pady=10)
entry_password = tk.Entry(login_frame, font=("B Titr", 20), show="*")
entry_password.grid(row=1, column=1, pady=10)

tk.Label(login_frame, text="Email:", font=("B Titr", 20), bg="white").grid(row=2, column=0, pady=10)
entry_email = tk.Entry(login_frame, font=("B Titr", 20))
entry_email.grid(row=2, column=1, pady=10)

tk.Button(login_frame, text="Register", font=("B Titr", 20), command=register_user, bg="green", fg="white").grid(row=3, column=0, pady=20)
tk.Button(login_frame, text="Login", font=("B Titr", 20), command=login_user, bg="blue", fg="white").grid(row=3, column=1, pady=20)

# --- ادامه کد اصلی (انیمیشن و چک اینترنت) ---
status_label = tk.Label(root, text="...", font=("B Titr", 30, "bold"), bg="white")
status_label.pack(pady=50)

canvas = tk.Canvas(root, width=200, height=200, bg="white", highlightthickness=0)
canvas.pack()

# --- توابع اصلی ---
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

def update_status(msg):
    status_label.config(text=msg)

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

def start_check():
    threading.Thread(target=run_process).start()
    animate_circle()

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

def show_final_message():
    for widget in root.winfo_children():
        widget.destroy()
    text = """باسلام
نیکل سرور در حال آپدیت میباشد

شنبه ۲۹ شهریور ۱۴۰۴ شمسی
20 September 2025 میلادی
۲۷ ربیع الاول ۱۴۴۷ قمری
"""
    final_label = tk.Label(root, text=text, font=("B Titr", 36, "bold"), justify="center", fg="darkred", bg="white")
    final_label.pack(expand=True)

    exit_button = tk.Button(root, text="خروج", font=("B Titr", 24, "bold"), command=root.destroy, bg="red", fg="white")
    exit_button.pack(pady=50)

root.mainloop()
