# utils/helpers.py
# General utility helpers used across the project

import hashlib
import re
from datetime import datetime


def hash_password(password: str) -> str:
    """SHA-256 hash a plain-text password. Returns the hex digest."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain: str, hashed: str) -> bool:
    """Compare a plain password against its stored hash."""
    return hash_password(plain) == hashed


def center_window(window, width: int, height: int):
    """Center a Tkinter Toplevel or Tk window on the screen."""
    window.update_idletasks()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def now_str() -> str:
    """Return current datetime as a readable string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def is_valid_email(email: str) -> bool:
    """Basic email format validation."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return bool(re.match(pattern, email))


def truncate(text: str, max_len: int = 40) -> str:
    """Truncate long text with ellipsis."""
    return text if len(text) <= max_len else text[:max_len - 3] + "..."