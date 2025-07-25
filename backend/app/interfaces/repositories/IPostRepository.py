from abc import abstractmethod
from typing import List, Optional
from app.interfaces.repositories.IBaseRepository import IBaseRepository
from app.models.posts import Post

class IPostRepository(IBaseRepository[Post]):
    """Interface for post repository operations"""
    
    @abstractmethod
    def get_posts(self, sort_by: str = 'recent', limit: int = 10, offset: int = 0, search: Optional[str] = None, user_id: Optional[int] = None) -> List[Post]:
        """Get posts with filtering, sorting and pagination"""
        pass
    
    @abstractmethod
    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        pass
    
    @abstractmethod
    def create_post(self, title: str, content: str, image_url: Optional[str], user_id: int) -> Post:
        pass

    @abstractmethod
    def edit_post(self, post_id: int, title: str, content: str, image_url: Optional[str]) -> Optional[Post]:
        """Update the post's content and optionally the image"""
        pass

    @abstractmethod
    def count_user_posts_today(self, user_id: int) -> int:
        """Retrieve count of posts made by user today"""
        pass