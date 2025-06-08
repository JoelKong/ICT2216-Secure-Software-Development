from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.users import User
from app.db import db

profile_bp = Blueprint('profile', __name__)

# TODOIS: SECURE THIS CHECK ACCESS TOKEN VALID
@profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def fetch_user():
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "membership": user.membership,
            "profile_picture": user.profile_picture,
            "created_at": user.created_at,
            "post_limit": user.post_limit
        }
    }), 200