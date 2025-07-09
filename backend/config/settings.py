import os
from datetime import timedelta

class BaseConfig:
    """Base configuration with settings common to all environments"""
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-for-dev")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-jwt-secret-for-dev")
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_SECURE = True #For development change this to false no https on development
    JWT_COOKIE_HTTPONLY = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 1)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 1)))
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS settings
    CORS_ORIGINS = [os.getenv("FRONTEND_ROUTE", "http://localhost:3000")]
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_DIR = '/var/log/app'  # Docker container path for logs
    LOG_FILE = 'app.log'

def get_config(env):
    """Return the appropriate configuration object based on environment"""
    if env == 'production':
        from .environments.production import ProductionConfig
        return ProductionConfig
    # Default to development
    from .environments.development import DevelopmentConfig
    return DevelopmentConfig