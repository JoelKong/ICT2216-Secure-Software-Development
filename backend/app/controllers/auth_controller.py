import re
from flask import request, jsonify, current_app
from app.interfaces.services.IAuthService import IAuthService
from app.services.auth_service import AuthService
from app.models.users import User
import pyotp
from app.utils.validation import is_valid_email, is_strong_password, is_valid_username
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    set_refresh_cookies,
    unset_jwt_cookies
)

EMAIL_REGEX = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
# Password: ≥8 chars, at least one lowercase, one uppercase, one digit, one special
PASSWORD_REGEX = (
    r"^(?=.*[a-z])"      # at least one lowercase
    r"(?=.*[A-Z])"       # at least one uppercase
    r"(?=.*\d)"          # at least one digit
    r"(?=.*[@$!%*#?&])"  # at least one special char
    r".{8,}$"            # at least 8 total chars
)
# Username: alphanumeric + underscores, 3–20 characters
USERNAME_REGEX = r"^[A-Za-z0-9_]{3,20}$"


class AuthController:
    def __init__(self, auth_service: IAuthService = None):
        self.auth_service = auth_service or AuthService()

    def signup(self):
        """Handle user signup with inline regex validation"""
        try:
            raw = request.get_json() or {}
            email    = (raw.get("email")    or "").strip()
            username = (raw.get("username") or "").strip()
            password = raw.get("password") or ""

            # --- Validate email ---
            if not is_valid_email(email):
                return jsonify({"error": "Invalid email format"}), 400

            # --- Validate username ---
            if not is_valid_username(username):
                return jsonify({
                    "error": "Username must be 3–20 chars, letters/numbers/underscore only."
                }), 400

            # --- Validate password ---
            is_strong, reason = is_strong_password(password)
            if not is_strong:
                return jsonify({"error": reason}), 400

            current_app.logger.info(f"Signup attempt: {email} (username: {username})")

            payload = {"email": email, "username": username, "password": password}
            is_valid, message = self.auth_service.validate_signup_data(payload)
            if not is_valid:
                return jsonify({"error": message}), 400

            user   = self.auth_service.create_user(payload)
            tokens = self.auth_service.generate_tokens(user.user_id)

            response = jsonify({
                "message": "Sign up successful! Logging in…",
                "access_token": tokens["access_token"]
            })
            set_refresh_cookies(response, tokens["refresh_token"])
            return response, 201

        except Exception as e:
            current_app.logger.error(f"Error during signup: {e}")
            return jsonify({"error": "Something went wrong. Please try again."}), 500

    def login(self):
        """Handle user login with basic regex validation"""
        try:
            raw = request.get_json() or {}
            email    = (raw.get("email")    or "").strip()
            password = raw.get("password") or ""

            current_app.logger.info(f"Login attempt for: {email}")

            # Presence checks
            if not email or not password:
                return jsonify({"error": "Email and password required"}), 400

            # Validate email format
            if not re.match(EMAIL_REGEX, email):
                return jsonify({"error": "Invalid email format"}), 400

            user, error = self.auth_service.login(email, password)
            if error:
                return jsonify({"error": error}), 401

            tokens = self.auth_service.generate_tokens(user.user_id)
            response = jsonify({
                "message": "Login successful",
                "access_token": tokens["access_token"]
            })
            set_refresh_cookies(response, tokens["refresh_token"])
            return response, 200

        except Exception as e:
            current_app.logger.error(f"Error during login: {e}")
            return jsonify({"error": "Something went wrong. Please try again."}), 500

    @jwt_required(refresh=True)
    def refresh_token(self):
        """Refresh access token using refresh token"""
        try:
            user_id = get_jwt_identity()
            current_app.logger.info(f"Refreshing token for user {user_id}")
            tokens = self.auth_service.refresh_access_token(user_id)
            return jsonify(tokens), 200

        except Exception as e:
            current_app.logger.error(f"Error refreshing token: {e}")
            return jsonify({"error": "Failed to refresh token"}), 500

    def logout(self):
        """Handle user logout"""
        try:
            response = jsonify({"message": "Logout successful"})
            unset_jwt_cookies(response)
            return response, 200

        except Exception as e:
            current_app.logger.error(f"Error during logout: {e}")
            return jsonify({"error": "Something went wrong. Please try again."}), 500
        
    @jwt_required()
    def get_user_totp_secret(self):
        """Retrieve the TOTP secret"""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user and user.totp_secret:
            return jsonify({"totpSecret": user.totp_secret}), 200
        else:
            return jsonify({"error": "TOTP secret not found"}), 404

    @jwt_required()
    def verify_totp(self):
        """Verify the OTP code entered by the user"""
        data = request.get_json()
        code = data.get("code")
        secret = data.get("totpSecret")

        # Ensure both code and secret are provided
        if not code or not secret:
            return jsonify({"success": False, "error": "Missing code or secret"}), 400

        # Verify the TOTP code using the secret
        totp = pyotp.TOTP(secret)
        is_valid = totp.verify(code)

        if is_valid:
            # Generate a new access token with totp_verified = True
            user_id = int(get_jwt_identity())
            new_tokens = self.auth_service.generate_tokens(user_id, totp_verified=True)
            return jsonify({
                "message": "TOTP Verified!",
                "access_token": new_tokens["access_token"]
            }), 200
        else:
            return jsonify({"success": False, "error": "Invalid TOTP code"}), 400