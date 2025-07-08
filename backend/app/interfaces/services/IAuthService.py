from abc import ABC, abstractmethod
from typing import Dict, Tuple, Any, Optional
from app.models.users import User

class IAuthService(ABC):
    """Interface for authentication service operations"""
    
    @abstractmethod
    def validate_signup_data(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate user signup data"""
        pass
    
    @abstractmethod
    def create_user(self, data: Dict[str, Any]) -> User:
        """Create a new user"""
        pass
    
    @abstractmethod
    def login(self, email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        """Authenticate a user"""
        pass
    
    @abstractmethod
    def generate_tokens(self, user_id: int) -> Dict[str, str]:
        """Generate access and refresh tokens"""
        pass
    
    @abstractmethod
    def refresh_access_token(self, user_id: int) -> Dict[str, str]:
        """Generate a new access token using a refresh token"""
        pass

    @abstractmethod
    def generate_email_token(self, user: User) -> Tuple[str, str]:
        """Generate a token for email verification"""
        pass

    @abstractmethod
    def send_verification_email(self, user: User) ->  None:
        """Send verification email to the user"""
        pass

    @abstractmethod
    def verify_email_token(self, token: str) -> Optional[User]:
        """Verify the email token and return the user if valid"""
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    def update_totp_verified(self, user_id: int, totp_verified: bool) -> None:
        """Update TOTP verification status"""
        pass