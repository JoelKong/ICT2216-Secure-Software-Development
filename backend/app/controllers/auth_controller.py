# backend/app/controllers/auth_controller.py

import re
from flask import request, jsonify, current_app
from app.interfaces.services.IAuthService import IAuthService
from app.services.auth_service import AuthService
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    set_refresh_cookies,
    unset_jwt_cookies
)

# --- Regex patterns ---
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
            if not re.match(EMAIL_REGEX, email):
                return jsonify({"error": "Invalid email format"}), 400

            # --- Validate username ---
            if not re.match(USERNAME_REGEX, username):
                return jsonify({
                    "error": "Username must be 3–20 chars, letters/numbers/underscore only."
                }), 400

            # --- Validate password ---
            if not re.match(PASSWORD_REGEX, password):
                return jsonify({
                    "error": (
                        "Password must be at least 8 chars, include uppercase, "
                        "lowercase, a number, and a special character."
                    )
                }), 400

            current_app.logger.info(f"Signup attempt: {email} (username: {username})")

            # Delegate to service for any further business logic
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

            # (Optionally) validate password complexity again, or skip
            # if not re.match(PASSWORD_REGEX, password):
            #     return jsonify({"error": "Invalid password format"}), 400

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
