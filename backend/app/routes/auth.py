from flask import Blueprint
from app.controllers.auth_controller import AuthController
from app.services.auth_service import AuthService
from app.extensions import limiter

auth_bp = Blueprint('auth', __name__)

# Create service instance
auth_service = AuthService()

# Create controller with injected service
auth_controller = AuthController(auth_service=auth_service)

# Sign up route with rate limiting
@auth_bp.route('/signup', methods=['POST'])
@limiter.limit("5 per minute")
def signup():
    return auth_controller.signup()

# Login route with rate limiting
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