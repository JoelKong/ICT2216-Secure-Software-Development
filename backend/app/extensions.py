from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request

# Define a custom key function that exempts OPTIONS requests
def limiter_key_func():
    if request.method == "OPTIONS":
        return None
    return get_remote_address()

# Initialize limiter without attaching to an app yet
limiter = Limiter(
    key_func=limiter_key_func,
    default_limits=[],
    strategy="fixed-window"
)