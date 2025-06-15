import os
from .logging_config import configure_logging

def init_app_config(app, provided_env=None):
    """Initialize application configuration"""
    # Use provided environment if available, fallback to environment variable
    env = provided_env or os.getenv('FLASK_ENV', 'development')
    
    # Import here to avoid circular imports
    from .settings import get_config
    
    # Load appropriate config
    config = get_config(env)
    app.config.from_object(config)
    
    # Configure logging
    configure_logging(app)
    
    # Return environment name for reference
    return env