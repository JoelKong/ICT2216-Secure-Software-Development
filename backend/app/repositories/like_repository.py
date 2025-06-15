from .base_repository import BaseRepository
from app.models.likes import Like
from flask import current_app

class LikeRepository(BaseRepository):
    def __init__(self):
        super().__init__(Like)
        
    def get_by_post_and_user(self, post_id, user_id):
        """Find like by post ID and user ID"""
        try:
            return Like.query.filter_by(
                post_id=post_id, 
                user_id=user_id
            ).first()
        except Exception as e:
            current_app.logger.error(f"Error retrieving like for post {post_id} by user {user_id}: {str(e)}")
            raise
            
    def count_likes_for_post(self, post_id):
        """Count likes for a specific post"""
        try:
            return Like.query.filter_by(post_id=post_id).count()
        except Exception as e:
            current_app.logger.error(f"Error counting likes for post {post_id}: {str(e)}")
            raise