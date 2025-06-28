import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add backend directory to path
backend_dir = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, backend_dir)

from app.services.auth_service import AuthService

class TestAuthService:
    
    @pytest.fixture
    def mock_user_repository(self):
        return Mock()
    
    @pytest.fixture
    def auth_service(self, mock_user_repository):
        return AuthService(user_repository=mock_user_repository)
    
    def test_validate_signup_data_success(self, auth_service, mock_user_repository):
        """Test successful signup data validation"""
        mock_user_repository.check_username_exists.return_value = False
        mock_user_repository.check_email_exists.return_value = False
        
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123!'
        }
        
        with patch('app.utils.validation.is_valid_email', return_value=True), \
             patch('app.utils.validation.is_strong_password', return_value=(True, "")):
            
            is_valid, message = auth_service.validate_signup_data(data)
            
            assert is_valid is True
            assert message == ""
    
    def test_validate_signup_data_missing_field(self, auth_service):
        """Test validation fails when required field is missing"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com'
            # password missing
        }
        
        is_valid, message = auth_service.validate_signup_data(data)
        
        assert is_valid is False
        assert "Missing required field: password" in message
    
    def test_validate_signup_data_username_too_short(self, auth_service):
        """Test validation fails when username is too short"""
        data = {
            'username': 'ab',
            'email': 'test@example.com',
            'password': 'Password123!'
        }
        
        is_valid, message = auth_service.validate_signup_data(data)
        
        assert is_valid is False
        assert "Username must be at least 3 characters" in message
    
    def test_validate_signup_data_username_exists(self, auth_service, mock_user_repository):
        """Test validation fails when username already exists"""
        mock_user_repository.check_username_exists.return_value = True
        
        data = {
            'username': 'existinguser',
            'email': 'test@example.com',
            'password': 'Password123!'
        }
        
        is_valid, message = auth_service.validate_signup_data(data)
        
        assert is_valid is False
        assert "Username already exists" in message
    
    def test_validate_signup_data_invalid_email(self, auth_service, mock_user_repository):
        """Test validation fails with invalid email format"""
        mock_user_repository.check_username_exists.return_value = False
        
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'Password123!'
        }
        
        with patch('app.utils.validation.is_valid_email', return_value=False):
            is_valid, message = auth_service.validate_signup_data(data)
            
            assert is_valid is False
            assert "Invalid email format" in message
    
    def test_validate_signup_data_email_exists(self, auth_service, mock_user_repository):
        """Test validation fails when email already exists"""
        mock_user_repository.check_username_exists.return_value = False
        mock_user_repository.check_email_exists.return_value = True
        
        data = {
            'username': 'testuser',
            'email': 'existing@example.com',
            'password': 'Password123!'
        }
        
        with patch('app.utils.validation.is_valid_email', return_value=True):
            is_valid, message = auth_service.validate_signup_data(data)
            
            assert is_valid is False
            assert "Email already exists" in message
