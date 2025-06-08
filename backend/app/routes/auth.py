from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.users import User
from datetime import datetime
from app.db import db
from app.utils.validation import is_valid_email, is_strong_password
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_refresh_cookies, unset_jwt_cookies

auth_bp = Blueprint('auth', __name__)

# Sign up route
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    if not all([email, username, password, confirm_password]):
        return jsonify({"error": "All fields are required."}), 400
    
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format."}), 400
    
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match."}), 400
    
    strong_enough, strength_message = is_strong_password(password)
    if not strong_enough:
        return jsonify({"error": strength_message}), 400
    
    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already in use."}), 400

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken."}), 400
    
    # TODOIS: send OTP, once pass, then can touch db

    password_hash = generate_password_hash(password)

    new_user = User(
        email=email,
        username=username,
        password=password_hash
    )

    try:
        db.session.add(new_user)
        db.session.commit()

        # Create access and refresh tokens
        user_identity = str(new_user.user_id)
        access_token = create_access_token(identity=user_identity)
        refresh_token = create_refresh_token(identity=user_identity)

        response = jsonify({
        "message": "Sign up was successful! Logging in...",
        "access_token": access_token,
        })
        set_refresh_cookies(response, refresh_token)
        return response, 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Something went wrong. Please try again."}), 500
    
# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    try:
        user_identity = str(user.user_id)
        access_token = create_access_token(identity=user_identity)
        refresh_token = create_refresh_token(identity=user_identity)
        response = jsonify({
            "message": "Login successful",
            "access_token": access_token,
        })
        set_refresh_cookies(response, refresh_token)
        return response, 200
    except Exception as e:
        return jsonify({"error": "Something went wrong. Please try again."}), 500


# Refresh token route
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_identity = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_identity)
    return jsonify(access_token=new_access_token), 200