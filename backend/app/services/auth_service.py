from app.interfaces.services.IAuthService import IAuthService
from app.interfaces.repositories.IUserRepository import IUserRepository
from app.repositories.user_repository import UserRepository
from app.models.users import User
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.validation import is_valid_email, is_strong_password
from flask_jwt_extended import create_access_token, create_refresh_token
import datetime
from typing import Dict, Tuple, Optional
import pyotp

class AuthService(IAuthService):
    def __init__(self, user_repository: IUserRepository = None):
        self.user_repository = user_repository or UserRepository()
    
    def validate_signup_data(self, data: Dict[str, str]) -> Tuple[bool, str]:
        """Validate user signup data"""
        # Check required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Missing required field: {field}"
        
        # Validate username
        if len(data['username']) < 3:
            return False, "Username must be at least 3 characters"
        
        # Check if username already exists
        if self.user_repository.check_username_exists(data['username']):
            return False, "Username already exists"
        
        # Validate email
        if not is_valid_email(data['email']):
            return False, "Invalid email format"
        
        # Check if email already exists
        if self.user_repository.check_email_exists(data['email']):
            return False, "Email already exists"
        
        # Validate password
        if not is_strong_password(data['password']):
            return False, "Password must be at least 8 characters and contain at least one uppercase letter, one lowercase letter, one number, and one special character"
        
        return True, ""
    
    def create_user(self, data: Dict[str, str]) -> User:
        """Create a new user"""
        # Hash the password
        hashed_password = generate_password_hash(data['password'])
        
        totp = pyotp.TOTP(pyotp.random_base32())
        totp_secret = totp.secret

        # Prepare user data
        user_data = {
            'username': data['username'],
            'email': data['email'],
            'password': hashed_password,
            'profile_picture': data.get('profile_picture', 'default.jpg'),
            'membership': 'basic',
            'totp_secret': totp_secret
        }
        
        # Create user
        user = self.user_repository.create(user_data)
        current_app.logger.info(f"Created new user with username: {user.username}")
        
        return user
    
    def login(self, email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        """Authenticate a user"""
        # Get user by email
        user = self.user_repository.get_by_email(email)
        if not user:
            current_app.logger.warning(f"Login attempt with non-existent email: {email}")
            return None, "Invalid email or password"
        
        # Check password
        if not check_password_hash(user.password, password):
            current_app.logger.warning(f"Failed login attempt for user: {user.username}")
            return None, "Invalid email or password"
        
        current_app.logger.info(f"Successful login for user: {user.username}")
        return user, None
    
    def generate_tokens(self, user_id: int) -> Dict[str, str]:
        """Generate access and refresh tokens"""
        # Convert user_id to string
        str_user_id = str(user_id)
        
        # Create access token with 15-minute expiry
        access_token = create_access_token(
            identity=str_user_id,
            expires_delta=datetime.timedelta(minutes=15)
        )
        
        # Create refresh token with 30-day expiry
        refresh_token = create_refresh_token(
            identity=str_user_id,
            expires_delta=datetime.timedelta(days=30)
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    def refresh_access_token(self, user_id: int) -> Dict[str, str]:
        """Generate a new access token using a refresh token"""
        # Convert user_id to string
        str_user_id = str(user_id)
        
        # Create new access token with 15-minute expiry
        access_token = create_access_token(
            identity=str_user_id,
            expires_delta=datetime.timedelta(minutes=15)
        )
        
        return {
            'access_token': access_token
        }