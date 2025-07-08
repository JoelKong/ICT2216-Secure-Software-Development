from abc import ABC, abstractmethod
from typing import Dict, Tuple, Any, Optional, List

class IProfileService(ABC):
    """Interface for profile service operations"""
    
    @abstractmethod
    def get_user_profile(self, user_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Get user profile data"""
        pass
    
    @abstractmethod
    def update_profile(self, user_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Update user profile"""
        pass
    
    @abstractmethod
    def update_profile_picture(self, user_id: int, file) -> Tuple[Optional[str], Optional[str]]:
        """Upload and update user's profile picture"""
        pass

    @abstractmethod
    def get_profile_image(self, filename: str) -> Any:
        """Serve the user's profile picture by filename"""
        pass

    @abstractmethod
    def delete_user_profile(self, user_id: int) -> Tuple[bool, Optional[str]]:
        """Delete user and related data"""
        pass

    @abstractmethod
    def get_user_posts(self, user_id: int, sort_by: str = 'recent', limit: int = 10, offset: int = 0) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """Get posts created by user"""
        pass