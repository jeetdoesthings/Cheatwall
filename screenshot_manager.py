import os
from datetime import datetime
from PIL import ImageGrab, ImageDraw, ImageFont
from config import screenshot_folder

def take_screenshot(app_name, reason):
    """Take a screenshot, save it with a descriptive filename, and overlay text."""
    try:
        # Format the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Replace spaces and special characters in the reason for filename safety
        sanitized_reason = reason.replace(" ", "_").replace(":", "").replace("/", "_")

        # Construct the screenshot filename
        screenshot_name = f"{app_name}_{sanitized_reason}_{timestamp}.png"

        # Ensure the screenshots folder exists
        os.makedirs(screenshot_folder, exist_ok=True)

        # Take the screenshot
        screenshot = ImageGrab.grab()

        # Overlay app name and reason on the screenshot
        draw = ImageDraw.Draw(screenshot)
        font_path = "arial.ttf"  # Replace with the path to a valid font file if needed
        try:
            font = ImageFont.truetype(font_path, 20)  # Use a TrueType font
        except IOError:
            font = ImageFont.load_default()  # Fallback to default font if TrueType font is unavailable

        text = f"App: {app_name}\nReason: {reason}"
        draw.text((10, 10), text, fill="red", font=font)  # Overlay text at the top-left corner

        # Save the screenshot
        screenshot_path = os.path.join(screenshot_folder, screenshot_name)
        screenshot.save(screenshot_path)

        print(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None