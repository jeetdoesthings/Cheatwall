from pyvda import VirtualDesktop
from screenshot_manager import take_screenshot
from input_buffer_manager import add_input_event
from datetime import datetime

# Store the current desktop ID
last_desktop_id = VirtualDesktop.current().id

def monitor_desktop_switch():
    global last_desktop_id
    current_desktop_id = VirtualDesktop.current().id

    # Check if the desktop has changed
    if current_desktop_id != last_desktop_id:
        last_desktop_id = current_desktop_id
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reason = "Suspicious activity detected: Desktop switch"
        event_data = [timestamp, "Desktop Switch", "", "", "", "", "", reason, f"Switched to desktop ID: {current_desktop_id}"]
        add_input_event(event_data)

        # Take a screenshot
        take_screenshot(f"Desktop {current_desktop_id}", reason)