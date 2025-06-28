import pytest
import sys
import os
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.services.profile_service import ProfileService

class TestProfileService:
    
    @pytest.fixture
    def mock_user_repository(self):
        return Mock()
    
    @pytest.fixture
    def mock_post_repository(self):
        return Mock()
    
    @pytest.fixture
    def profile_service(self, mock_user_repository, mock_post_repository):
        return ProfileService(
            user_repository=mock_user_repository,
            post_repository=mock_post_repository
        )
    
    def test_is_allowed_file_valid_extension(self, profile_service):
        """Test file validation with valid extensions"""
        assert profile_service._is_allowed_file('image.png') is True
        assert profile_service._is_allowed_file('image.jpg') is True
        assert profile_service._is_allowed_file('image.jpeg') is True
    
    def test_is_allowed_file_invalid_extension(self, profile_service):
        """Test file validation with invalid extensions"""
        assert profile_service._is_allowed_file('image.gif') is False
        assert profile_service._is_allowed_file('document.pdf') is False
        assert profile_service._is_allowed_file('noextension') is False
    
    def test_get_user_profile_success(self, profile_service, mock_user_repository):
        """Test successful user profile retrieval"""
        from app.models.users import User
        
        mock_user = User()
        mock_user.user_id = 1
        mock_user.username = 'testuser'
        mock_user.email = 'test@example.com'
        mock_user.membership = 'basic'
        mock_user_repository.get_by_id.return_value = mock_user
        
        result, error = profile_service.get_user_profile(user_id=1)
        
        assert error is None
        assert result['user_id'] == 1
        assert result['username'] == 'testuser'
        assert result['email'] == 'test@example.com'
        assert result['membership'] == 'basic'
    
    def test_get_user_profile_not_found(self, profile_service, mock_user_repository):
        """Test user profile retrieval when user not found"""
        mock_user_repository.get_by_id.return_value = None
        
        result, error = profile_service.get_user_profile(user_id=999)
        
        assert result is None
        assert error == "User not found"
    
    def test_update_profile_invalid_email(self, profile_service):
        """Test profile update with invalid email"""
        update_data = {
            'email': 'invalid-email'
        }
        
        with patch('app.utils.validation.is_valid_email', return_value=False):
            result, error = profile_service.update_profile(user_id=1, data=update_data)
            
            assert result is None
            assert error == "Invalid email format"
    
    @patch('os.makedirs')
    @patch('time.time')
    def test_update_profile_picture_success(self, mock_time, mock_makedirs, profile_service, mock_user_repository):
        """Test successful profile picture update"""
        mock_time.return_value = 1234567890
        
        mock_file = Mock()
        mock_file.filename = 'profile.jpg'
        mock_file.save = Mock()
        
        mock_user_repository.update_profile_picture.return_value = Mock()
        
        with patch.object(profile_service, '_is_allowed_file', return_value=True):
            result, error = profile_service.update_profile_picture(user_id=1, file=mock_file)
            
            assert error is None
            assert result.startswith('/uploads/')
            mock_makedirs.assert_called_once()
            mock_file.save.assert_called_once()
    
    def test_update_profile_picture_invalid_file(self, profile_service):
        """Test profile picture update with invalid file type"""
        mock_file = Mock()
        mock_file.filename = 'document.pdf'
        
        with patch.object(profile_service, '_is_allowed_file', return_value=False):
            result, error = profile_service.update_profile_picture(user_id=1, file=mock_file)
            
            assert result is None
            assert error == "File type not allowed"