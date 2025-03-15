from pynput import keyboard, mouse
from input_monitor import on_key_press, on_key_release, on_click, detect_idle
from window_monitor import log_window_switch
from network_monitor import monitor_network
from process_monitor import monitor_processes
from desktop_monitor import monitor_desktop_switch
from config import running
import time
from clipboard_monitor import monitor_clipboard
import threading
from network_monitor import block_non_whitelisted_domains

# Global list to store whitelisted apps
WHITELISTED_APPS = []

def on_key_press(key):
    # Remove the ESC key termination logic
    process_name = "Unknown Process"  # Placeholder value; replace with actual process name retrieval logic
    window_title = "Unknown Window"  # Placeholder value; replace with actual window title retrieval logic
    event_data = ['Keypress', process_name, window_title, "", "", "", "Key pressed", str(key)]
    print(f"Input event logged: {event_data}")  # Placeholder for actual logging logic

def main():
    # Allow the user to specify whitelisted apps
    print("Enter the names of whitelisted apps (comma-separated, e.g., chrome.exe, code.exe):")
    user_input = input().strip()
    WHITELISTED_APPS.extend([app.strip() for app in user_input.split(",")])
    print(f"Whitelisted apps: {WHITELISTED_APPS}")

    # Start network blocking in a separate thread
    network_blocking_thread = threading.Thread(target=block_non_whitelisted_domains, daemon=True)
    network_blocking_thread.start()

    # Start keyboard listener
    keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    keyboard_listener.start()

    # Start mouse listener
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    # Monitor window switches, network, processes, idle detection, desktop switches, and clipboard
    try:
        while running:
            log_window_switch()
            monitor_network()  # Monitor network activity
            monitor_processes(WHITELISTED_APPS)  # Pass whitelisted apps to monitor_processes
            monitor_desktop_switch()
            detect_idle()
            monitor_clipboard()
            time.sleep(1)  # Reduce CPU usage
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    main()