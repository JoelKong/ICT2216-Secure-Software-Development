from flask import request, jsonify, current_app
from app.interfaces.services.IPostService import IPostService
from app.services.post_service import PostService
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify

class PostController:
    def __init__(self, post_service: IPostService = None):
        self.post_service = post_service or PostService()
    
    @jwt_required()
    def fetch_posts(self):
        """Get posts with filtering, pagination and sorting"""
        try:
            sort_by = request.args.get('sort_by', 'recent')
            offset = int(request.args.get('offset', 0))  # Changed here
            limit = int(request.args.get('limit', 10))   # Optional: also read limit from query
            search = request.args.get('search', None)
            user_id = request.args.get('user_id', None)
            if user_id:
                user_id = int(user_id)

            current_user_id = get_jwt_identity()

            # Pass offset and limit instead of page
            result = self.post_service.get_posts(
                sort_by=sort_by,
                offset=offset,
                limit=limit,
                search=search,
                user_id=user_id
            )
            
            # Get user's liked posts
            post_ids = [post["post_id"] for post in result.get('posts', [])]
            liked_post_ids = self.post_service.get_user_liked_posts(current_user_id, post_ids)
            
            # Include liked post IDs in the response
            result['liked_post_ids'] = liked_post_ids
            
            return jsonify(result), 200
            
        except ValueError as e:
            current_app.logger.warning(f"Invalid query parameter: {str(e)}")
            return jsonify({"error": "Invalid query parameter"}), 400
            
        except Exception as e:
            current_app.logger.error(f"Error getting posts: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    @jwt_required()
    def toggle_like(self, post_id):
        """Toggle like status for a post"""
        try:
            # Get current user ID from JWT
            user_id = get_jwt_identity()
            
            # Toggle like
            result, error = self.post_service.toggle_like(post_id, user_id)
            
            if error:
                return jsonify({"error": error}), 404
                
            return jsonify(result), 200
            
        except Exception as e:
            current_app.logger.error(f"Error toggling like: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    @jwt_required()
    def delete_post(self, post_id):
        """Delete a post"""
        try:
            # Get current user ID from JWT
            user_id = get_jwt_identity()
            
            # Delete post
            success, message = self.post_service.delete_post(int(post_id), int(user_id))
            
            if not success:
                return jsonify({"error": message}), 403
                
            return jsonify({"message": message}), 200
            
        except Exception as e:
            current_app.logger.error(f"Error deleting post: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    @jwt_required()
    def get_post_detail(self, post_id):
        try:
            current_user_id = get_jwt_identity()
            post_detail = self.post_service.get_post_detail(post_id, current_user_id)
            if not post_detail:
                return jsonify({"error": "Post not found"}), 404
            
            return jsonify(post_detail), 200
        except Exception as e:
            current_app.logger.error(f"Error fetching post detail: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    @jwt_required()
    def create_post(self):
        """Handle POST request for creating a new post with optional image"""
        try:
            user_id = get_jwt_identity()
            title = request.form.get("title")
            content = request.form.get("content")
            image_file = request.files.get("image")

            if not title or not content:
                return jsonify({"error": "Title and content are required"}), 400

            post = self.post_service.create_post(
                title=title,
                content=content,
                image_file=image_file,
                user_id=user_id
            )

            return jsonify({
                "message": "Post created",
                "post_id": post.post_id
            }), 201

        except ValueError as ve:
            current_app.logger.warning(f"Validation error: {str(ve)}")
            return jsonify({"error": str(ve)}), 400

        except Exception as e:
            current_app.logger.error(f"Create post error: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    @jwt_required()
    def get_post_for_edit(self, post_id):
        try:
            current_user_id = int(get_jwt_identity())
            post = self.post_service.get_post_detail(post_id, current_user_id)

            if not post:
                return jsonify({"error": "Post not found"}), 404

            if post["user_id"] != current_user_id:
                return jsonify({"error": "Unauthorized"}), 403

            # Minimal data needed for editing
            return jsonify({
                "post_id": post["post_id"],
                "title": post["title"],
                "content": post["content"],
                "image": post["image"]
            }), 200

        except Exception as e:
            current_app.logger.error(f"Error fetching post for edit: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    @jwt_required()
    def edit_post(self, post_id):
        """Edit an existing post with optional new image"""
        try:
            user_id = int(get_jwt_identity())
            title = request.form.get("title")
            content = request.form.get("content")
            image_file = request.files.get("image")

            if not title or not content:
                return jsonify({"error": "Title and content are required"}), 400

            updated_post = self.post_service.edit_post(
                post_id=post_id,
                user_id=user_id,
                title=title,
                content=content,
                image_file=image_file
            )

            if not updated_post:
                return jsonify({"error": "Post not found or unauthorized"}), 404

            return jsonify({
                "message": "Post updated",
                "post_id": updated_post.post_id
            }), 200

        except Exception as e:
            current_app.logger.error(f"Edit post error: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    def get_post_image(self, filename):
        """Handle GET request for post images"""
        return self.post_service.get_post_image(filename)