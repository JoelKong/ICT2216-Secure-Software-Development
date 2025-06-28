from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.comment_service import CommentService
from app.interfaces.services.ICommentService import ICommentService

class CommentController:
    def __init__(self, comment_service: ICommentService = None):
        self.comment_service = comment_service or CommentService()

    @jwt_required()
    def get_comments_by_post(self, post_id):
        try:
            comments = self.comment_service.get_comments_by_post(post_id)
            return jsonify({"comments": comments}), 200
        except Exception as e:
            current_app.logger.error(f"Error fetching comments for post {post_id}: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    @jwt_required()
    def create_comment(self, post_id):
        try:
            user_id = get_jwt_identity()
            content = request.form.get("content")
            parent_id = request.form.get("parent_id", None)
            if parent_id:
                parent_id = int(parent_id)
            image_file = request.files.get("image")

            if not content:
                return jsonify({"error": "Content is required"}), 400

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
            current_app.logger.error(f"Error creating comment: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
        
    def get_comment_image(self, filename):
        """Handle GET request for comment images"""
        return self.comment_service.get_comment_image(filename)