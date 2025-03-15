import psutil
import win32gui
import win32process
from datetime import datetime
from input_buffer_manager import add_input_event
from screenshot_manager import take_screenshot
from config import CRITICAL_PROCESSES

def terminate_process(pid):
    """Terminate a process using Windows API."""
    try:
        # Get process handle with required privileges
        handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, pid)
        if handle:
            win32api.TerminateProcess(handle, -1)
            win32api.CloseHandle(handle)
            return True
    except Exception as e:
        print(f"Error terminating process: {e}")
    return False

def is_window_visible(pid):
    """Check if a process has a visible window."""
    def callback(hwnd, visible_windows):
        if win32gui.IsWindowVisible(hwnd):
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid == pid:
                visible_windows.append(hwnd)
    visible_windows = []
    win32gui.EnumWindows(callback, visible_windows)
    return len(visible_windows) > 0

def monitor_processes(whitelisted_apps):
    """Monitor running processes and terminate unwhitelisted apps with visible windows."""
    try:
        for process in psutil.process_iter(['pid', 'name']):
            process_name = process.info['name']
            pid = process.info['pid']

            # Skip processes without visible windows
            if not is_window_visible(pid):
                continue

            # Skip critical Windows processes
            if process_name.lower() in [critical.lower() for critical in CRITICAL_PROCESSES]:
                continue

            # Skip whitelisted apps
            if process_name.lower() in [app.lower() for app in whitelisted_apps]:
                print(f"Skipping whitelisted app: {process_name} (PID: {pid})")
                continue

            # Log and terminate unwhitelisted apps
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            reason = f"Suspicious activity detected: Unwhitelisted app running ({process_name})"
            
            print(f"Attempting to terminate: {process_name} (PID: {pid})")
            
            # Take a screenshot before terminating
            screenshot_path = take_screenshot(process_name, reason)
            if screenshot_path:
                print(f"Screenshot captured: {screenshot_path}")
            else:
                print(f"Failed to capture screenshot for: {process_name} (PID: {pid})")

            # Log the detection
            event_data = [timestamp, "Process Activity", process_name, "", pid, "", "", reason, ""]
            add_input_event(event_data)

            # Attempt to terminate the process
            try:
                psutil.Process(pid).terminate()
                termination_reason = f"Terminated unwhitelisted app: {process_name}"
                event_data = [timestamp, "Process Termination", process_name, "", pid, "", "", termination_reason, ""]
                add_input_event(event_data)
                print(f"Successfully terminated process: {process_name} (PID: {pid})")
            except Exception as e:
                print(f"Failed to terminate process {process_name} (PID: {pid}): {e}")

    except Exception as e:
        print(f"Error in monitor_processes: {e}")