import os

# Combined CSV log setup
combined_log = "combined_log.csv"  # Save logs in CSV format
combined_headers = ['Timestamp', 'Event', 'Process Name', 'Window Title', 'PID', 'Local IP', 'Remote IP', 'Action taken', 'Details']

# Screenshots folder setup
screenshot_folder = 'screenshots'
os.makedirs(screenshot_folder, exist_ok=True)

# Whitelisted apps (to be set by the admin during the exam)
WHITELISTED_APPS = []

# Whitelisted domains
WHITELISTED_DOMAINS = [
    "gmail.com.com",  # Replace with actual whitelisted domains
    "google.com",
    "microsoft.com"
]

# Global flag for termination
running = True

# Store last window details
last_window = {"process_name": "", "window_title": ""}

# Initialize the seen_connections set
seen_connections = set()

# Typing speed thresholds (characters per second)
TYPING_SPEED_THRESHOLD = 10  # Adjust as needed

# Idle detection threshold (seconds)
IDLE_THRESHOLD = 60  # Adjust as needed

CRITICAL_PROCESSES = [
    "explorer.exe",      # Windows Explorer
    "taskmgr.exe",       # Task Manager
    "svchost.exe",       # Service Host
    "winlogon.exe",      # Windows Logon
    "csrss.exe",         # Client Server Runtime Process
    "lsass.exe",         # Local Security Authority Process
    "dwm.exe",           # Desktop Window Manager
    "TextInputHost.exe"  # Text Input Host (critical for text input services)
]

