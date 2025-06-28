import pytest
import sys
import os
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.services.post_service import PostService

class TestPostService:
    
    @pytest.fixture
    def mock_post_repository(self):
        return Mock()
    
    @pytest.fixture
    def mock_like_repository(self):
        return Mock()
    
    @pytest.fixture
    def post_service(self, mock_post_repository, mock_like_repository):
        return PostService(
            post_repository=mock_post_repository,
            like_repository=mock_like_repository
        )
    
    def test_is_allowed_file_valid_extension(self, post_service):
        """Test file validation with valid extensions"""
        assert post_service._is_allowed_file('image.png') is True
        assert post_service._is_allowed_file('image.jpg') is True
        assert post_service._is_allowed_file('image.jpeg') is True
        assert post_service._is_allowed_file('image.gif') is True
        assert post_service._is_allowed_file('image.webp') is True
    
    def test_is_allowed_file_invalid_extension(self, post_service):
        """Test file validation with invalid extensions"""
        assert post_service._is_allowed_file('document.pdf') is False
        assert post_service._is_allowed_file('script.js') is False
        assert post_service._is_allowed_file('image.txt') is False
        assert post_service._is_allowed_file('noextension') is False
    
    def test_get_posts_success(self, post_service, mock_post_repository):
        """Test successful post retrieval"""
        from app.models.posts import Post
        from app.models.users import User
        
        # Mock user and post data
        mock_user = User()
        mock_user.username = 'testuser'
        mock_user.profile_picture = None
        
        mock_post = Post()
        mock_post.post_id = 1
        mock_post.title = 'Test Post'
        mock_post.content = 'Test Content'
        mock_post.created_at = Mock()
        mock_post.created_at.isoformat.return_value = '2023-01-01T00:00:00'
        mock_post.updated_at = None
        mock_post.user_id = 1
        mock_post.user = mock_user
        mock_post.likes_count = 5
        
        mock_post_repository.get_posts.return_value = [mock_post]
        
        result = post_service.get_posts()
        
        assert 'posts' in result
        assert len(result['posts']) == 1
        
        post_data = result['posts'][0]
        assert post_data['post_id'] == 1
        assert post_data['title'] == 'Test Post'
        assert post_data['content'] == 'Test Content'
        assert post_data['username'] == 'testuser'
        assert post_data['likes'] == 5
    
    def test_get_posts_with_search(self, post_service, mock_post_repository):
        """Test post retrieval with search parameter"""
        mock_post_repository.get_posts.return_value = []
        
        post_service.get_posts(search='test query')
        
        mock_post_repository.get_posts.assert_called_once_with(
            sort_by='recent',
            limit=10,
            offset=0,
            search='test query',
            user_id=None
        )
    
    @patch('os.makedirs')
    @patch('time.time')
    def test_create_post_with_image(self, mock_time, mock_makedirs, post_service, mock_post_repository):
        """Test post creation with image upload"""
        mock_time.return_value = 1234567890
        
        # Mock image file
        mock_image = Mock()
        mock_image.filename = 'test.jpg'
        mock_image.save = Mock()
        
        mock_post_repository.create_post.return_value = {'post_id': 1}
        
        with patch.object(post_service, '_is_allowed_file', return_value=True):
            result = post_service.create_post(
                title='Test Post',
                content='Test Content',
                image_file=mock_image,
                user_id=1
            )
        
        mock_makedirs.assert_called_once_with(post_service.UPLOAD_FOLDER, exist_ok=True)
        mock_image.save.assert_called_once()
        mock_post_repository.create_post.assert_called_once()
        assert result == {'post_id': 1}
    
    def test_create_post_invalid_file_type(self, post_service):
        """Test post creation with invalid file type"""
        mock_image = Mock()
        mock_image.filename = 'test.txt'
        
        with patch.object(post_service, '_is_allowed_file', return_value=False):
            with pytest.raises(ValueError, match="File type not allowed"):
                post_service.create_post(
                    title='Test Post',
                    content='Test Content',
                    image_file=mock_image,
                    user_id=1
                )
    
    def test_create_post_without_image(self, post_service, mock_post_repository):
        """Test post creation without image"""
        mock_post_repository.create_post.return_value = {'post_id': 1}
        
        result = post_service.create_post(
            title='Test Post',
            content='Test Content',
            image_file=None,
            user_id=1
        )
        
        mock_post_repository.create_post.assert_called_once_with(
            'Test Post', 'Test Content', None, 1
        )
        assert result == {'post_id': 1}
    
    def test_get_user_liked_posts(self, post_service, mock_like_repository):
        """Test getting user's liked posts"""
        mock_like_repository.get_user_liked_post_ids.return_value = [1, 3, 5]
        
        result = post_service.get_user_liked_posts(user_id=1)
        
        assert result == [1, 3, 5]
        mock_like_repository.get_user_liked_post_ids.assert_called_once_with(1, None)
    
    def test_get_user_liked_posts_with_filter(self, post_service, mock_like_repository):
        """Test getting user's liked posts with post ID filter"""
        mock_like_repository.get_user_liked_post_ids.return_value = [1, 3]
        
        result = post_service.get_user_liked_posts(user_id=1, post_ids=[1, 2, 3])
        
        assert result == [1, 3]
        mock_like_repository.get_user_liked_post_ids.assert_called_once_with(1, [1, 2, 3])