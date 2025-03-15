import psutil
import win32gui
import win32process
from config import last_window, WHITELISTED_APPS
from input_buffer_manager import add_input_event
from screenshot_manager import take_screenshot
from datetime import datetime

def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process_name = psutil.Process(pid).name()
        window_title = win32gui.GetWindowText(hwnd)
        return process_name, window_title
    except Exception as e:
        return "Unknown", "Unknown"

def log_window_switch():
    global last_window
    process_name, window_title = get_active_window()
    if process_name != last_window["process_name"] or window_title != last_window["window_title"]:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event_data = [timestamp, "Window Switch", process_name, window_title, "", "", "Switched Window", ""]
        add_input_event(event_data)
        
        # Check for suspicious activity
        if process_name not in WHITELISTED_APPS:
            reason = "Suspicious activity detected: Window switch to non-whitelisted app"
            take_screenshot(window_title, reason)
            event_data[-1] = reason
            add_input_event(event_data)
        
        # Update last window
        last_window = {"process_name": process_name, "window_title": window_title}