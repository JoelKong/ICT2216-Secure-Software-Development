import re
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.services.comment_service import CommentService
from app.interfaces.services.ICommentService import ICommentService
from app.utils.validation import is_valid_id

# --- Validation constants & regexes ---
INT_REGEX          = r"^[1-9]\d*$"          # positive integers (no leading zero)
MAX_CONTENT_LENGTH = 500                    # max characters in a comment
ALLOWED_IMAGE_EXTS  = {"png", "jpg", "jpeg", "gif"}
FILENAME_REGEX     = r"^[A-Za-z0-9_\-]+\.(?:png|jpg|jpeg|gif)$"

class CommentController:
    def __init__(self, comment_service: ICommentService = None):
        self.comment_service = comment_service or CommentService()

    @jwt_required()
    def get_comments_by_post(self, post_id):
        """GET /posts/<post_id>/comments"""
        try:
            # Validate post_id is a positive integer
            if not is_valid_id(post_id):
                return jsonify({"error": "Invalid post ID"}), 400

            comments = self.comment_service.get_comments_by_post(int(post_id))
            return jsonify({"comments": comments}), 200

        except Exception as e:
            current_app.logger.error(
                f"Error fetching comments for post {post_id}: {e}"
            )
            return jsonify({"error": "Internal server error"}), 500

    @jwt_required()
    def create_comment(self, post_id):
        """POST /posts/<post_id>/comments"""
        try:
            user_id = get_jwt_identity()

            # Validate post_id
            if not re.match(INT_REGEX, str(post_id)):
                return jsonify({"error": "Invalid post ID"}), 400
            post_id = int(post_id)

            # Get and sanitize content
            content = (request.form.get("content") or "").strip()
            if not content:
                return jsonify({"error": "Content is required"}), 400
            if len(content) > MAX_CONTENT_LENGTH:
                return jsonify({
                    "error": f"Content must be ≤ {MAX_CONTENT_LENGTH} characters."
                }), 400

            # Validate optional parent_id
            parent_raw = request.form.get("parent_id", None)
            parent_id = None
            if parent_raw:
                if not is_valid_id(parent_raw):
                    return jsonify({"error": "Invalid parent comment ID"}), 400
                parent_id = int(parent_raw)

            # Validate optional image upload
            image_file = request.files.get("image")
            if image_file:
                filename = secure_filename(image_file.filename or "")
                ext = filename.rsplit(".", 1)[-1].lower()
                if ext not in ALLOWED_IMAGE_EXTS:
                    return jsonify({
                        "error": f"Invalid image type; must be one of {', '.join(ALLOWED_IMAGE_EXTS)}."
                    }), 400

            comment = self.comment_service.create_comment(
                post_id=post_id,
                user_id=user_id,
                content=content,
                parent_id=parent_id,
                image_file=image_file
            )
            return jsonify({
                "message": "Comment created",
                "comment_id": comment.comment_id
            }), 201

        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            current_app.logger.error(f"Error creating comment: {e}")
            return jsonify({"error": "Internal server error"}), 500

    def get_comment_image(self, filename):
        # Validate filename to prevent path traversal
        if not re.match(FILENAME_REGEX, filename):
            return jsonify({"error": "Invalid image filename"}), 400

        return self.comment_service.get_comment_image(filename)