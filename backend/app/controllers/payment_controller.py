from flask import request, jsonify, current_app
from app.interfaces.services.IPaymentService import IPaymentService
from app.services.payment_service import PaymentService
from flask_jwt_extended import jwt_required, get_jwt_identity
import stripe
import os

class PaymentController:
    def __init__(self, payment_service: IPaymentService = None):
        self.payment_service = payment_service or PaymentService()
        self.webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    @jwt_required()
    def create_checkout_session(self):
        """Create a checkout session for upgrading membership"""
        try:
            # Get user ID from JWT
            user_id = get_jwt_identity()
            
            # Create checkout session
            session_data, error = self.payment_service.create_checkout_session(user_id)
            
            if error:
                return jsonify({"error": error}), 400
                
            return jsonify(session_data), 200
            
        except Exception as e:
            current_app.logger.error(f"Error creating checkout session: {str(e)}")
            return jsonify({"error": "Failed to create checkout session"}), 500
    
    def webhook_handler(self):
        """Handle Stripe webhook events"""
        try:
            # Get webhook payload and signature
            payload = request.data
            sig_header = request.headers.get('Stripe-Signature')
            
            if not payload or not sig_header:
                return jsonify({"error": "Missing payload or signature"}), 400
            
            # Verify webhook signature
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, self.webhook_secret
                )
            except stripe.error.SignatureVerificationError as e:
                current_app.logger.warning(f"Invalid webhook signature: {str(e)}")
                return jsonify({"error": "Invalid signature"}), 400
            
            # Handle specific events
            event_type = event['type']
            
            if event_type == 'checkout.session.completed':
                # Payment was successful
                session = event['data']['object']
                
                # Update user membership
                user_id = session.get('metadata', {}).get('user_id')
                if user_id:
                    success, _, error = self.payment_service.verify_session(session.id)
                    if not success:
                        current_app.logger.error(f"Failed to process session: {error}")
                
            return jsonify({"received": True}), 200
            
        except Exception as e:
            current_app.logger.error(f"Error handling webhook: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    @jwt_required()
    def verify_session(self):
        """Verify a checkout session and update user membership"""
        try:
            # Get session ID from query parameters
            session_id = request.args.get('session_id')
            
            if not session_id:
                return jsonify({"error": "Session ID is required"}), 400
            
            # Verify session
            success, user_id, error = self.payment_service.verify_session(session_id)
            
            if not success:
                return jsonify({"error": error}), 400
                
            return jsonify({"success": True, "message": "Membership upgraded successfully"}), 200
            
        except Exception as e:
            current_app.logger.error(f"Error verifying session: {str(e)}")
            return jsonify({"error": "Failed to verify session"}), 500