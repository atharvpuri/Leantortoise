

import os
import shutil
import tempfile
import hashlib
import time
import ctypes


SUSPICIOUS_EXTENSIONS = ['.exe', '.bat', '.scr', '.vbs', '.js', '.jar', '.ps1', '.cmd']
SUSPICIOUS_KEYWORDS = ['virus', 'trojan', 'hacktool', 'keylogger', 'backdoor', 'spyware']
MAX_SUSPICIOUS_SIZE_MB = 50  


JUNK_PATHS = [
    tempfile.gettempdir(),
    os.path.expanduser("~\\AppData\\Local\\Temp"),
    os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Recent"),
]

def log(msg):
    print(f"[Leantortoise] {msg}")


def count_files(folder_path):
    total = 0
    for _, _, files in os.walk(folder_path):
        total += len(files)
    return total


def scan_folder(folder_path, progress_callback=None, result_callback=None):
    total_files = count_files(folder_path)
    scanned = 0
    found_files = []
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            scanned += 1
            
            try:
                if is_suspicious(file_path):
                    found_files.append(file_path)
            except Exception as e:
                log(f"Error scanning {file_path}: {e}")

            if progress_callback:
                percent = int((scanned / total_files) * 100)
                progress_callback(percent, file_path)

    if result_callback:
        if found_files:
            result_callback("danger", found_files)
        else:
            result_callback("clean", [])

    return found_files


def is_suspicious(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    name = os.path.basename(file_path).lower()
    size_mb = os.path.getsize(file_path) / (1024 * 1024)


    if ext in SUSPICIOUS_EXTENSIONS and size_mb > MAX_SUSPICIOUS_SIZE_MB:
        return True


    if any(keyword in name for keyword in SUSPICIOUS_KEYWORDS):
        return True

 
    try:
        with open(file_path, 'rb') as f:
            content = f.read(4096)  
            for keyword in SUSPICIOUS_KEYWORDS:
                if keyword.encode() in content:
                    return True
    except Exception as e:
        log(f"Skipped reading {file_path}: {e}")

    return False


def clean_junk():
    deleted_files = []

    for path in JUNK_PATHS:
        if not os.path.exists(path):
            continue

        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    deleted_files.append(file_path)
                except Exception:
                    pass
            for d in dirs:
                dir_path = os.path.join(root, d)
                try:
                    shutil.rmtree(dir_path)
                    deleted_files.append(dir_path)
                except Exception:
                    pass

    return deleted_files


def delete_files(file_list):
    deleted = []
    for file in file_list:
        try:
            os.remove(file)
            deleted.append(file)
            log(f"Deleted: {file}")
        except Exception as e:
            log(f"Failed to delete {file}: {e}")
    return deleted


def notify_user(title, message):
    try:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)
    except:
        pass
