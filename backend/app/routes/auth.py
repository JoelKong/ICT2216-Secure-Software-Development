# all this is gpt generated need reserach if secure
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.users import User
from app.db import db

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
    
    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already in use."}), 400

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken."}), 400
    
    # TODO: inside here need do server side protection, check email valid then need do server side rate limiting also (fe is set to 5 attempts then 10 sec cooldown)
    # check if username and email unique, password meets Minimum 8 characters
    #At least one uppercase letter
    #At least one lowercase letter
    #At least one number
    #At least one special character
    #check if confirm password is same, then generate hash, send OTP, once pass, add to db
    # create session for user with access refresh token all that, idk if we store token in local storage better or yall got more secure idea
    # and return me corresponding success/error message, along with user details and session

    # lmk if need create new frontend page for OTP

    password_hash = generate_password_hash(password)

    new_user = User(
        email=email,
        username=username,
        password=password_hash
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        # might need to add last login and posts made
        return jsonify({
        "message": "Sign up was successful! Logging in...",
        "access_token": "",
        "refresh_token": "",
        "user": {
            "user_id": new_user.user_id,
            "username": new_user.username,
            "profile_picture": new_user.profile_picture,
            "membership": new_user.membership,
            "created_at": new_user.created_at
            }
        }), 201
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
    
    #TODO: same thing with signup, need secure this

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    #return session also
    return jsonify({
        "message": "Login successful",
        "access_token": "",
        "refresh_token": "",
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "profile_picture": user.profile_picture,
            "membership": user.membership,
            "created_at": user.created_at
            }
    }), 200



# TODO: add route for refreshing token here from now onwards in every route in home onwards, we check access token whether expire if expire then call refresh route?