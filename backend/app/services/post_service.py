from app.repositories.post_repository import PostRepository
from app.repositories.like_repository import LikeRepository
from flask import current_app

class PostService:
    def __init__(self):
        self.post_repository = PostRepository()
        self.like_repository = LikeRepository()
    
    def get_posts(self, user_id, sort_by='recent', limit=10, offset=0, search=None, filter_user_id=None):
        """Get posts with all necessary data"""
        try:
            # Get posts with sorting and filtering
            posts_data = self.post_repository.get_posts(
                sort_by=sort_by,
                limit=limit,
                offset=offset,
                search=search,
                user_id=filter_user_id
            )
            
            # Extract post IDs
            post_ids = [post.post_id for post, _, _, _ in posts_data]
            
            # Get current user's liked posts
            liked_posts = []
            if post_ids:
                liked_posts = self.post_repository.get_user_liked_posts(user_id, post_ids)
                
            liked_post_ids = set(like.post_id for like in liked_posts)
            
            # Format posts response
            result = []
            for post, user, comment_count, like_count in posts_data:
                result.append({
                    "post_id": post.post_id,
                    "title": post.title,
                    "content": post.content,
                    "image": post.image,
                    "username": user.username,
                    "likes": like_count,
                    "comments": comment_count,
                    "created_at": post.created_at.isoformat(),
                    "updated_at": post.updated_at.isoformat() if post.updated_at else None,
                })
            
            return {
                "posts": result,
                "liked_post_ids": list(liked_post_ids)
            }
            
        except Exception as e:
            current_app.logger.error(f"Error in get_posts service: {str(e)}")
            raise
            
    def toggle_like(self, post_id, user_id):
        """Toggle like status for a post"""
        try:
            # Get post
            post = self.post_repository.get_by_id(post_id)
            if not post:
                current_app.logger.warning(f"Like attempt on non-existent post {post_id}")
                return None, "Post not found"
                
            # Check if user already liked this post
            existing_like = self.like_repository.get_by_post_and_user(post_id, user_id)
            
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
            
    def delete_post(self, post_id, user_id):
        """Delete a post"""
        try:
            post = self.post_repository.get_by_id(post_id)
            
            if not post:
                current_app.logger.warning(f"Delete attempt on non-existent post {post_id}")
                return False, "Post not found"
                
            # Verify ownership
            if int(post.user_id) != int(user_id):
                current_app.logger.warning(f"Unauthorized delete attempt on post {post_id} by user {user_id}")
                return False, "Unauthorized"
                
            # Delete post
            self.post_repository.delete(post)
            current_app.logger.info(f"Post {post_id} deleted by user {user_id}")
            
            return True, "Post deleted successfully"
            
        except Exception as e:
            current_app.logger.error(f"Error deleting post: {str(e)}")
            raise