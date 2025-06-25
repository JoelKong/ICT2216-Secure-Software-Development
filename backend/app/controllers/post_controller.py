from flask import request, jsonify, current_app
from app.interfaces.services.IPostService import IPostService
from app.services.post_service import PostService
from flask_jwt_extended import jwt_required, get_jwt_identity

class PostController:
    def __init__(self, post_service: IPostService = None):
        self.post_service = post_service or PostService()
    
    @jwt_required()
    def fetch_posts(self):
        """Get posts with filtering, pagination and sorting"""
        try:
            # Get query parameters
            sort_by = request.args.get('sort_by', 'recent')
            page = int(request.args.get('page', 1))
            search = request.args.get('search', None)
            user_id = request.args.get('user_id', None)
            if user_id:
                user_id = int(user_id)
            
            # Get current user ID from JWT
            current_user_id = get_jwt_identity()
            
            # Get posts
            result = self.post_service.get_posts(
                sort_by=sort_by,
                page=page,
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

    # Create posts
    # @jwt_required()
    # def create_post(self):
    #     """Create a new post"""
    #     try:
    #         data = request.get_json()
            
    #         if not data:
    #             return jsonify({"error": "No data provided"}), 400
            
    #         # Get required fields
    #         title = data.get('title')
    #         content = data.get('content')
            
    #         # Validate required fields
    #         if not title or not content:
    #             return jsonify({"error": "Title and content are required"}), 400
            
    #         # Get user ID from token
    #         user_id = get_jwt_identity()
            
    #         # Create post
    #         new_post = self.post_repository.create({
    #             'user_id': user_id,
    #             'title': title,
    #             'content': content,
    #             'image': data.get('image')
    #         })
            
    #         return jsonify({
    #             "message": "Post created successfully",
    #             "post_id": new_post.post_id
    #         }), 201
            
    #     except Exception as e:
    #         current_app.logger.error(f"Error creating post: {str(e)}")
    #         return jsonify({"error": "Internal server error"}), 500