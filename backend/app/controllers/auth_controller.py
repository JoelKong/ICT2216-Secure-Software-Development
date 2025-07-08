import re
from flask import request, jsonify, current_app
from app.interfaces.services.IAuthService import IAuthService
from app.services.auth_service import AuthService
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

ERROR_MESSAGE = "Something went wrong. Please try again."

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
            response = jsonify({
                "message": "Sign up successful! Please Verify email."
            })
            self.auth_service.send_verification_email(user)
            return response, 201

        except Exception as e:
            current_app.logger.error(f"Error during signup: {e}")
            return jsonify({"error": ERROR_MESSAGE}), 500

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
            
            # Prevent login if email is not verified
            if not user.email_verified:
                return jsonify({"error": "Email not verified. Please check your inbox."}), 401
            
            totp_verified = user.totp_verified
            tokens = self.auth_service.generate_tokens(user.user_id, totp_verified=totp_verified)
            response = jsonify({
                "message": "Login successful",
                "access_token": tokens["access_token"]
            })
            set_refresh_cookies(response, tokens["refresh_token"])
            return response, 200

        except Exception as e:
            current_app.logger.error(f"Error during login: {e}")
            return jsonify({"error": ERROR_MESSAGE}), 500

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
            return jsonify({"error": ERROR_MESSAGE}), 500
        
    @jwt_required()
    def get_totp_setup(self):
        """Return provisioning URI and showQr flag based on TOTP state"""
        user_id = int(get_jwt_identity())
        user = self.auth_service.get_user(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # 1) If they’ve already verified TOTP, skip QR
        if user.totp_verified:
            return jsonify({
                "message": "TOTP already verified",
                "showQr": False,
                "otpUrl": None
            }), 200

        # 2) Otherwise do setup
        if not user.totp_secret:
            return jsonify({"error": "TOTP not configured"}), 400

        totp = pyotp.TOTP(user.totp_secret)
        uri  = totp.provisioning_uri(name=user.email, issuer_name="TheleonardoDR")

        return jsonify({
            "otpUrl": uri,
            "showQr": True
        }), 200
        
    @jwt_required()
    def verify_totp(self):
        """Verify the OTP code entered by the user"""
        user_id = int(get_jwt_identity())
        user = self.auth_service.get_user(user_id)

        if user.totp_verified:
            new_tokens = self.auth_service.generate_tokens(user.user_id, totp_verified=True)
            return jsonify({
                "message": "TOTP already verified",
                "access_token": new_tokens["access_token"]
            }), 200
    
        data = request.get_json()
        code = data.get("code")

        # Ensure both code and secret are provided
        if not code:
            return jsonify({"success": False, "error": "Missing code"}), 400

        # Verify the TOTP code using the secret
        totp = pyotp.TOTP(user.totp_secret)
        is_valid = totp.verify(code)

        if is_valid:
            self.auth_service.update_totp_verified(user_id, True)
            current_app.logger.info(f"TOTP verified for user {user_id}")
            user_id = int(get_jwt_identity())
            new_tokens = self.auth_service.generate_tokens(user_id, totp_verified=True)
            return jsonify({
                "message": "TOTP Verified!",
                "access_token": new_tokens["access_token"]
            }), 200
        else:
            return jsonify({"success": False, "error": "Invalid TOTP code"}), 400
        
    def verify_email(self):
        token = request.args.get('token')
        salt = request.args.get('salt')
        
        if not token or not salt:
            return jsonify({"error": "Missing token"}), 400

        success = self.auth_service.verify_email_token(token, salt)
        if not success:
            return jsonify({"error": "Invalid or expired token"}), 400

        tokens = self.auth_service.generate_tokens(success)
        response = jsonify({
            "message": "Email verified successfully!",
            "access_token": tokens["access_token"]
        })
        set_refresh_cookies(response, tokens["refresh_token"])
        return response, 200