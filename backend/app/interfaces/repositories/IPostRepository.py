from abc import abstractmethod
from typing import List, Optional
from app.interfaces.repositories.IBaseRepository import IBaseRepository
from app.models.posts import Post

class IPostRepository(IBaseRepository[Post]):
    """Interface for post repository operations"""
    
    @abstractmethod
    def get_posts(self, sort_by: str = 'recent', limit: int = 10, offset: int = 0, 
                  search: Optional[str] = None, user_id: Optional[int] = None) -> List[Post]:
        """Get posts with filtering, sorting and pagination"""
        pass
    
    @abstractmethod
    def get_user_liked_posts(self, user_id: int, post_ids: Optional[List[int]] = None) -> List[Post]:
        """Get posts liked by a specific user"""
        pass