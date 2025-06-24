import os
from app.interfaces.services.IProfileService import IProfileService
from app.interfaces.repositories.IUserRepository import IUserRepository
from app.interfaces.repositories.IPostRepository import IPostRepository
from app.repositories.user_repository import UserRepository
from app.repositories.post_repository import PostRepository
from flask import current_app
from app.utils.validation import is_valid_email
from typing import Dict, Tuple, Any, Optional, List
from werkzeug.security import generate_password_hash

class ProfileService(IProfileService):
    def __init__(self, user_repository: IUserRepository = None, post_repository: IPostRepository = None):
        self.user_repository = user_repository or UserRepository()
        self.post_repository = post_repository or PostRepository()
    
    def get_user_profile(self, user_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Get user profile data"""
        try:
            # Get user from repository
            user = self.user_repository.get_by_id(user_id)
            if not user:
                current_app.logger.warning(f"Profile request for non-existent user {user_id}")
                return None, "User not found"
                
            # Format response
            user_data = {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "profile_picture": user.profile_picture,
                "membership": user.membership,
                "created_at": user.created_at
            }
            
            current_app.logger.info(f"Retrieved profile for user: {user_id}")
            return user_data, None
            
        except Exception as e:
            current_app.logger.error(f"Error fetching user profile: {str(e)}")
            raise
    
    def update_profile(self, user_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Update user profile"""
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                current_app.logger.warning(f"Profile update attempt for non-existent user {user_id}")
                return None, "User not found"
            
            # Validate data
            profile_data = {}
            if 'email' in data:
                email = data['email']
                if not is_valid_email(email):
                    return None, "Invalid email format"
                
                # Check if email is already in use by another user
                if email != user.email and self.user_repository.check_email_exists(email):
                    return None, "Email is already in use"
                
                profile_data['email'] = email
            
            if 'username' in data:
                username = data['username']
                if len(username) < 3:
                    return None, "Username must be at least 3 characters"
                
                # Check if username is already in use by another user
                if username != user.username and self.user_repository.check_username_exists(username):
                    return None, "Username is already in use"
                
                profile_data['username'] = username

            if 'password' in data:
                hashed_password = generate_password_hash(data['password'])
                profile_data['password'] = hashed_password
            
            # if 'profile_picture' in data:
            #     profile_data['profile_picture'] = data['profile_picture']
            
            # Update user profile
            updated_user = self.user_repository.update(user, profile_data)
            if not updated_user:
                current_app.logger.warning(f"Failed to update profile for user: {user_id}")
                return None, "Failed to update profile"
                
            # Format response
            user_data = {
                "user_id": updated_user.user_id,
                "username": updated_user.username,
                "email": updated_user.email,
                "password": updated_user.password,
                "profile_picture": updated_user.profile_picture,
                "membership": updated_user.membership
            }
            
            current_app.logger.info(f"Profile updated for user: {user_id}")
            return user_data, None
            
        except Exception as e:
            current_app.logger.error(f"Error updating profile: {str(e)}")
            raise

    # def update_profile_picture(self, user_id: int, file) -> Tuple[Optional[str], Optional[str]]:
    #     """Update profile picture"""
    #     try:
    #         # Validate file
    #         if not file or file.filename == '':
    #             return None, "No selected file"
                
    #         if not self._is_allowed_file(file.filename):
    #             return None, "File type not allowed"
            
    #         # Secure filename and create save path
    #         filename = file.filename
    #         filepath = os.path.join(self.UPLOAD_FOLDER, filename)
    #         #current_app.logger.info(f"Saved profile picture to: {filepath}")

    #         os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
    #         # Save file
    #         file.save(filepath)
    #         current_app.logger.info(f"Saved profile picture to: {filepath}")
            
    #         # Update database with relative path
    #         relative_path = f"/{filename}"
    #         self.user_repository.update_profile_picture(user_id, relative_path)
            
    #         return relative_path, None
            
    #     except Exception as e:
    #         # Clean up file if saved but DB update failed
    #         if 'filepath' in locals() and os.path.exists(filepath):
    #             try:
    #                 os.remove(filepath)
    #             except OSError as cleanup_error:
    #                 current_app.logger.error(f"Cleanup failed: {str(cleanup_error)}")
                    
    #         current_app.logger.error(f"Profile picture upload failed: {str(e)}")
    #         raise

    
    
    def delete_user_profile(self, user_id: int) -> Tuple[bool, Optional[str]]:
        """Delete user profile and related data"""
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                return False, "User not found"
                
            # # Delete profile picture if exists
            # if user.profile_picture:
            #     try:
            #         filepath = os.path.join(self.UPLOAD_FOLDER, user.profile_picture.split('/')[-1])
            #         if os.path.exists(filepath):
            #             os.remove(filepath)
            #     except OSError as e:
            #         current_app.logger.error(f"Failed to delete profile picture: {str(e)}")
            
            # Delete user from database
            self.user_repository.delete(user)
            return True, None
            
        except Exception as e:
            current_app.logger.error(f"Error deleting user: {str(e)}")
            return False, str(e)
    
    def get_user_posts(self, user_id: int, sort_by: str = 'recent', 
                       limit: int = 10, offset: int = 0) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """Get posts created by user"""
        try:
            # Check if user exists
            user = self.user_repository.get_by_id(user_id)
            if not user:
                current_app.logger.warning(f"Posts request for non-existent user {user_id}")
                return [], "User not found"
            
            # Get posts from repository
            posts = self.post_repository.get_posts(
                sort_by=sort_by,
                limit=limit,
                offset=offset,
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
                    "likes": post.likes_count if hasattr(post, 'likes_count') else 0,
                    "comments": post.comments_count if hasattr(post, 'comments_count') else 0
                }
                formatted_posts.append(formatted_post)
            
            current_app.logger.info(f"Retrieved {len(posts)} posts for user: {user_id}")
            return formatted_posts, None
            
        except Exception as e:
            current_app.logger.error(f"Error getting user posts: {str(e)}")
            raise