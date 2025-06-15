from app.repositories.user_repository import UserRepository
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.validation import is_valid_email, is_strong_password
from flask import current_app

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
    
    def validate_signup_data(self, data):
        """Validate signup form data"""
        errors = {}
        
        # Required fields validation
        required_fields = ['email', 'username', 'password', 'confirmPassword']
        for field in required_fields:
            if not data.get(field):
                errors[field] = f"{field} is required"
        
        if errors:
            return False, "All fields are required."
            
        # Email format validation
        if not is_valid_email(data['email']):
            return False, "Invalid email format."
            
        # Passwords match
        if data['password'] != data['confirmPassword']:
            return False, "Passwords do not match."
            
        # Password strength
        is_password_strong, message = is_strong_password(data['password'])
        if not is_password_strong:
            return False, message
            
        # Unique email
        if self.user_repository.get_by_email(data['email']):
            return False, "Email already in use."
            
        # Unique username
        if self.user_repository.get_by_username(data['username']):
            return False, "Username already taken."
            
        return True, ""
        
    def create_user(self, user_data):
        """Create new user"""
        try:
            # Hash password
            hashed_password = generate_password_hash(user_data['password'])
            
            # Create user object
            new_user_data = {
                'email': user_data['email'],
                'username': user_data['username'],
                'password': hashed_password
            }
            
            # Save to database
            user = self.user_repository.create(new_user_data)
            current_app.logger.info(f"New user created: {user.username}")
            return user
            
        except Exception as e:
            current_app.logger.error(f"Error creating user: {str(e)}")
            raise
            
    def login(self, email, password):
        """Authenticate user login"""
        try:
            # Validate inputs
            if not email or not password:
                return None, "Email and password required"
                
            # Find user
            user = self.user_repository.get_by_email(email)
            
            # Check credentials
            if not user or not check_password_hash(user.password, password):
                current_app.logger.warning(f"Failed login attempt for email: {email}")
                return None, "Invalid email or password"
                
            current_app.logger.info(f"User logged in: {user.username}")
            return user, None
                
        except Exception as e:
            current_app.logger.error(f"Error during login: {str(e)}")
            raise
            
    def generate_tokens(self, user_id):
        """Generate JWT tokens for authentication"""
        try:
            user_identity = str(user_id)
            access_token = create_access_token(identity=user_identity)
            refresh_token = create_refresh_token(identity=user_identity)
            
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            
        except Exception as e:
            current_app.logger.error(f"Error generating tokens: {str(e)}")
            raise