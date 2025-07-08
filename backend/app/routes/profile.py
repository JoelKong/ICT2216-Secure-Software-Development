from flask import Blueprint
from app.controllers.profile_controller import ProfileController
from app.services.profile_service import ProfileService
# Importing limiter for rate limiting
from app.extensions import limiter

# Define blueprint
profile_bp = Blueprint('profile', __name__)

# Create service instance
profile_service = ProfileService()

# Create controller with injected service
profile_controller = ProfileController(profile_service=profile_service)

# Get user profile
# Applies a rate limit to prevent scraping or abuse
limiter.limit("5 per minute")(profile_bp.route('/profile', methods=['GET'])(profile_controller.get_profile))

# Update user profile
# Applies a low rate limit to prevent abuse
limiter.limit("2 per minute")(profile_bp.route('/profile', methods=['PUT'])(profile_controller.update_profile))

# Upload profile picture
# File uploads are expensive, so we rate limit strictly
limiter.limit("3 per minute")(profile_bp.route('/profile/picture', methods=['POST'])(profile_controller.update_profile_picture))

# Delete user profile
# Sensitive operation, hence low rate
limiter.limit("2 per minute")(profile_bp.route('/profile', methods=['DELETE'])(profile_controller.delete_profile))

# Get user's posts
# Read operation, so slightly higher allowance
limiter.limit("10 per minute")(profile_bp.route('/profile/posts', methods=['GET'])(profile_controller.get_user_posts))

# Get profile images
# Allows for media loading while preventing excessive requests
limiter.limit("10 per minute")(profile_bp.route('/profile/uploads/<filename>', methods=['GET'])(profile_controller.get_profile_image))