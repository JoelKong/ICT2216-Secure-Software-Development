from abc import abstractmethod
from typing import Optional, Dict, Any, List
from app.interfaces.repositories.IBaseRepository import IBaseRepository
from app.models.users import User

class IUserRepository(IBaseRepository[User]):
    """Interface for user repository operations"""
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass
    
    @abstractmethod
    def check_email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        pass
    
    @abstractmethod
    def check_username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        pass
    
    @abstractmethod
    def update_membership(self, user_id: int, is_premium: bool) -> User:
        """Update user membership status"""
        pass

    @abstractmethod
    def update_profile_picture(self, user_id: int, filename: str) -> None:
        """Update user profile picture"""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass