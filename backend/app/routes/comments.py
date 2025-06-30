from flask import Blueprint
from app.controllers.comment_controller import CommentController

comments_bp = Blueprint("comments", __name__)
comment_controller = CommentController()

comments_bp.route("/comments/create/<int:post_id>", methods=["POST"])(comment_controller.create_comment)
comments_bp.route("/comments/<int:post_id>", methods=["GET"])(comment_controller.get_comments_by_post)

# Get post images 
comments_bp.route('/comments/comment_uploads/<filename>', methods=['GET'])(comment_controller.get_comment_image)