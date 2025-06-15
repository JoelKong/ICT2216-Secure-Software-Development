from config.settings import BaseConfig

class ProductionConfig(BaseConfig):
    """Production-specific configuration"""
    DEBUG = False
    TESTING = False
    JWT_COOKIE_SECURE = True
    # Additional production hardening
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True