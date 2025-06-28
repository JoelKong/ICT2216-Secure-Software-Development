from .base_repository import BaseRepository
from app.models.comments import Comment
from app.interfaces.repositories.ICommentRepository import ICommentRepository
from flask import current_app
from typing import List, Optional

class CommentRepository(BaseRepository[Comment], ICommentRepository):
    def __init__(self):
        super().__init__(Comment)
    
    def get_by_post_id(self, post_id: int) -> List[Comment]:
        """Get all comments for a specific post"""
        try:
            return self.model.query.filter_by(post_id=post_id).all()
        except Exception as e:
            current_app.logger.error(f"Error getting comments by post ID: {str(e)}")
            raise
    
    def count_by_post_id(self, post_id: int) -> int:
        """Count comments for a specific post"""
        try:
            return self.model.query.filter_by(post_id=post_id).count()
        except Exception as e:
            current_app.logger.error(f"Error counting comments by post ID: {str(e)}")
            raise
    
    def delete_by_post_id(self, post_id: int) -> None:
        """Delete all comments for a specific post"""
        try:
            comments = self.get_by_post_id(post_id)
            for comment in comments:
                self.delete(comment)
            current_app.logger.info(f"Deleted all comments for post {post_id}")
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"Error deleting comments by post ID: {str(e)}")
            raise
    
    def create_comment(self, comment: Comment) -> Comment:
        try:
            self.db.session.add(comment)
            self.db.session.commit()
            current_app.logger.info(f"Created comment with id {comment.comment_id}")
            return comment
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"Error creating comment: {str(e)}")
            raise

    def get_comment_by_id(self, comment_id: int) -> Optional[Comment]:
        try:
            return self.model.query.filter_by(comment_id=comment_id).first()
        except Exception as e:
            current_app.logger.error(f"Error getting comment by id {comment_id}: {str(e)}")
            raise