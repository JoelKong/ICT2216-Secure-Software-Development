import pytest
import sys
import os
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.services.payment_service import PaymentService

class TestPaymentService:
    
    @pytest.fixture
    def mock_user_repository(self):
        return Mock()
    
    @pytest.fixture
    def payment_service(self, mock_user_repository):
        return PaymentService(user_repository=mock_user_repository)
    
    @patch('stripe.checkout.Session.retrieve')
    def test_verify_session_payment_not_completed(self, mock_stripe_retrieve, payment_service):
        """Test session verification with incomplete payment"""
        mock_session = Mock()
        mock_session.payment_status = 'unpaid'
        mock_stripe_retrieve.return_value = mock_session
        
        success, user_id, error = payment_service.verify_session(session_id='sess_test123')
        
        assert success is False
        assert user_id is None
        assert error == "Payment not completed"
    
    @patch('stripe.checkout.Session.retrieve')
    def test_verify_session_missing_metadata(self, mock_stripe_retrieve, payment_service):
        """Test session verification with missing user metadata"""
        mock_session = Mock()
        mock_session.payment_status = 'paid'
        mock_session.metadata = {}
        mock_stripe_retrieve.return_value = mock_session
        
        success, user_id, error = payment_service.verify_session(session_id='sess_test123')
        
        assert success is False
        assert user_id is None
        assert error == "Invalid session: user ID not found"
    
    @patch('stripe.checkout.Session.retrieve')
    def test_verify_session_stripe_error(self, mock_stripe_retrieve, payment_service):
        """Test session verification with Stripe error"""
        mock_stripe_retrieve.side_effect = Exception("Stripe API error")
        
        success, user_id, error = payment_service.verify_session(session_id='sess_test123')
        
        assert success is False
        assert user_id is None
        assert "Internal server error" in error
    
    @patch('stripe.checkout.Session.retrieve')
    def test_verify_session_user_update_failure(self, mock_stripe_retrieve, payment_service, mock_user_repository):
        """Test session verification with user update failure"""
        # Mock Stripe session
        mock_session = Mock()
        mock_session.payment_status = 'paid'
        mock_session.metadata = {'user_id': '1'}
        mock_stripe_retrieve.return_value = mock_session
        
        # Mock user repository update failure
        mock_user_repository.update_membership.return_value = None
        
        success, user_id, error = payment_service.verify_session(session_id='sess_test123')
        
        assert success is False
        assert user_id == 1
        assert error == "Failed to update user membership"