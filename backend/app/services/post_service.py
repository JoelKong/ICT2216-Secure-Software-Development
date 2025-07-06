from app.interfaces.services.IPostService import IPostService
from app.interfaces.repositories.IPostRepository import IPostRepository
from app.interfaces.repositories.ILikeRepository import ILikeRepository
from app.interfaces.repositories.IUserRepository import IUserRepository
from app.repositories.post_repository import PostRepository
from app.repositories.like_repository import LikeRepository
from app.repositories.user_repository import UserRepository
from flask import current_app, send_from_directory
from typing import Dict, List, Optional, Any, Tuple
import os
import time
import magic

ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

class PostService(IPostService):
    def __init__(self, user_repository: IUserRepository = None, post_repository: IPostRepository = None, like_repository: ILikeRepository = None):
        self.post_repository = post_repository or PostRepository()
        self.like_repository = like_repository or LikeRepository()
        self.user_repository = user_repository or UserRepository()
        self.UPLOAD_FOLDER = '/data/post_uploads'
    
    def _is_allowed_file(self, filename: str) -> bool:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    def _is_valid_mime(self, file) -> bool:
        file.seek(0)
        mime = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)
        return mime in ALLOWED_MIME_TYPES

    def _is_valid_size(self, file) -> bool:
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        return size <= MAX_FILE_SIZE

    def get_posts(self, sort_by: str = 'recent', offset: int = 0, limit: int = 10,
                search: Optional[str] = None, user_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            posts = self.post_repository.get_posts(
                sort_by=sort_by,
                limit=limit,
                offset=offset,
                search=search,
                user_id=user_id
            )
            
            # Format response
            formatted_posts = []
            for post in posts:
                formatted_post = {
                    "post_id": post.post_id,
                    "title": post.title,
                    "content": post.content,
                    "created_at": post.created_at.isoformat(),
                    "updated_at": post.updated_at.isoformat() if post.updated_at else None,
                    "user_id": post.user_id,
                    "username": post.user.username,
                    "profile_picture": post.user.profile_picture,
                    "image": post.image,
                    "likes": post.likes_count if hasattr(post, 'likes_count') else 0,
                    "comments": post.comments_count if hasattr(post, 'comments_count') else 0
                }
                formatted_posts.append(formatted_post)
            
            result = {
                "posts": formatted_posts,
                "offset": offset,
                "limit": limit,
                "has_more": len(posts) == limit
            }
            current_app.logger.info(f"Retrieved {len(posts)} posts for offset {offset}")
            return result
        except Exception as e:
            current_app.logger.error(f"Error getting posts: {str(e)}")
            raise
    
    def toggle_like(self, post_id: int, user_id: int) -> Tuple[Dict[str, Any], Optional[str]]:
        """Toggle like status for a post"""
        try:
            # Get post
            post = self.post_repository.get_by_id(post_id)
            if not post:
                current_app.logger.warning(f"Like attempt on non-existent post {post_id}")
                return None, "Post not found"
                
            # Check if user already liked this post
            existing_like = self.like_repository.get_by_user_and_post(user_id, post_id)
            
            if existing_like:
                # Remove like
                self.like_repository.delete(existing_like)
                current_app.logger.info(f"User {user_id} unliked post {post_id}")
            else:
                # Add like
                self.like_repository.create({
                    'post_id': post_id,
                    'user_id': user_id
                })
                current_app.logger.info(f"User {user_id} liked post {post_id}")
                
            # Count likes
            likes_count = self.like_repository.count_likes_for_post(post_id)
            
            return {"likes": likes_count}, None
            
        except Exception as e:
            current_app.logger.error(f"Error toggling like: {str(e)}")
            raise
    
    def delete_post(self, post_id: int, user_id: int) -> Tuple[bool, str]:
        """Delete a post if user is authorized"""
        try:
            # Get post
            post = self.post_repository.get_by_id(post_id)
            if not post:
                current_app.logger.warning(f"Delete attempt on non-existent post {post_id}")
                return False, "Post not found"
            
            # Check if user is authorized to delete this post
            if post.user_id != user_id:
                current_app.logger.warning(f"Unauthorized delete attempt on post {post_id} by user {user_id}")
                return False, "Unauthorized: You can only delete your own posts"
            
            # Delete likes and comments related to this post first
            self.like_repository.delete_by_post_id(post_id)
            
            # Now delete the post
            self.post_repository.delete(post)
            
            current_app.logger.info(f"Post {post_id} deleted by user {user_id}")
            return True, "Post deleted successfully"
            
        except Exception as e:
            current_app.logger.error(f"Error deleting post: {str(e)}")
            raise
    
    # Get posts liked by a specific user
    def get_user_liked_posts(self, user_id: int, post_ids: Optional[List[int]] = None) -> List[int]:
        """Get IDs of posts liked by a specific user"""
        try:
            return self.like_repository.get_user_liked_post_ids(user_id, post_ids)
        except Exception as e:
            current_app.logger.error(f"Error getting user liked posts: {str(e)}")
            return []
        
    def get_post_detail(self, post_id: int, current_user_id: int) -> Optional[Dict[str, Any]]:
        try:
            post = self.post_repository.get_post_by_id(post_id)
            if not post:
                return None
            
            # Check if current user liked the post
            liked_post_ids = self.get_user_liked_posts(current_user_id, [post_id])
            liked = post_id in liked_post_ids
            
            return {
                "post_id": post.post_id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at.isoformat(),
                "updated_at": post.updated_at.isoformat() if post.updated_at else None,
                "user_id": post.user_id,
                "username": post.user.username,
                "profile_picture": post.user.profile_picture,
                "likes": post.likes_count if hasattr(post, 'likes_count') else 0,
                "comments": post.comments_count if hasattr(post, 'comments_count') else 0,
                "liked": liked,
                "image": post.image
            }
        except Exception as e:
            current_app.logger.error(f"Error getting post detail {post_id}: {str(e)}")
            raise

    def create_post(self, title: str, content: str, image_file, user_id: int):
        try:
            image_url = None

            if image_file and image_file.filename:
                # Validate file extension
                if not self._is_allowed_file(image_file.filename):
                    raise ValueError("File type not allowed")
                
                if not self._is_valid_mime(image_file):
                    raise ValueError("Invalid file content")
            
                if not self._is_valid_size(image_file):
                    raise ValueError("File too large")
                
                # Generate unique filename
                filename = f"user_{user_id}_{int(time.time())}.{image_file.filename.rsplit('.', 1)[1].lower()}"
                filepath = os.path.join(self.UPLOAD_FOLDER, filename)

                # Create uploads directory if it doesn't exist
                os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)

                # Save image
                image_file.save(filepath)
                image_url = f"/post_uploads/{filename}"
                current_app.logger.info(f"Image saved at {filepath}")

            # Save post using repository
            return self.post_repository.create_post(title, content, image_url, user_id)

        except Exception as e:
            current_app.logger.error(f"Failed to create post: {str(e)}")
            raise

    def edit_post(self, post_id: int, user_id: int, title: str, content: str, image_file=None):
        """Update an existing post"""
        try:
            post = self.post_repository.get_by_id(post_id)
            if not post:
                current_app.logger.warning(f"Post {post_id} not found for update.")
                return None

            if post.user_id != user_id:
                current_app.logger.warning(f"User {user_id} unauthorized to update post {post_id}.")
                return None

            image_url = post.image  # Default to existing image
            if image_file and image_file.filename:
                # Validate file
                if not self._is_allowed_file(image_file.filename):
                    raise ValueError("File type not allowed")
                # Yan Cong this part not tested but should work, cause the edit not working
                if not self._is_valid_mime(image_file):
                    raise ValueError("Invalid file content")
            
                if not self._is_valid_size(image_file):
                    raise ValueError("File too large")

                # Generate new filename
                filename = f"user_{user_id}_{int(time.time())}.{image_file.filename.rsplit('.', 1)[1].lower()}"
                filepath = os.path.join(self.UPLOAD_FOLDER, filename)

                # Ensure upload folder exists
                os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)

                # Save file
                image_file.save(filepath)
                image_url = f"/post_uploads/{filename}"
                current_app.logger.info(f"Updated image saved at {filepath}")

            # Call repository update method
            return self.post_repository.edit_post(
                post_id=post_id,
                title=title,
                content=content,
                image_url=image_url
            )

        except Exception as e:
            current_app.logger.error(f"Error updating post {post_id}: {str(e)}")
            raise

    def get_post_image(self, filename):
        """Serve post image from post_uploads folder"""
        try:
            # Security check - prevent directory traversal
            if '..' in filename or filename.startswith('/'):
                raise ValueError("Invalid filename")
                
            return send_from_directory(self.UPLOAD_FOLDER, filename)
        except Exception as e:
            current_app.logger.error(f"Error serving file {filename}: {str(e)}")
            raise

    def has_reached_daily_post_limit(self, user_id: int) -> bool:
        """Check if user has reached the daily post limit."""
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                current_app.logger.warning(f"Profile request for non-existent user {user_id}")
                return None, "User not found"
                
            # Format response
            user_membership = user.membership
            # Determine daily post limit based on membership
            if user_membership == "basic":
                daily_post_limit = 3
            else:
                daily_post_limit = None  # no limit
            
            # If unlimited, just return success with no limit info
            if daily_post_limit is None:
                return False
            else:
                post_count = self.post_repository.count_user_posts_today(user_id)
                return post_count >= daily_post_limit
            
        except Exception as e:
            current_app.logger.error(f"Error checking post limit for user {user_id}: {str(e)}")
            raise