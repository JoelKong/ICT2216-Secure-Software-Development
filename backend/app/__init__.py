from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .db import db
from .extensions import limiter
from config import init_app_config

def create_app(env=None):
    app = Flask(__name__)
    
    # Initialize configuration from the config module
    configured_env = init_app_config(app, env)
    
    # Initialize extensions
    limiter.init_app(app)
    
    # Setup CORS
    CORS(app, 
         resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS')}}, 
         supports_credentials=True)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize database
    db.init_app(app)

    with app.app_context():
        # Import all models to register them with SQLAlchemy
        from app import models  # this loads models/__init__.py
    
    # Import blueprints here to avoid circular imports
    from .routes.auth import auth_bp
    from .routes.posts import posts_bp
    from .routes.profile import profile_bp
    from .routes.upgrade_membership import upgrade_membership_bp
    from .routes.comments import comments_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(posts_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')
    app.register_blueprint(upgrade_membership_bp, url_prefix='/api')
    app.register_blueprint(comments_bp, url_prefix="/api")
    
    # Log application creation
    app.logger.info(f"Application initialized with environment: {configured_env}")
    
    return app