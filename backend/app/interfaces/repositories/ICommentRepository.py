from abc import abstractmethod
from typing import List, Optional
from app.interfaces.repositories.IBaseRepository import IBaseRepository
from app.models.comments import Comment

class ICommentRepository(IBaseRepository[Comment]):
    """Interface for comment repository operations"""
    
    @abstractmethod
    def get_by_post_id(self, post_id: int) -> List[Comment]:
        """Get all comments for a specific post"""
        pass
    
    @abstractmethod
    def create_comment(self, comment: Comment) -> Comment:
        pass