from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.payment_service import PaymentService

class PaymentController:
    def __init__(self):
        self.payment_service = PaymentService()
    
    @jwt_required()
    def create_checkout_session(self):
        """Create Stripe checkout session for membership upgrade"""
        try:
            user_id = get_jwt_identity()
            current_app.logger.info(f"Creating checkout session for user: {user_id}")
            
            session, error = self.payment_service.create_checkout_session(user_id)
            
            if error:
                return jsonify({"error": error}), 400
                
            return jsonify({'id': session.id}), 200
            
        except Exception as e:
            current_app.logger.error(f"Error creating checkout session: {str(e)}")
            return jsonify({'error': "Failed to create checkout session"}), 500
    
    @jwt_required(optional=True)
    def verify_session(self):
        """Verify Stripe session status"""
        try:
            session_id = request.args.get('session_id')
            if not session_id:
                return jsonify({'valid': False, 'message': 'Session ID is required'}), 400
                
            current_app.logger.info(f"Verifying session: {session_id}")
            
            result = self.payment_service.verify_session(session_id)
            
            if result.get("error"):
                return jsonify({'valid': False, 'message': result["error"]}), 400
                
            return jsonify(result), 200
            
        except Exception as e:
            current_app.logger.error(f"Error verifying session: {str(e)}")
            return jsonify({'valid': False, 'message': 'An unexpected error occurred'}), 500
    
    def webhook_handler(self):
        """Handle Stripe webhook events"""
        try:
            payload = request.data
            sig_header = request.headers.get('Stripe-Signature')
            
            if not sig_header:
                current_app.logger.warning("Webhook called without Stripe signature")
                return jsonify({'error': 'No Stripe signature provided'}), 400
                
            current_app.logger.info("Processing webhook event")
            
            success, error = self.payment_service.process_webhook_event(payload, sig_header)
            
            if not success:
                return jsonify({'error': error}), 400
                
            return jsonify({'status': 'success'}), 200
            
        except Exception as e:
            current_app.logger.error(f"Webhook handler error: {str(e)}")
            return jsonify({'error': 'An unexpected error occurred'}), 500