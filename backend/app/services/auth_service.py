from app.interfaces.services.IAuthService import IAuthService
from app.interfaces.repositories.IUserRepository import IUserRepository
from app.repositories.user_repository import UserRepository
from app.models.users import User
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.validation import is_valid_email, is_strong_password
from flask_jwt_extended import create_access_token, create_refresh_token
import datetime
from itsdangerous import URLSafeTimedSerializer
import secrets
from flask_mail import Message
from app import mail
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
    
    def generate_tokens(self, user_id: int, totp_verified: bool = False) -> Dict[str, str]:
        """Generate access and refresh tokens"""
        # Convert user_id to string
        str_user_id = str(user_id)
        additional_claims = {"totp_verified": totp_verified}

        if not totp_verified:
            access_token = create_access_token(
                identity=str_user_id,
                expires_delta=datetime.timedelta(minutes=3),
                additional_claims=additional_claims
            )
        else:
            # Create access token with 15-minute expiry
            access_token = create_access_token(
                identity=str_user_id,
                expires_delta=datetime.timedelta(minutes=15),
                additional_claims=additional_claims
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
    
    # Send verification email to user
    def generate_email_token(self, user: User) -> tuple[str, str]:
        """Generate token and random salt (to be passed separately)"""
        salt = secrets.token_urlsafe(16)  # Random salt
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps({'user_id': user.user_id}, salt=salt)
        return token, salt

    def send_verification_email(self, user: User):
        token, salt = self.generate_email_token(user)

        current_app.logger.info(f"🔐 Generated token: {token}")
        current_app.logger.info(f"🧂 Token salt: {salt}")

        verification_url = (
            f"{current_app.config['FRONTEND_ROUTE']}/verify_email?"
            f"token={token}&salt={salt}"
        )

        current_app.logger.info(f"📩 Verification URL: {verification_url}")

        msg = Message(
            subject="Verify Your Email",
            recipients=[user.email],
            body=f"Hi {user.username},\n\nClick the link to verify your email:\n\n{verification_url}"
        )
        mail.send(msg)

    def verify_email_token(self, token: str, salt: str, max_age: int = 3600) -> bool:
        """Verify email token with externally passed salt"""
        try:
            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            data = serializer.loads(token, salt=salt, max_age=max_age)
            user_id = data.get("user_id")
        except Exception as e:
            current_app.logger.warning(f"Invalid or expired token: {e}")
            return False

        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None

        if not user.email_verified:
            self.user_repository.update(user, {"email_verified": True})

        return user_id
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            current_app.logger.warning(f"User with ID {user_id} not found")
            return None
        return user
    
    def update_totp_verified(self, user_id: int, totp_verified: bool) -> None:
        """Update TOTP verification status"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            current_app.logger.warning(f"User with ID {user_id} not found for TOTP update")
            raise ValueError("User not found")
        
        user.totp_verified = totp_verified
        self.user_repository.update(user, {"totp_verified": totp_verified})
        current_app.logger.info(f"TOTP verification status updated for user {user.username}")