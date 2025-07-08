from .base_repository import BaseRepository
from app.models.likes import Like
from app.interfaces.repositories.ILikeRepository import ILikeRepository
from flask import current_app
from typing import Optional, List

class LikeRepository(BaseRepository[Like], ILikeRepository):
    def __init__(self):
        super().__init__(Like)
    
    def get_by_user_and_post(self, user_id: int, post_id: int) -> Optional[Like]:
        """Get like by user_id and post_id"""
        try:
            return self.model.query.filter_by(user_id=user_id, post_id=post_id).first()
        except Exception as e:
            current_app.logger.error(f"Error getting like by user and post: {str(e)}")
            raise
    
    def get_user_liked_post_ids(self, user_id: int, post_ids: Optional[List[int]] = None) -> List[int]:
        """Get IDs of posts liked by a specific user"""
        try:
            query = self.model.query.filter_by(user_id=user_id)
            if post_ids:
                query = query.filter(self.model.post_id.in_(post_ids))
            likes = query.all()
            return [like.post_id for like in likes]
        except Exception as e:
            current_app.logger.error(f"Error getting user liked post IDs: {str(e)}")
            raise
        
    def count_likes_for_post(self, post_id: int) -> int:
        """Count likes for a specific post"""
        try:
            return self.model.query.filter_by(post_id=post_id).count()
        except Exception as e:
            current_app.logger.error(f"Error counting likes for post: {str(e)}")
            raise