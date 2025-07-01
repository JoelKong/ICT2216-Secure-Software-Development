from flask import request, jsonify, current_app
from app.interfaces.services.IAuthService import IAuthService
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity, set_refresh_cookies, unset_jwt_cookies
from app.models.users import User
import pyotp

class AuthController:
    def __init__(self, auth_service: IAuthService = None):
        self.auth_service = auth_service or AuthService()
    
    def signup(self):
        """Handle user signup"""
        try:
            data = request.get_json()
            current_app.logger.info(f"Signup attempt for user: {data.get('email')}")
            
            # Validate signup data
            is_valid, message = self.auth_service.validate_signup_data(data)
            if not is_valid:
                return jsonify({"error": message}), 400
                
            # Create user
            user = self.auth_service.create_user(data)
            
            # Generate tokens
            tokens = self.auth_service.generate_tokens(user.user_id)
            
            # Create response
            response = jsonify({
                "message": "Sign up was successful! Logging in...",
                "access_token": tokens['access_token'],
            })
            
            # Set refresh token as HttpOnly cookie
            set_refresh_cookies(response, tokens['refresh_token'])
            
            return response, 201
            
        except Exception as e:
            current_app.logger.error(f"Error during signup: {str(e)}")
            return jsonify({"error": "Something went wrong. Please try again."}), 500
    
    def login(self):
        """Handle user login"""
        try:
            data = request.get_json()
            
            email = data.get('email')
            password = data.get('password')
            
            current_app.logger.info(f"Login attempt for user: {email}")
            
            if not email or not password:
                return jsonify({"error": "Email and password required"}), 400
                
            # Authenticate user
            user, error = self.auth_service.login(email, password)
            if error:
                return jsonify({"error": error}), 401
                
            # Generate tokens
            tokens = self.auth_service.generate_tokens(user.user_id)
            
            # Create response
            response = jsonify({
                "message": "Login successful", 
                "access_token": tokens['access_token'],
            })
            
            # Set refresh token as HttpOnly cookie
            set_refresh_cookies(response, tokens['refresh_token'])
            
            return response, 200
            
        except Exception as e:
            current_app.logger.error(f"Error during login: {str(e)}")
            return jsonify({"error": "Something went wrong. Please try again."}), 500
    
    @jwt_required(refresh=True)
    def refresh_token(self):
        """Refresh access token using refresh token"""
        try:
            # Get user ID from refresh token
            user_id = get_jwt_identity()
            current_app.logger.info(f"Refreshing token for user {user_id}")
            
            # Generate new access token
            tokens = self.auth_service.refresh_access_token(user_id)
            
            return jsonify(tokens), 200
            
        except Exception as e:
            current_app.logger.error(f"Error refreshing token: {str(e)}")
            return jsonify({"error": "Failed to refresh token"}), 500
    
    def logout(self):
        """Handle user logout"""
        try:
            # Create response and unset JWT cookies
            response = jsonify({"message": "Logout successful"})
            unset_jwt_cookies(response)
            
            return response, 200
            
        except Exception as e:
            current_app.logger.error(f"Error during logout: {str(e)}")
            return jsonify({"error": "Something went wrong. Please try again."}), 500

    @jwt_required()
    def get_user_totp_secret(self):
        """Retrieve the TOTP secret"""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        print("🧠 user_id from JWT:", user_id)
        print("🔍 user found:", user)
        print("🔐 totp_secret:", user.totp_secret if user else "no user")

        if user and user.totp_secret:
            return jsonify({"totpSecret": user.totp_secret}), 200
        else:
            return jsonify({"error": "TOTP secret not found"}), 404

    @jwt_required()
    def verify_totp(self):
        """Verify the OTP code entered by the user"""
        data = request.get_json()
        code = data.get("code")  # OTP entered by user
        secret = data.get("totpSecret")  # The TOTP secret

        # Ensure both code and secret are provided
        if not code or not secret:
            return jsonify({"success": False, "error": "Missing code or secret"}), 400

        # Verify the TOTP code using the secret
        totp = pyotp.TOTP(secret)
        is_valid = totp.verify(code)

        if is_valid:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False, "error": "Invalid TOTP code"}), 400