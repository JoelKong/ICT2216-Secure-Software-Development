from app.interfaces.services.IPaymentService import IPaymentService
from app.interfaces.repositories.IUserRepository import IUserRepository
from app.repositories.user_repository import UserRepository
from flask import current_app, request
import stripe
import os
from typing import Dict, Tuple, Optional, Any

class PaymentService(IPaymentService):
    def __init__(self, user_repository: IUserRepository = None):
        self.user_repository = user_repository or UserRepository()
        stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
        self.price_id = os.environ.get('STRIPE_PRICE_ID')
        self.domain_url = os.environ.get('FRONTEND_ROUTE')
    
    def create_checkout_session(self, user_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Create a new checkout session"""
        try:
            # Check if user exists
            user = self.user_repository.get_by_id(user_id)
            if not user:
                current_app.logger.warning(f"Checkout session request for non-existent user {user_id}")
                return None, "User not found"
                
            # Check if user is already premium
            if user.membership == 'premium':
                current_app.logger.warning(f"User {user_id} already has premium membership")
                return None, "User already has premium membership"
                
            # Create checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Premium Membership',
                            },
                            'unit_amount': 200, 
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    'user_id': int(user_id)
                },
                mode='payment',
                success_url=f'{self.domain_url}/success?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=f'{self.domain_url}/failure',
            )
            
            current_app.logger.info(f"Created checkout session for user {user_id}: {checkout_session.id}")
            return {'id': checkout_session.id}, None
            
        except stripe.error.StripeError as e:
            current_app.logger.error(f"Stripe error: {str(e)}")
            return None, f"Stripe error: {str(e)}"
            
        except Exception as e:
            current_app.logger.error(f"Error creating checkout session: {str(e)}")
            return None, f"Internal server error: {str(e)}"
    
    def verify_session(self, session_id: str) -> Tuple[bool, Optional[int], Optional[str]]:
        """Verify a completed session and update user membership"""
        try:
            # Retrieve session
            session = stripe.checkout.Session.retrieve(session_id)
            
            # Check payment status
            if session.payment_status != 'paid':
                return False, None, "Payment not completed"
            
            # Get user ID from session metadata
            user_id = session.metadata.get('user_id')
            if not user_id:
                return False, None, "Invalid session: user ID not found"
            
            user_id = int(user_id)
            
            # Update user membership
            user = self.user_repository.update_membership(user_id, 'premium')
            if not user:
                current_app.logger.error(f"Failed to update membership for user {user_id}")
                return False, user_id, "Failed to update user membership"
            
            current_app.logger.info(f"User {user_id} membership upgraded to premium")
            return True, user_id, None
            
        except stripe.error.StripeError as e:
            current_app.logger.error(f"Stripe error during verification: {str(e)}")
            return False, None, f"Stripe error: {str(e)}"
            
        except Exception as e:
            current_app.logger.error(f"Error verifying session: {str(e)}")
            return False, None, f"Internal server error: {str(e)}"