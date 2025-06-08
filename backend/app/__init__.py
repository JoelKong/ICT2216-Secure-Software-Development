from flask import Flask
from flask_cors import CORS
from .db import db
from .routes.auth import auth_bp
from .routes.posts import posts_bp
from .routes.profile import profile_bp
from .routes.upgrade_membership import upgrade_membership_bp
import os
from flask_jwt_extended import JWTManager
from datetime import timedelta

# Initialise app
def create_app():
    app = Flask(__name__)
    #TODOIS: dk if need secure this and need adjust origin for cloud
    CORS(app, resources={r"/api/*": {"origins": {os.getenv("FRONTEND_ROUTE")}}}, supports_credentials=True)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your-default-secret-key-for-dev")
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_COOKIE_SECURE"] = os.getenv("FLASK_ENV")
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 1))) 
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 1)))

    jwt = JWTManager(app)


    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(posts_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')
    app.register_blueprint(upgrade_membership_bp, url_prefix='/api')

    return app
