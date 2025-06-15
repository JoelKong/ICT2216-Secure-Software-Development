from flask import Blueprint
from app.controllers.post_controller import PostController

posts_bp = Blueprint('posts', __name__)
post_controller = PostController()

# Fetch posts route
posts_bp.route('/posts', methods=['GET'])(post_controller.fetch_posts)

# Delete post route
posts_bp.route('/posts/delete/<int:post_id>', methods=['DELETE'])(post_controller.delete_post)

# Toggle like route
posts_bp.route('/posts/like/<int:post_id>', methods=['POST'])(post_controller.toggle_like)