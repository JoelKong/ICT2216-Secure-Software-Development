from flask import Blueprint
from app.controllers.auth_controller import AuthController
from app.extensions import limiter

auth_bp = Blueprint('auth', __name__)
auth_controller = AuthController()

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