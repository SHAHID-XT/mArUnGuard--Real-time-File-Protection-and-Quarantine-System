
import warnings; warnings.filterwarnings('ignore')
import os
import sys
import hashlib
import requests
import sqlite3
import threading
import time
import logging
import shutil
from datetime import datetime, timezone
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from win10toast_click import ToastNotifier
from pathlib import Path
import os
import sys
import ctypes
import webbrowser

sys.stderr = open(os.devnull, 'w') #setup to hide upwated error by default


# Folders to watch by default
WATCH_PATHS = [
    r"C:\Users\Public",
    r"C:\Users",
]

appdata_env = str(os.environ.get("APPDATA")).replace("\\Roaming","").replace("\\Local","").replace("\\LocalLow","")

IGNORED_PATHS = [
    r"C:\Windows",
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    appdata_env
]

# Quarantine folder
QUARANTINE_PATH = r"C:\mArUnGuard\Quarantine"

# SQLite database file
DB_FILE = r"logs\malware_hashes.db"

# Hash feed source (daily updated)
HASH_SOURCE_URL = "https://bazaar.abuse.ch/export/txt/sha256/recent/"

HIGH_RISK_EXTENSIONS = ('.vbe' , '.js', '.docm', '.inf', '.sh', '.dll', '.doc', '.msp', '.xlsm', '.inx', '.dotm', '.hta', '.ps1', '.gadget', '.exe', '.rtf', '.msh', '.bat', '.xls', '.com', '.ocx', '.cmd', '.scr', '.url', '.pif', '.cpl', '.sys', '.vbs', '.msi', '.jse', '.drv', '.job', '.wsh', '.wsf', '.pptm', '.ins', '.mst', '.pdf', '.lnk')