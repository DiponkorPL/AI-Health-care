# utils/validation.py
# Input validation functions for forms

from utils.helpers import is_valid_email


def validate_signup(username: str, email: str, password: str, confirm: str):
    """
    Validates signup form inputs.
    Returns (True, "") on success, or (False, error_message) on failure.
    """
    if not username.strip():
        return False, "Username is required."
    if len(username.strip()) < 3:
        return False, "Username must be at least 3 characters."
    if not email.strip():
        return False, "Email address is required."
    if not is_valid_email(email.strip()):
        return False, "Please enter a valid email address."
    if not password:
        return False, "Password is required."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if password != confirm:
        return False, "Passwords do not match."
    return True, ""


def validate_login(username: str, password: str):
    """
    Validates login form inputs.
    Returns (True, "") on success, or (False, error_message) on failure.
    """
    if not username.strip():
        return False, "Username is required."
    if not password:
        return False, "Password is required."
    return True, ""


def validate_password_reset(email: str, new_password: str, confirm: str):
    """Validates password reset form inputs."""
    if not email.strip():
        return False, "Email address is required."
    if not is_valid_email(email.strip()):
        return False, "Please enter a valid email address."
    if not new_password:
        return False, "New password is required."
    if len(new_password) < 6:
        return False, "Password must be at least 6 characters."
    if new_password != confirm:
        return False, "Passwords do not match."
    return True, ""