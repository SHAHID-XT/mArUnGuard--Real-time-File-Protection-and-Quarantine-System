# mArUnGuard — Real-time File Protection & Quarantine System

## Overview

**mArUnGuard** is a lightweight, background-running malware monitor for Windows that provides **real-time file protection**. It monitors selected folders, computes the SHA256 hash of every new or modified file, and checks it against a **large malicious hash database** stored locally in SQLite.

If a file matches a known malicious hash, it is **immediately quarantined** and access is restricted using Windows ACLs, while a **toast notification** alerts the user.

Key features:

* Real-time monitoring of selected directories.
* SHA256 hashing and comparison against a **massive hash database** (millions of entries).
* Automatic daily hash updates from [Abuse.ch SHA256 feed](https://bazaar.abuse.ch/export/txt/sha256/recent/).
* Safe quarantine system with `.mr` file renaming and ACL restrictions.
* Desktop notifications via Windows toast.
* Detailed logging of all actions with timestamps.
* Built-in **automatic elevation** to admin if required.

---

## Features

### 1. Real-time File Monitoring

* Uses Python `watchdog` to detect new and modified files.
* Efficient scanning using **SQLite queries** for rapid hash checks.

### 2. Malware Detection & Quarantine

* Detects malicious files using SHA256 hashes.
* Moves infected files to a dedicated `Quarantine` folder.
* Renames files to `.mr` extension for safety.
* Locks files using Windows `icacls` to prevent accidental access.

### 3. Notifications

* Desktop toast notifications alert users immediately when a file is quarantined.
* Custom icon support (`icon.png`) for better UX.
* Threaded notifications avoid blocking main monitoring process.

### 4. Logging

* Logs all events (safe scans, malicious detections, errors) in `logs/mArUnGuard.log`.
* Timestamps for all operations.
* Optionally review logs to see detailed file activity.

### 5. Automatic Hash Updates

* Downloads the latest malicious SHA256 hashes daily from Abuse.ch.
* Efficient batch insertion into SQLite for very large datasets (>1 million hashes).
* Avoids blocking the monitoring service during updates.

### 6. Admin Rights Handling

* Automatically elevates the script to admin using UAC if required.
* Necessary for moving files to quarantine and restricting access via ACLs.

---

## Installation

1. Clone or download the repository:

```bash
git clone https://github.com/SHAHID-XT/mArUnGuard--Real-time-File-Protection-and-Quarantine-System.git
cd mArUnGuard*
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

### Watched Paths

Edit the `WATCH_PATHS` list in `lib\configurations.py`:

```python
WATCH_PATHS = [
    r"C:\Users\Public",
    r"C:\Users",
]
```

You can add or remove directories you want to monitor.

### Ignored Paths

Some directories are ignored to prevent unnecessary scanning:

```python
IGNORED_PATHS = [
    r"C:\Windows",
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    appdata_env  # auto-detected AppData path
]
```

---

## Running the Script

Run directly with Python:

```bash
python main.py
```

* The script **auto-elevates** to admin if needed.
* Windows toast will confirm monitoring is active.
* Logs are saved in `logs/mArUnGuard.log`.

---

## Building to EXE

To distribute as a standalone Windows executable:

```bash
pyinstaller --onefile --icon=icon.png --name=mArUnGuard main.py
```

* Generates a single `mArUnGuard.exe`.
* Includes icon and runs without requiring Python installed on the target machine.

---

## File Quarantine

* All detected malicious files are moved to:

```text
C:\mArUnGuard\Quarantine
```

* Files are renamed to `.mr` extension.
* Access is blocked using Windows ACLs (`icacls`).
* Notifications alert the user about the quarantined file.

---

## Logging

* Logs all actions in `logs/mArUnGuard.log`.
* Example log entries:

```
2025-10-17 12:08:01,823 - INFO - Scanned safe file: C:\Users\moham\Documents\example.txt
2025-10-17 12:08:01,997 - WARNING - ⚠️ Malicious file detected: C:\Users\moham\Downloads\malware.exe
2025-10-17 12:08:01,998 - INFO - Quarantined file: C:\mArUnGuard\Quarantine\malware.mr
```

---

## Example Usage

```python
from main import mArUnGuard

guard = mArUnGuard()
guard.start()
```

* Runs the monitoring service.
* Automatically updates hash database and monitors files in the configured paths.

---

## Notes

* Designed for **Windows 10/11 only**.
* Requires **Python 3.10+**.
* Ensure **`icon.png`** is available in the same directory for toast notifications.
* `.mr` extension prevents execution of quarantined files.

---

## License

**Author:** Shahid-Xt
