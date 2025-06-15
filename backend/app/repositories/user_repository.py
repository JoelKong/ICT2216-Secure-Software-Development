from .base_repository import BaseRepository
from app.models.users import User
from flask import current_app

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
        
    def get_by_email(self, email):
        """Find user by email"""
        try:
            return User.query.filter_by(email=email).first()
        except Exception as e:
            current_app.logger.error(f"Error retrieving user by email: {str(e)}")
            raise
    
    def get_by_username(self, username):
        """Find user by username"""
        try:
            return User.query.filter_by(username=username).first()
        except Exception as e:
            current_app.logger.error(f"Error retrieving user by username: {str(e)}")
            raise
            
    def update_membership(self, user_id, new_membership):
        """Update user membership"""
        try:
            user = self.get_by_id(user_id)
            if user:
                user.membership = new_membership
                self.db.session.commit()
                current_app.logger.info(f"User {user_id} membership updated to {new_membership}")
                return user
            return None
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"Error updating user membership: {str(e)}")
            raise