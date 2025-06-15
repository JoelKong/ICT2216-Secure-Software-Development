from flask import request, jsonify, current_app
from app.services.post_service import PostService
from flask_jwt_extended import jwt_required, get_jwt_identity

class PostController:
    def __init__(self):
        self.post_service = PostService()
        
    @jwt_required()
    def fetch_posts(self):
        """Get posts with filtering, sorting and pagination"""
        try:
            user_id = get_jwt_identity()
            
            sort_by = request.args.get('sort_by', 'recent')
            limit = min(int(request.args.get('limit', 10)), 50)
            offset = int(request.args.get('offset', 0))
            search = request.args.get('search', '').strip()
            filter_user_id = request.args.get('user_id', '').strip()
            
            current_app.logger.info(f"User {user_id} fetching posts: sort={sort_by}, limit={limit}, offset={offset}")
            
            result = self.post_service.get_posts(
                user_id=user_id,
                sort_by=sort_by,
                limit=limit,
                offset=offset,
                search=search,
                filter_user_id=filter_user_id
            )
            
            return jsonify(result), 200
            
        except ValueError as e:
            current_app.logger.warning(f"Invalid request parameters: {str(e)}")
            return jsonify({"error": "Invalid parameters"}), 400
        except Exception as e:
            current_app.logger.error(f"Error fetching posts: {str(e)}")
            return jsonify({"error": "Failed to fetch posts"}), 500
            
    @jwt_required()
    def toggle_like(self, post_id):
        """Toggle like status for a post"""
        try:
            user_id = get_jwt_identity()
            current_app.logger.info(f"User {user_id} toggling like on post {post_id}")
            
            result, error = self.post_service.toggle_like(post_id, user_id)
            
            if error:
                return jsonify({"error": error}), 404
                
            return jsonify(result), 200
            
        except Exception as e:
            current_app.logger.error(f"Error toggling like: {str(e)}")
            return jsonify({"error": "Could not update like status"}), 500
            
    @jwt_required()
    def delete_post(self, post_id):
        """Delete a post"""
        try:
            user_id = get_jwt_identity()
            current_app.logger.info(f"User {user_id} attempting to delete post {post_id}")
            
            success, message = self.post_service.delete_post(post_id, user_id)
            
            if not success:
                if message == "Post not found":
                    return jsonify({"error": message}), 404
                else:
                    return jsonify({"error": message}), 403
                    
            return jsonify({"message": message}), 200
            
        except Exception as e:
            current_app.logger.error(f"Error deleting post: {str(e)}")
            return jsonify({"error": "Could not delete post"}), 500