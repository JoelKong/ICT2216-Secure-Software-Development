from flask import request, jsonify, current_app
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity, set_refresh_cookies, unset_jwt_cookies

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()
        
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
            current_user_identity = get_jwt_identity()
            current_app.logger.info(f"Token refresh for user {current_user_identity}")
            
            # Generate new access token
            new_access_token = self.auth_service.generate_tokens(current_user_identity)['access_token']
            
            return jsonify(access_token=new_access_token), 200
            
        except Exception as e:
            current_app.logger.error(f"Error refreshing token: {str(e)}")
            return jsonify({"error": "Failed to refresh token"}), 500