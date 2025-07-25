from flask import Blueprint
from app.controllers.auth_controller import AuthController
from app.services.auth_service import AuthService
from app.extensions import limiter

auth_bp = Blueprint('auth', __name__)

auth_service = AuthService()

# Create controller with injected service
auth_controller = AuthController(auth_service=auth_service)

# Sign up route with rate limiting
# Limiter is done to prevent abuse of the signup endpoint and spams especially for bots
@auth_bp.route('/signup', methods=['POST'])
@limiter.limit("5 per minute")
def signup():
    return auth_controller.signup()

# Login route with rate limiting
# Limiter is done to prevent abuse of the signup endpoint and spams especially for brute force attacks
@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    return auth_controller.login()

# Refresh token route
@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    return auth_controller.refresh_token()

# Logout route
@auth_bp.route('/logout', methods=['POST'])
def logout():
    return auth_controller.logout()

@auth_bp.route('/verify_totp', methods=['POST'])
def verify_totp():
    return auth_controller.verify_totp()

@auth_bp.route('/totp_setup', methods=['GET'])
def totp_setup():
    return auth_controller.get_totp_setup()

@auth_bp.route('/verify_email', methods=['GET'])
def verify_email():
    return auth_controller.verify_email()