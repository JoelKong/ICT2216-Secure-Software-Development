import os
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from flask import request, has_request_context

class RequestFormatter(logging.Formatter):
    """Custom formatter to include request-specific information"""
    
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.method = request.method
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.method = None
            record.remote_addr = None
            
        return super().format(record)

def configure_logging(app):
    """Configure logging for the Flask application"""
    # Create logs directory if it doesn't exist
    log_dir = app.config.get('LOG_DIR', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    log_format = app.config.get('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Clear existing handlers
    if app.logger.handlers:
        app.logger.handlers.clear()
    
    # Set up basic configuration
    app.logger.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Use different formatters based on context
    if app.debug:
        console_format = RequestFormatter(
            '[%(levelname)s] %(asctime)s - %(message)s'
        )
    else:
        console_format = logging.Formatter(log_format)
    
    console_handler.setFormatter(console_format)
    app.logger.addHandler(console_handler)
    
    # File handler - daily rotation
    file_handler = TimedRotatingFileHandler(
        os.path.join(log_dir, app.config.get('LOG_FILE', 'app.log')),
        when='midnight',
        interval=1,
        backupCount=30
    )
    file_handler.setLevel(log_level)
    
    # Use a simpler format for file logs
    file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    app.logger.addHandler(file_handler)
    
    # Set propagate to False to avoid duplicate logs
    app.logger.propagate = False
    
    # Log startup message
    app.logger.info(f"Application started in {app.config.get('ENV', 'unknown')} mode")