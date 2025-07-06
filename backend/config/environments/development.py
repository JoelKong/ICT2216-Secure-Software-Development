import os
from config.settings import BaseConfig

class DevelopmentConfig(BaseConfig):
    """Development-specific configuration"""
    DEBUG = True
    TESTING = False
    JWT_COOKIE_SECURE = False
    LOG_LEVEL = 'DEBUG'
    # Development-specific overrides
    LOG_DIR = os.getenv("LOG_PATH", os.path.join(os.getcwd(), "logs"))