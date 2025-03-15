from pynput import keyboard, mouse
from window_monitor import get_active_window
from config import running, WHITELISTED_APPS, TYPING_SPEED_THRESHOLD, IDLE_THRESHOLD
from input_buffer_manager import add_input_event
from screenshot_manager import take_screenshot
from datetime import datetime
import time

last_keypress_time = time.time()
last_activity_time = time.time()
typed_characters = 0

def on_key_press(key):
    global running, last_keypress_time, last_activity_time, typed_characters
    process_name, window_title = get_active_window()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event_data = [timestamp, "Keypress", process_name, window_title, "", "", "", "Key pressed", str(key)]
    add_input_event(event_data)

    # Update typing speed
    current_time = time.time()
    time_diff = current_time - last_keypress_time
    last_keypress_time = current_time
    last_activity_time = current_time
    typed_characters += 1

    # Calculate typing speed
    if time_diff > 0:
        typing_speed = typed_characters / time_diff
        if typing_speed > TYPING_SPEED_THRESHOLD:
            reason = f"Suspicious activity detected: High typing speed ({typing_speed:.2f} chars/sec)"
            take_screenshot(window_title, reason)
            event_data[-1] = reason
            add_input_event(event_data)

    # Detect suspicious key combinations
    if key in [keyboard.Key.alt_l, keyboard.Key.tab]:
        if process_name not in WHITELISTED_APPS:
            reason = "Suspicious activity detected: Alt+Tab to non-whitelisted app"
            event_data = [timestamp, "Keypress", process_name, window_title, "", "", "", reason, str(key)]
            add_input_event(event_data)

    # Detect Ctrl+C and Ctrl+V
    if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        try:
            if key.char in ['c', 'v']:
                if process_name not in WHITELISTED_APPS:
                    reason = f"Suspicious activity detected: Ctrl+{key.char.upper()} in non-whitelisted app"
                    take_screenshot(window_title, reason)
                    event_data[-1] = reason
                    add_input_event(event_data)
        except AttributeError:
            pass  # Ignore non-character keys

    # Detect Windows shortcuts (e.g., Windows+D, Windows+E)
    if hasattr(key, 'vk') and key.vk == 91:  # Windows key
        reason = "Suspicious activity detected: Windows key shortcut"
        take_screenshot(window_title, reason)
        event_data[-1] = reason
        add_input_event(event_data)

    if key == keyboard.Key.esc:
        term_data = ['Termination requested', process_name, window_title, "", "", "", "Terminating", "Termination key pressed"]
        add_input_event(term_data)
        running = False
        return False

def on_key_release(key):
    pass

def on_click(x, y, button, pressed):
    global running, last_activity_time
    if not running:
        return False

    last_activity_time = time.time()
    action = "Pressed" if pressed else "Released"
    process_name, window_title = get_active_window()
    event_data = ['Mouse Click', process_name, window_title, "", "", "", f"Mouse {action}", f"({x}, {y})"]
    add_input_event(event_data)

def detect_idle():
    global last_activity_time
    current_time = time.time()
    idle_time = current_time - last_activity_time
    if idle_time > IDLE_THRESHOLD:
        process_name, window_title = get_active_window()
        reason = f"Suspicious activity detected: User idle for {idle_time:.2f} seconds"
        take_screenshot(window_title, reason)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event_data = [timestamp, "Idle Detection", process_name, window_title, "", "", reason, f"Idle time: {idle_time:.2f} seconds"]
        add_input_event(event_data)