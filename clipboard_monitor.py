import win32clipboard
from window_monitor import get_active_window
from config import WHITELISTED_APPS
from input_buffer_manager import add_input_event
from screenshot_manager import take_screenshot
from datetime import datetime

last_clipboard_content = ""
last_copied_process = ""

def monitor_clipboard():
    global last_clipboard_content, last_copied_process
    try:
        # Open the clipboard and get its content
        win32clipboard.OpenClipboard()
        clipboard_content = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        # Get the current active window
        process_name, window_title = get_active_window()

        # Check if the clipboard content has changed
        if clipboard_content != last_clipboard_content:
            last_clipboard_content = clipboard_content
            last_copied_process = process_name

            # Log the clipboard copy event
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            event_data = [timestamp, "Clipboard Copy", process_name, window_title, "", "", "", "Copied Text", clipboard_content]
            add_input_event(event_data)
            print(f"Clipboard Copy Logged: {event_data}")  # Debug statement

        # Check if text is pasted into the exam tab
        if process_name in WHITELISTED_APPS and clipboard_content == last_clipboard_content:
            if last_copied_process not in WHITELISTED_APPS:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                reason = "Suspicious activity detected: External text pasted into exam tab"
                event_data = [timestamp, "Clipboard Paste", process_name, window_title, "", "", "", reason, clipboard_content]
                take_screenshot(window_title, reason)
                add_input_event(event_data)
                print(f"Clipboard Paste Logged: {event_data}")  # Debug statement

    except Exception as e:
        print(f"Error monitoring clipboard: {e}")

def is_suspicious_text(text):
    """Check if the text contains suspicious content."""
    suspicious_keywords = ["cheat", "answer", "solution", "AI-generated"]
    for keyword in suspicious_keywords:
        if keyword.lower() in text.lower():
            return True
    return False