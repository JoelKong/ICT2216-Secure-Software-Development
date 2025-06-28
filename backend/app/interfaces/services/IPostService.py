from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple
from app.models.posts import Post

class IPostService(ABC):
    """Interface for post service operations"""

    @abstractmethod
    def _is_allowed_file(self, filename: str) -> bool:
        """Check if a given filename has an allowed image extension."""
        pass

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

    @abstractmethod
    def get_post_detail(self, post_id: int, current_user_id: int) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def create_post(self, title: str, content: str, image_file, user_id: int) -> Post:
        pass

    @abstractmethod
    def edit_post(self, post_id: int, user_id: int, title: str, content: str, image_file: Optional[Any] = None) -> Optional[Post]:
        """Update a post's title, content, and optionally the image"""
        pass


    @abstractmethod
    def get_post_image(self, filename: str) -> Any:
        """Serve post image by filename"""
        pass