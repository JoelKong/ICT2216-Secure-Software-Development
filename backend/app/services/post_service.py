from app.interfaces.services.IPostService import IPostService
from app.interfaces.repositories.IPostRepository import IPostRepository
from app.interfaces.repositories.ILikeRepository import ILikeRepository
from app.repositories.post_repository import PostRepository
from app.repositories.like_repository import LikeRepository
from flask import current_app
from typing import Dict, List, Optional, Any, Tuple

class PostService(IPostService):
    def __init__(self, post_repository: IPostRepository = None, like_repository: ILikeRepository = None):
        self.post_repository = post_repository or PostRepository()
        self.like_repository = like_repository or LikeRepository()
    
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
    
    # Get posts created by a specific user
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
