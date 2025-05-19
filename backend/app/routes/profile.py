from flask import Blueprint, request, jsonify
from app.models.users import User
from app.db import db

profile_bp = Blueprint('profile', __name__)

# TODO: SECURE THIS CHECK ACCESS TOKEN VALID
@profile_bp.route('/profile', methods=['GET'])
def fetch_user():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    # token = auth_header.split(" ")[1]
    # payload = decode_token(token)
    # if not payload:
    #     return jsonify({"error": "Invalid or expired token"}), 401

    # user_id = payload.get("user_id")
    user_id = 1 # for testing
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Return user data 
    return jsonify({
        "user": {
            "username": user.username,
            "email": user.email,
            "membership": user.membership,
            "profile_picture": user.profile_picture,
            "created_at": user.created_at,
            "post_limit": user.post_limit
        }
    }), 200