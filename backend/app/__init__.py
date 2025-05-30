from flask import Flask
from flask_cors import CORS
from .db import db
from .routes.auth import auth_bp
from .routes.posts import posts_bp
from .routes.profile import profile_bp
from .routes.upgrade_membership import upgrade_membership_bp
import os

# Initialise app
def create_app():
    app = Flask(__name__)
    #TODOIS: dk if need secure this and need adjust origin for cloud
    CORS(app, resources={r"/api/*": {"origins": {os.getenv("FRONTEND_ROUTE")}}})
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', 'defaultsecretkey') #TODO: gpt say this is for session? idk
    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(posts_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')
    app.register_blueprint(upgrade_membership_bp, url_prefix='/api')

    return app
