
import os
import psutil
import tkinter as tk
from tkinter import filedialog, messagebox
from send2trash import send2trash
import matplotlib.pyplot as plt

# -------- SYSTEM STATS --------
def get_stats():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return cpu, ram, disk

# -------- RECOMMENDATIONS --------
def get_recommendations(cpu, ram, disk):
    rec = []

    if cpu > 75:
        rec.append("⚡ Close heavy apps (CPU high)")
    if ram > 80:
        rec.append("🧠 Free RAM (close browser tabs)")
    if disk > 85:
        rec.append("💾 Clean disk space (Downloads/Desktop)")

    if not rec:
        rec.append("🟢 System is healthy")

    return "\n".join(rec)

# -------- CLEAN DESKTOP --------
def clean_desktop():
    desktop = f"C:/Users/{os.getlogin()}/Desktop"

    files = os.listdir(desktop)

    if len(files) == 0:
        messagebox.showinfo("Cleaner", "Desktop is already clean 🟢")
        return

    confirm = messagebox.askyesno(
        "Confirm",
        f"Move {len(files)} files from Desktop to Recycle Bin?"
    )

    if not confirm:
        return

    for f in files:
        path = os.path.join(desktop, f)
        try:
            send2trash(path)
        except:
            pass

    messagebox.showinfo("Done", "Desktop cleaned 🧹")

# -------- CLEAN CUSTOM FOLDER --------
def clean_custom_folder():
    folder = filedialog.askdirectory()

    if not folder:
        return

    files = os.listdir(folder)

    if len(files) == 0:
        messagebox.showinfo("Cleaner", "Folder is empty 🟢")
        return

    confirm = messagebox.askyesno(
        "Confirm",
        f"Move {len(files)} files to Recycle Bin?"
    )

    if not confirm:
        return

    for f in files:
        path = os.path.join(folder, f)
        try:
            send2trash(path)
        except:
            pass

    messagebox.showinfo("Done", "Folder cleaned 🧹")

# -------- GRAPH --------
def show_graph():
    cpu, ram, disk = get_stats()

    labels = ["CPU", "RAM", "DISK"]
    values = [cpu, ram, disk]

    plt.figure("System Usage")
    plt.bar(labels, values)
    plt.title("PC Load Analysis")
    plt.ylabel("% Usage")
    plt.ylim(0, 100)
    plt.show()

# -------- SYSTEM INFO --------
def show_info():
    cpu, ram, disk = get_stats()

    rec = get_recommendations(cpu, ram, disk)

    messagebox.showinfo(
        "System Info",
        f"CPU: {cpu}%\nRAM: {ram}%\nDisk: {disk}%\n\n{rec}"
    )

# -------- GUI --------
app = tk.Tk()
app.title("Lux-8 System Optimizer PRO")
app.geometry("400x350")

title = tk.Label(app, text="🧠 System Optimizer PRO", font=("Arial", 14))
title.pack(pady=10)

tk.Button(app, text="System Info + Tips", command=show_info).pack(pady=5)

tk.Button(app, text="Show Usage Graph 📊", command=show_graph).pack(pady=5)

tk.Button(app, text="Clean Desktop 🧹", command=clean_desktop).pack(pady=5)

tk.Button(app, text="Clean Custom Folder 📁", command=clean_custom_folder).pack(pady=5)

tk.Button(app, text="Exit", command=app.quit).pack(pady=10)

app.mainloop()