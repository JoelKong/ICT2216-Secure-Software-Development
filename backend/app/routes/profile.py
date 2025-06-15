from flask import Blueprint
from app.controllers.profile_controller import ProfileController

profile_bp = Blueprint('profile', __name__)
profile_controller = ProfileController()

# Get user profile
profile_bp.route('/profile', methods=['GET'])(profile_controller.get_profile)

# Update user profile
# profile_bp.route('/profile', methods=['PUT'])(profile_controller.update_profile)

# # Get user's posts
# profile_bp.route('/profile/posts', methods=['GET'])(profile_controller.get_user_posts)