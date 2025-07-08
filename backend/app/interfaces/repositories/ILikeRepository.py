from abc import abstractmethod
from typing import Optional, List
from app.interfaces.repositories.IBaseRepository import IBaseRepository
from app.models.likes import Like

class ILikeRepository(IBaseRepository[Like]):
    """Interface for like repository operations"""
    
    @abstractmethod
    def get_by_user_and_post(self, user_id: int, post_id: int) -> Optional[Like]:
        """Get like by user_id and post_id"""
        pass
    
    @abstractmethod
    def get_user_liked_post_ids(self, user_id: int, post_ids: Optional[List[int]] = None) -> List[int]:
        """Get IDs of posts liked by a specific user"""
        pass

    @abstractmethod
    def count_likes_for_post(self, post_id: int) -> int:
        """Count likes for a specific post"""
        pass