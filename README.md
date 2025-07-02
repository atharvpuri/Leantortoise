📄 README.md (for your GitHub repo)

# Leantortoise

Leantortoise is a lightweight antivirus and junk cleaner built using Python. It scans Windows directories for suspicious files and can clean common junk locations like temp folders, caches, and logs.

## Features

- Lightweight Python-based scanner
- Detects suspicious files based on:
  - File extension
  - File size anomalies
  - Malware keywords in filenames or content
- Junk cleaner to remove temporary files and logs
- Clean and modern user interface with:
  - Adjustable window size
  - Blur effect on Windows 10+
  - Smooth fade-in animation
  - Progress bar and logs
- No background bloat, runs only when needed

## How to Use

1. Install Python 3.9 or higher.
2. Install required packages:

pip install ttkbootstrap



3. Run the application:

python gui.py



4. Use the interface to:
- Select a folder to scan
- View real-time scan progress and logs
- Delete suspicious files
- Clean junk files from the system

## Folder Structure

Leantortoise/
├── gui.py # Graphical interface
├── main.py # Core logic for scanning and cleaning
├── README.md # This file
├── requirements.txt # Dependencies (optional)


## Requirements

- Python 3.9+
- ttkbootstrap



This project is licensed under the MIT License.
✅ Optional: requirements.txt
txt
Copy
Edit
ttkbootstrap
