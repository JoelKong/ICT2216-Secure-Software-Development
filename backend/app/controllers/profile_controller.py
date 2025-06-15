#TEMPLATE FOR RAIHAH

from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.profile_service import ProfileService

class ProfileController:
    def __init__(self):
        self.profile_service = ProfileService()
    
    @jwt_required()
    def get_profile(self):
        """Handle GET request for user profile"""
        try:
            user_id = get_jwt_identity()
            current_app.logger.info(f"Fetching profile for user: {user_id}")
            
            user_data, error = self.profile_service.get_user_profile(user_id)
            
            if error:
                return jsonify({"error": error}), 404
                
            return jsonify({"user": user_data}), 200
            
        except Exception as e:
            current_app.logger.error(f"Error in profile controller: {str(e)}")
            return jsonify({"error": "Failed to retrieve user profile"}), 500
    
    # @jwt_required()
    # def update_profile(self):
    #     """Handle PUT request to update user profile"""
    #     try:
    #         user_id = get_jwt_identity()
    #         data = request.get_json()
            
    #         if not data:
    #             return jsonify({"error": "No data provided"}), 400
                
    #         current_app.logger.info(f"Updating profile for user: {user_id}")
            
    #         updated_user, error = self.profile_service.update_profile(user_id, data)
            
    #         if error:
    #             return jsonify({"error": error}), 400
                
    #         return jsonify({"user": updated_user, "message": "Profile updated successfully"}), 200
            
    #     except Exception as e:
    #         current_app.logger.error(f"Error updating profile: {str(e)}")
    #         return jsonify({"error": "Failed to update user profile"}), 500

    # @jwt_required()
    # def get_user_posts(self):
    #     """Handle GET request for user's posts"""
    #     try:
    #         user_id = get_jwt_identity()
            
    #         # Get pagination params
    #         sort_by = request.args.get('sort_by', 'recent')
    #         limit = min(int(request.args.get('limit', 10)), 50)  # Cap at 50
    #         offset = int(request.args.get('offset', 0))
            
    #         current_app.logger.info(f"Fetching posts for user {user_id}")
            
    #         posts, error = self.profile_service.get_user_posts(
    #             user_id=user_id,
    #             sort_by=sort_by,
    #             limit=limit,
    #             offset=offset
    #         )
            
    #         if error:
    #             return jsonify({"error": error}), 400
                
    #         return jsonify({"posts": posts}), 200
            
    #     except ValueError as e:
    #         current_app.logger.warning(f"Invalid request parameters: {str(e)}")
    #         return jsonify({"error": "Invalid parameters"}), 400
    #     except Exception as e:
    #         current_app.logger.error(f"Error fetching user posts: {str(e)}")
    #         return jsonify({"error": "Failed to fetch posts"}), 500