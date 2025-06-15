# THIS IS A TEMPLATE FOR RAIHAH 



from app.repositories.user_repository import UserRepository
from app.repositories.post_repository import PostRepository
from flask import current_app
from app.utils.validation import is_valid_email

class ProfileService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.post_repository = PostRepository()
    
    def get_user_profile(self, user_id):
        """Get user profile information"""
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                current_app.logger.warning(f"Profile request for non-existent user: {user_id}")
                return None, "User not found"
            
            # Format user data for response (from existing /profile route)
            user_data = {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "profile_picture": user.profile_picture,
                "membership": user.membership,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            }
            
            current_app.logger.info(f"Profile fetched for user: {user_id}")
            return user_data, None
        except Exception as e:
            current_app.logger.error(f"Error fetching profile: {str(e)}")
            raise
    
    # def update_profile(self, user_id, profile_data):
    #     """Update user profile with validation"""
    #     try:
    #         # Validate email if provided
    #         if 'email' in profile_data and not is_valid_email(profile_data['email']):
    #             current_app.logger.warning(f"Invalid email format in profile update: {profile_data.get('email')}")
    #             return None, "Invalid email format"
            
    #         # Check if username already exists if changing username
    #         if 'username' in profile_data:
    #             existing_user = self.profile_repository.get_by_username(profile_data['username'])
    #             if existing_user and existing_user.user_id != int(user_id):
    #                 current_app.logger.warning(f"Username already taken in profile update: {profile_data.get('username')}")
    #                 return None, "Username already taken"
            
    #         # Update profile
    #         updated_user = self.profile_repository.update_profile(user_id, profile_data)
    #         if not updated_user:
    #             current_app.logger.warning(f"Failed to update profile for user: {user_id}")
    #             return None, "Failed to update profile"
                
    #         # Format response
    #         user_data = {
    #             "user_id": updated_user.user_id,
    #             "username": updated_user.username,
    #             "email": updated_user.email,
    #             "profile_picture": updated_user.profile_picture,
    #             "membership": updated_user.membership
    #         }
            
    #         current_app.logger.info(f"Profile updated for user: {user_id}")
    #         return user_data, None
    #     except Exception as e:
    #         current_app.logger.error(f"Error updating profile: {str(e)}")
    #         raise

    # def get_user_posts(self, user_id, sort_by='recent', limit=10, offset=0):
    #     """Get posts by the user"""
    #     try:
    #         posts = self.post_repository.get_posts(
    #             sort_by=sort_by,
    #             limit=limit,
    #             offset=offset,
    #             user_id=user_id
    #         )
            
    #         current_app.logger.info(f"Fetched {len(posts)} posts for user {user_id}")
    #         return posts, None
    #     except Exception as e:
    #         current_app.logger.error(f"Error fetching user posts: {str(e)}")
    #         raise