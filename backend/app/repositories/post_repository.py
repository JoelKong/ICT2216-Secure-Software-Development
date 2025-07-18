from .base_repository import BaseRepository
from app.models.posts import Post
from app.models.users import User
from app.models.likes import Like
from app.models.comments import Comment
from app.interfaces.repositories.IPostRepository import IPostRepository
from flask import current_app
from sqlalchemy import func, distinct
from typing import Optional
from datetime import datetime, timezone
from typing import List

class PostRepository(BaseRepository[Post], IPostRepository):
    def __init__(self):
        super().__init__(Post)

    def get_posts(self, sort_by='recent', limit=10, offset=0, search=None, user_id=None) -> List[Post]:
        """Get posts with filtering, sorting and pagination"""
        try:
            # Define sort criteria as tuples (primary, tiebreaker)
            sort_map = {
                'recent': (Post.updated_at.desc(), Post.post_id.desc()),
                'likes': (func.count(distinct(Like.like_id)).desc(), Post.post_id.desc()),
                'comments': (func.count(distinct(Comment.comment_id)).desc(), Post.post_id.desc())
            }
            primary_sort, tiebreak_sort = sort_map.get(sort_by, (Post.updated_at.desc(), Post.post_id.desc()))

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
            query = query.order_by(primary_sort, tiebreak_sort)\
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

            current_app.logger.info(f"Posts returned: {[p.post_id for p in results]}")

            return results

        except Exception as e:
            current_app.logger.error(f"Error retrieving posts: {str(e)}")
            raise

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
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

    def create_post(self, title: str, content: str, image_url: Optional[str], user_id: int) -> Post:
        new_post = Post(
            title=title,
            content=content,
            image=image_url,
            user_id=user_id
        )
        self.db.session.add(new_post)
        self.db.session.commit()
        return new_post
    
    def edit_post(self, post_id: int, title: str, content: str, image_url: Optional[str]) -> Optional[Post]:
        try:
            post = self.db.session.query(Post).filter_by(post_id=post_id).first()
            if not post:
                current_app.logger.warning(f"Post {post_id} not found for update.")
                return None

            post.title = title
            post.content = content
            if image_url is not None:
                post.image = image_url

            self.db.session.commit()
            current_app.logger.info(f"Post {post_id} updated successfully.")
            return post
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"Error updating post {post_id}: {str(e)}")
            raise

    def count_user_posts_today(self, user_id: int) -> int:
        try:
            today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
            count = self.db.session.query(Post).filter(
                Post.user_id == user_id,
                Post.created_at >= today_start
            ).count()
            return count
        except Exception as e:
            current_app.logger.error(f"Error counting posts for user {user_id}: {str(e)}")
            raise