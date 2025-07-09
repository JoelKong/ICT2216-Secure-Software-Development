import pytest
import sys
import os
from unittest.mock import Mock, patch
import secrets

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

@pytest.fixture(autouse=True)
def mock_environment():
    """Mock environment variables for all tests"""
    os.environ.update({
        'FLASK_ENV': 'testing',
        'SECRET_KEY': secrets.token_hex(16),
        'JWT_SECRET_KEY': secrets.token_hex(16),
        'DATABASE_URL': 'sqlite:///:memory:',
    })

@pytest.fixture
def mock_flask_app():
    """Mock Flask app for testing"""
    from flask import Flask
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'JWT_SECRET_KEY': secrets.token_hex(16),
        'SECRET_KEY': secrets.token_hex(16)
    })
    return app

@pytest.fixture(autouse=True)
def app_context(mock_flask_app):
    """Provide Flask application context for all tests"""
    with mock_flask_app.app_context():
        yield

# Mock external dependencies to avoid import errors
@pytest.fixture(autouse=True)
def mock_external_deps(monkeypatch):
    """Mock external dependencies"""
    # Mock Flask-JWT-Extended functions
    monkeypatch.setattr('flask_jwt_extended.create_access_token', Mock(return_value='mock_access_token'))
    monkeypatch.setattr('flask_jwt_extended.create_refresh_token', Mock(return_value='mock_refresh_token'))
    
    # Mock Flask current_app logger
    mock_logger = Mock()
    mock_current_app = Mock()
    mock_current_app.logger = mock_logger
    monkeypatch.setattr('flask.current_app', mock_current_app)
    
    # Mock Stripe
    monkeypatch.setattr('stripe.checkout.Session.create', Mock())
    monkeypatch.setattr('stripe.checkout.Session.retrieve', Mock())
    
    # Mock file operations
    monkeypatch.setattr('os.makedirs', Mock())
    monkeypatch.setattr('time.time', Mock(return_value=1234567890))
    
    # Mock Flask send_from_directory
    monkeypatch.setattr('flask.send_from_directory', Mock())