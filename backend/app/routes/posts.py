from flask import Blueprint
from app.controllers.post_controller import PostController
from app.services.post_service import PostService

posts_bp = Blueprint('posts', __name__)

# Create service instance with dependency injection
post_service = PostService()

# Create controller with injected service
post_controller = PostController(post_service=post_service)

# Fetch posts route
posts_bp.route('/posts', methods=['GET'])(post_controller.fetch_posts)

# Create post route
posts_bp.route('/posts/create', methods=['POST'])(post_controller.create_post)

# Delete post route
posts_bp.route('/posts/delete/<int:post_id>', methods=['DELETE'])(post_controller.delete_post)

# Toggle like route
posts_bp.route('/posts/like/<int:post_id>', methods=['POST'])(post_controller.toggle_like)

posts_bp.route('/posts/<int:post_id>', methods=['GET'])(post_controller.get_post_detail)

# Get post images 
posts_bp.route('/posts/post_uploads/<filename>', methods=['GET'])(post_controller.get_post_image)