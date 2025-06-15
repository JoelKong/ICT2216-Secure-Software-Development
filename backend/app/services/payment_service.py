import os
import stripe
from app.repositories.user_repository import UserRepository
from flask import current_app

class PaymentService:
    def __init__(self):
        self.user_repository = UserRepository()
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    
    def create_checkout_session(self, user_id):
        """Create Stripe checkout session for membership upgrade"""
        try:
            # Get user details from repository
            user = self.user_repository.get_by_id(user_id)
            
            if not user:
                current_app.logger.warning(f"Checkout attempt for non-existent user: {user_id}")
                return None, "User not found"
                
            if user.membership == 'premium':
                current_app.logger.info(f"User {user_id} attempted upgrade but is already premium")
                return None, "User is already a premium member"
            
            # Create checkout session (from existing upgrade-membership route)
            frontend_route = os.getenv("FRONTEND_ROUTE")
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Premium Membership Upgrade',
                            'description': 'Upgrade to premium membership for unlimited posts',
                        },
                        'unit_amount': 200,  # $2.00 in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'{frontend_route}/success?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=f'{frontend_route}/failure?session_id={{CHECKOUT_SESSION_ID}}',
                metadata={'user_id': user_id}
            )
            
            current_app.logger.info(f"Created checkout session for user {user_id}: {session.id}")
            return session, None
            
        except stripe.error.StripeError as e:
            current_app.logger.error(f"Stripe error creating checkout session: {str(e)}")
            return None, f"Payment processing error: {str(e)}"
        except Exception as e:
            current_app.logger.error(f"Error creating checkout session: {str(e)}")
            raise
    
    def verify_session(self, session_id):
        """Verify Stripe session status"""
        try:
            # Get session from Stripe (from existing verify-session route)
            session = stripe.checkout.Session.retrieve(session_id)
            
            is_valid = session.payment_status == "paid"
            current_app.logger.info(f"Verified session {session_id}: valid={is_valid}")
            
            return {
                "valid": is_valid,
                "session_id": session_id,
                "customer_email": session.customer_details.email if hasattr(session, 'customer_details') else None
            }
            
        except stripe.error.StripeError as e:
            current_app.logger.error(f"Stripe error verifying session: {str(e)}")
            return {"valid": False, "error": str(e)}
        except Exception as e:
            current_app.logger.error(f"Error verifying session: {str(e)}")
            raise
    
    def process_webhook_event(self, payload, signature):
        """Process Stripe webhook event"""
        try:
            # Process webhook (from existing stripe/webhook route)
            endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
            
            event = stripe.Webhook.construct_event(
                payload, signature, endpoint_secret
            )
            
            # Handle checkout completion event
            if event['type'] == 'checkout.session.completed':
                session = event['data']['object']
                user_id = session['metadata']['user_id']
                
                # Upgrade user membership using UserRepository
                user = self.user_repository.get_by_id(user_id)
                if user:
                    user.membership = 'premium'
                    
                    try:
                        self.user_repository.db.session.commit()
                        current_app.logger.info(f"Successfully upgraded user {user_id} to premium via webhook")
                    except Exception as e:
                        self.user_repository.db.session.rollback()
                        current_app.logger.error(f"Database error updating user membership: {str(e)}")
                        return False, f"Database error: {str(e)}"
                else:
                    current_app.logger.warning(f"Failed to upgrade user {user_id} - user not found")
                
            return True, None
            
        except stripe.error.SignatureVerificationError as e:
            current_app.logger.error(f"Webhook signature verification failed: {str(e)}")
            return False, f"Signature verification failed: {str(e)}"
        except ValueError as e:
            current_app.logger.error(f"Invalid webhook payload: {str(e)}")
            return False, f"Invalid payload: {str(e)}"
        except Exception as e:
            current_app.logger.error(f"Webhook processing error: {str(e)}")
            raise