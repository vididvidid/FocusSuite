"""
Contains Windows-specific utility functions using the pywin32
library. This isolates platform-dependent code.
"""

import logging

logger = logging.getLogger(__name__)

try:
    import win32gui
    IS_WINDOWS = True
except ImportError:
    IS_WINDOWS = False
    logger.warning("'pywin32' not found. Whitelisting and window detection will be disabled.")

def get_active_window_bbox() -> tuple | None:
    #Gets the bounding box (x1,y1,x2,y2) of the active window
    if not IS_WINDOWS:
        return None
    try:
        hwnd = win32gui.GetForegroundWindow()
        #Exclue the desktop to avoid capturing the entire screen
        if win32gui.GetWindowText(hwnd) in ["Program Manager",""]:
            return None
        return win32gui.GetWindowRect(hwnd)
    except Exception as e:
        logger.warning(f"Could not get active window rect: {e}")
        return None


def is_whitelisted(whitelist: list) -> bool:
    #Checks if the active window's title matches any item in the whitelist
    if not IS_WINDOWS or not whitelist:
        return False
    try:
        hwnd = win32gui.GetForegroundWindow()
        active_title = win32gui.GetWindowText(hwnd).lower()

        for item in whitelist:
            if item.lower() in active_title:
                logger.debug(f"Whitelisted app detected: '{active_title}' matches '{item}'")
                return True
    except Exception as e:
        logger.warning(f"Could not get active window titel for whitelist check: {e}")
        return False
