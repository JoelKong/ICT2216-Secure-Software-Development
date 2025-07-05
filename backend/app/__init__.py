from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .db import db
from .extensions import limiter
from config import init_app_config
from flask_mail import Mail
import os

mail = Mail()

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

    app.config['MAIL_SECRET_KEY'] = os.getenv('MAIL_SECRET_KEY')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    app.config['FRONTEND_ROUTE'] = os.getenv('FRONTEND_ROUTE', 'http://localhost:5173')

    # Initialize Mail
    mail.init_app(app)

    with app.app_context():
        # Import all models to register them with SQLAlchemy
        from app import models
    
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
    
    # Apply HSTS headers for enhanced security
    @app.after_request
    def apply_security_headers(response):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        return response
    
    return app