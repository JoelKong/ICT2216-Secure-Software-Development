from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.models.comments import Comment

class ICommentService(ABC):
    
    @abstractmethod
    def get_comments_by_post(self, post_id: int) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def create_comment(self, post_id: int, user_id: int, content: str, parent_id: Optional[int] = None, image_file=None) -> Comment:
        pass

    @abstractmethod
    def get_comment_image(self, filename: str) -> Any:
        """Serve comment image by filename"""
        pass