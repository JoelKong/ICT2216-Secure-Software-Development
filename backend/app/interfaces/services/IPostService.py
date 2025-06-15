from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple

class IPostService(ABC):
    """Interface for post service operations"""
    
    @abstractmethod
    def get_posts(self, sort_by: str = 'recent', page: int = 1, 
                  search: Optional[str] = None, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get posts with pagination, filtering and sorting"""
        pass
    
    @abstractmethod
    def toggle_like(self, post_id: int, user_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Toggle like status for a post"""
        pass
    
    @abstractmethod
    def delete_post(self, post_id: int, user_id: int) -> Tuple[bool, str]:
        """Delete a post if user is authorized"""
        pass
        
    @abstractmethod
    def get_user_liked_posts(self, user_id: int, post_ids: Optional[List[int]] = None) -> List[int]:
        """Get IDs of posts liked by a specific user"""
        pass