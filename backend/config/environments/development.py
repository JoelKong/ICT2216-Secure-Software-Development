import os
from config.settings import BaseConfig

class DevelopmentConfig(BaseConfig):
    """Development-specific configuration"""
    DEBUG = True
    TESTING = False
    JWT_COOKIE_SECURE = False
    LOG_LEVEL = 'DEBUG'
    # Development-specific overrides
    LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')