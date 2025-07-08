from .base_repository import BaseRepository
from app.models.users import User
from app.interfaces.repositories.IUserRepository import IUserRepository
from flask import current_app
from typing import Any, Optional, Dict

class UserRepository(BaseRepository[User], IUserRepository):
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            return self.model.query.filter_by(email=email).first()
        except Exception as e:
            current_app.logger.error(f"Error getting user by email: {str(e)}")
            raise
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            return self.model.query.filter_by(username=username).first()
        except Exception as e:
            current_app.logger.error(f"Error getting user by username: {str(e)}")
            raise
    
    def check_email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        try:
            return self.model.query.filter_by(email=email).first() is not None
        except Exception as e:
            current_app.logger.error(f"Error checking if email exists: {str(e)}")
            raise
    
    def check_username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        try:
            return self.model.query.filter_by(username=username).first() is not None
        except Exception as e:
            current_app.logger.error(f"Error checking if username exists: {str(e)}")
            raise

    def update_membership(self, user_id: int, is_premium: str) -> User:
        """Update user membership status"""
        try:
            user = self.get_by_id(user_id)
            if user:
                user.membership = is_premium
                self.db.session.commit()
                current_app.logger.info(f"User {user_id} membership updated to {is_premium}")
                return user
            return None
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"Error updating user membership: {str(e)}")
            raise

    def update_profile_picture(self, user_id: int, filename: str) -> None:
        """Update user profile picture"""
        try:
            user = self.get_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            user.profile_picture = filename
            self.db.session.commit()
            current_app.logger.info(f"Updated profile picture reference for user {user_id}")
            
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"Database error updating profile picture: {str(e)}")
            raise

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            return self.model.query.get(user_id)
        except Exception as e:
            current_app.logger.error(f"Error getting user by ID: {str(e)}")
            raise

    def update_totp_verified(self, user_id: int, totp_verified: bool) -> None:
        """Update TOTP verification status"""
        try:
            user = self.get_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            user.totp_verified = totp_verified
            self.db.session.commit()
            current_app.logger.info(f"Updated TOTP verification status for user {user_id}")
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"Error updating TOTP verification status: {str(e)}")
            raise