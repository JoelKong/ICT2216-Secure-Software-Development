import re

def is_valid_email(email):
    if not email:
        return False

    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def is_strong_password(password):
    """Password strength check."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, ""

# This is to help validate IDs in the system, such as user IDs, post IDs, etc.
def is_valid_id(value):
    """Check if value is a positive integer (no leading zero)"""
    return re.match(r"^[1-9]\d*$", str(value)) is not None

# This is to validate usernames.
def is_valid_username(username):
    USERNAME_REGEX = r"^[A-Za-z0-9_]{3,20}$"
    return re.match(USERNAME_REGEX, username) is not None

