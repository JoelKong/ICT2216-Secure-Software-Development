from .base_repository import BaseRepository
from app.models.posts import Post
from app.models.users import User
from app.models.likes import Like
from app.models.comments import Comment
from flask import current_app
from sqlalchemy import func, desc, distinct

class PostRepository(BaseRepository):
    def __init__(self):
        super().__init__(Post)
        
    def get_posts(self, sort_by='recent', limit=10, offset=0, search=None, user_id=None):
        """Get posts with filtering, sorting and pagination"""
        try:
            # Define sort criteria
            sort_map = {
                'recent': Post.updated_at.desc(),
                'likes': func.count(Like.post_id).desc(),
                'comments': func.count(Comment.comment_id).desc()
            }
            sort_criteria = sort_map.get(sort_by, Post.updated_at.desc())
            
            # Build query
            query = self.db.session.query(
                Post,
                User,
                func.count(distinct(Comment.comment_id)).label("comment_count"),
                func.count(distinct(Like.like_id)).label("like_count")
            )\
            .join(User, Post.user_id == User.user_id)\
            .outerjoin(Comment, Post.post_id == Comment.post_id)\
            .outerjoin(Like, Post.post_id == Like.post_id)\
            .group_by(Post.post_id, User.user_id)
            
            # Apply filters if provided
            if search:
                query = query.filter(Post.title.ilike(f'%{search}%'))
            if user_id:
                query = query.filter(Post.user_id == user_id)
                
            # Apply sorting and pagination
            query = query.order_by(sort_criteria, Post.post_id.desc())\
                .offset(offset)\
                .limit(limit)
                
            current_app.logger.info(f"Fetching posts with sort: {sort_by}, limit: {limit}, offset: {offset}")
            return query.all()
            
        except Exception as e:
            current_app.logger.error(f"Error retrieving posts: {str(e)}")
            raise
            
    def get_user_liked_posts(self, user_id, post_ids=None):
        """Get posts liked by a specific user"""
        try:
            query = Like.query.filter(Like.user_id == user_id)
            if post_ids:
                query = query.filter(Like.post_id.in_(post_ids))
                
            return query.all()
        except Exception as e:
            current_app.logger.error(f"Error retrieving liked posts: {str(e)}")
            raise