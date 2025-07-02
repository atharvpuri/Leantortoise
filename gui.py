# gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkbootstrap import Style
import threading
import main
import time
import ctypes
import os

class LeanTortoiseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Leantortoise - Lightweight File Scanner")
        self.root.geometry("900x600")
        self.root.configure(bg="#0f0f0f")
        self.root.minsize(800, 500)
        self.root.attributes('-alpha', 0.0)  # Start transparent
        self.fade_in()

        self.enable_blur()  # Windows 10+ only

        self.selected_folder = tk.StringVar()
        self.suspicious_files = []

        self.style = Style("darkly")  # Use ttkbootstrap dark theme
        self.build_ui()

    def fade_in(self):
        for i in range(0, 11):
            alpha = i / 10
            self.root.attributes('-alpha', alpha)
            self.root.update()
            time.sleep(0.03)

    def enable_blur(self):
        try:
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            accent = ctypes.Structure._fields_ = [
                ("AccentState", ctypes.c_int),
                ("AccentFlags", ctypes.c_int),
                ("GradientColor", ctypes.c_int),
                ("AnimationId", ctypes.c_int)
            ]
            accent_policy = ctypes.Structure()
            accent_policy.AccentState = 3  # ACCENT_ENABLE_BLURBEHIND
            accent_policy.GradientColor = 0x01000000  # Transparent
            data = ctypes.pointer(accent_policy)
            size = ctypes.sizeof(accent_policy)
            ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.byref(data))
        except:
            pass  # No blur on non-Windows or older OS

    def build_ui(self):
        # App Title
        title = ttk.Label(self.root, text="🛡️ Leantortoise Scanner", font=("Segoe UI", 24, "bold"), foreground="#00FFAA", background="#0f0f0f")
        title.pack(pady=(20, 10))

        # Select Folder Button
        folder_btn = ttk.Button(self.root, text="📁 Select Folder", style="success.TButton", command=self.select_folder)
        folder_btn.pack(pady=10)

        self.path_label = ttk.Label(self.root, text="", font=("Segoe UI", 10), background="#0f0f0f", foreground="#ccc")
        self.path_label.pack()

        # Scan & Delete Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=15)

        self.scan_btn = ttk.Button(btn_frame, text="🔍 Start Scan", style="info.TButton", command=self.start_scan_thread)
        self.scan_btn.grid(row=0, column=0, padx=15)

        self.delete_btn = ttk.Button(btn_frame, text="❌ Delete Suspicious", style="danger.TButton", command=self.delete_files)
        self.delete_btn.grid(row=0, column=1, padx=15)

        self.junk_btn = ttk.Button(btn_frame, text="🧹 Clean Junk", style="secondary.TButton", command=self.clean_junk)
        self.junk_btn.grid(row=0, column=2, padx=15)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=600, mode='determinate', style="info.Horizontal.TProgressbar")
        self.progress.pack(pady=15)

        # Log box
        self.log_box = tk.Text(self.root, height=15, width=100, bg="#111", fg="#0f0", font=("Consolas", 11), borderwidth=0)
        self.log_box.pack(padx=30, pady=(0, 20))

        # Exit button
        exit_btn = ttk.Button(self.root, text="⏹ Exit", style="light.TButton", command=self.root.quit)
        exit_btn.pack(pady=(0, 10))

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder.set(folder)
            self.path_label.config(text=folder)

    def start_scan_thread(self):
        if not self.selected_folder.get():
            messagebox.showwarning("No folder selected", "Please select a folder.")
            return

        self.log_box.delete(1.0, tk.END)
        self.progress['value'] = 0
        self.suspicious_files.clear()

        threading.Thread(target=self.scan_files, daemon=True).start()

    def scan_files(self):
        def progress_callback(percent, file_path):
            self.progress['value'] = percent
            self.log_box.insert(tk.END, f"Scanned: {file_path}\n")
            self.log_box.see(tk.END)

        def result_callback(result_type, files):
            if result_type == "clean":
                messagebox.showinfo("Scan Result", "✅ No suspicious files found.")
            elif result_type == "danger":
                msg = f"⚠️ Found {len(files)} suspicious files!\n\n" + "\n".join(files[:5]) + ("\n..." if len(files) > 5 else "")
                messagebox.showerror("Suspicious Files Detected", msg)

        self.log_box.insert(tk.END, "🔎 Starting scan...\n")
        self.suspicious_files = main.scan_folder(self.selected_folder.get(), progress_callback, result_callback)

    def delete_files(self):
        if not self.suspicious_files:
            messagebox.showinfo("Nothing to delete", "No suspicious files to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Delete {len(self.suspicious_files)} suspicious files?")
        if confirm:
            deleted = main.delete_files(self.suspicious_files)
            self.log_box.insert(tk.END, f"\n🧹 Deleted {len(deleted)} files.\n")
            self.suspicious_files.clear()

    def clean_junk(self):
        deleted = main.clean_junk()
        messagebox.showinfo("Junk Cleaner", f"🧹 Deleted {len(deleted)} junk files.")
        self.log_box.insert(tk.END, f"\n🧹 Cleaned {len(deleted)} junk files.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = LeanTortoiseApp(root)
    root.mainloop()
