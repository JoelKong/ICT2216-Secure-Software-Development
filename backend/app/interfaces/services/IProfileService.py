from abc import ABC, abstractmethod
from typing import Dict, Tuple, Any, Optional, List

class IProfileService(ABC):
    """Interface for profile service operations"""
    
    @abstractmethod
    def get_user_profile(self, user_id: int) -> Tuple[Dict[str, Any], Optional[str]]:
        """Get user profile data"""
        pass
    
    @abstractmethod
    def update_profile(self, user_id: int, data: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[str]]:
        """Update user profile"""
        pass
    
    # @abstractmethod
    # def get_user_posts(self, user_id: int, sort_by: str = 'recent', 
    #                     limit: int = 10, offset: int = 0) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    #     """Get posts created by user"""
    #     pass