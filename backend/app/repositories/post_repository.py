from .base_repository import BaseRepository
from app.models.posts import Post
from app.models.users import User
from app.models.likes import Like
from app.models.comments import Comment
from app.interfaces.repositories.IPostRepository import IPostRepository
from flask import current_app
from sqlalchemy import func, desc, distinct
from typing import List, Optional

class PostRepository(BaseRepository[Post], IPostRepository):
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
                func.count(distinct(Comment.comment_id)).label("comments_count"),
                func.count(distinct(Like.like_id)).label("likes_count")
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
            
            # Get results and add counts as attributes to the Post objects
            results = []
            for post_tuple in query.all():
                post, user, comments_count, likes_count = post_tuple
                post.user = user
                post.comments_count = comments_count
                post.likes_count = likes_count
                results.append(post)
            
            return results
            
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

    def get_post_by_id(self, post_id: int):
        try:
            # Query Post joined with User, and count comments and likes
            query = self.db.session.query(
                Post,
                func.count(distinct(Comment.comment_id)).label("comments_count"),
                func.count(distinct(Like.like_id)).label("likes_count"),
                User
            )\
            .join(User, Post.user_id == User.user_id)\
            .outerjoin(Comment, Post.post_id == Comment.post_id)\
            .outerjoin(Like, Post.post_id == Like.post_id)\
            .filter(Post.post_id == post_id)\
            .group_by(Post.post_id, User.user_id)
            
            result = query.first()
            if not result:
                return None
            
            post, comments_count, likes_count, user = result
            post.comments_count = comments_count
            post.likes_count = likes_count
            post.user = user
            
            return post
        
        except Exception as e:
            current_app.logger.error(f"Error retrieving post {post_id}: {str(e)}")
            raise
