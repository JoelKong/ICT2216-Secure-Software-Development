from flask import Blueprint
from app.controllers.post_controller import PostController
from app.services.post_service import PostService
#Added to enable rate limiting
from app.extensions import limiter

posts_bp = Blueprint('posts', __name__)

# Create service instance with dependency injection
post_service = PostService()

# Create controller with injected service
post_controller = PostController(post_service=post_service)

# Fetch posts route
posts_bp.route('/posts', methods=['GET'])(post_controller.fetch_posts)

# Create post route
posts_bp.route('/posts/create', methods=['POST'])(post_controller.create_post)

# Edit post route
posts_bp.route('/posts/edit/<int:post_id>', methods=['PUT'])(post_controller.edit_post)

# Fetch post route for editing
posts_bp.route('/posts/<int:post_id>/edit', methods=['GET'])(post_controller.get_post_for_edit)

# Delete post route
# Rate limited to prevent abuse or any mass deletions (max 3 delete requests/minute per user/IP)
@posts_bp.route('/posts/delete/<int:post_id>', methods=['DELETE'])
@limiter.limit("3 per minute")
def delete_post(post_id):
    return post_controller.delete_post(post_id)

# Toggle like route
posts_bp.route('/posts/like/<int:post_id>', methods=['POST'])(post_controller.toggle_like)

# Get post detail
posts_bp.route('/posts/<int:post_id>', methods=['GET'])(post_controller.get_post_detail)

# Get post images 
posts_bp.route('/posts/post_uploads/<filename>', methods=['GET'])(post_controller.get_post_image)

# Summarize post
posts_bp.route('/posts/summary/<int:post_id>', methods=['GET'])(post_controller.summarize_post)

posts_bp.route('/posts/limit/', methods=['GET'])(post_controller.get_user_post_limit)