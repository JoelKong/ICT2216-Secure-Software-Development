from .base_repository import BaseRepository
from app.models.comments import Comment
from app.models.users import User
from app.interfaces.repositories.ICommentRepository import ICommentRepository
from flask import current_app
from typing import List

class CommentRepository(BaseRepository[Comment], ICommentRepository):
    def __init__(self):
        super().__init__(Comment)
    
    def get_by_post_id(self, post_id: int) -> List[Comment]:
        try:
            # query with join but load Comment objects
            results = (
                self.db.session.query(Comment, User.username)
                .join(User, Comment.user_id == User.user_id)
                .filter(Comment.post_id == post_id)
                .order_by(Comment.created_at.asc())
                .all()
            )

            comments = []
            for comment, username in results:
                comment.username = username  # dynamically attach username
                comments.append(comment)
            return comments
        except Exception as e:
            print(f"Error getting comments with usernames: {e}")
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