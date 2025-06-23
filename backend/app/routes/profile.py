from flask import Blueprint
from app.controllers.profile_controller import ProfileController
from app.services.profile_service import ProfileService

profile_bp = Blueprint('profile', __name__)

# Create service instance
profile_service = ProfileService()

# Create controller with injected service
profile_controller = ProfileController(profile_service=profile_service)

# Get user profile
profile_bp.route('/profile', methods=['GET'])(profile_controller.get_profile)

# Update user profile
profile_bp.route('/profile', methods=['PUT'])(profile_controller.update_profile)

# Upload profile picture
#profile_bp.route('/profile/picture', methods=['POST'])(profile_controller.update_profile_picture)

# Delete user profile
profile_bp.route('/profile', methods=['DELETE'])(profile_controller.delete_profile)

# Get user's posts
profile_bp.route('/profile/posts', methods=['GET'])(profile_controller.get_user_posts)

