from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.users import User
from app.db import db
import os
import stripe

upgrade_membership_bp = Blueprint('upgrade_membership', __name__)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@upgrade_membership_bp.route('/upgrade-membership', methods=['POST'])
@jwt_required()
def upgrade_membership():
    frontend_route = os.getenv("FRONTEND_ROUTE")
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if user.membership == 'premium':
        return jsonify({"message": "User is already a premium member."}), 400

    try:
        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Premium Membership Upgrade',
                    },
                    'unit_amount': 200,  # $2.00 in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{frontend_route}/success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{frontend_route}/cancel',
            metadata={'user_id': user_id}
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# TODO:need to secure this idk how this works the on top linked to this webhook 
# need cloud then can register the endpoint under the webhook, for now need use stripe cli if want to connect db
@upgrade_membership_bp.route('/stripe/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print(f"Webhook ValueError: {e}")
        return jsonify({'error': str(e)}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f"Webhook SignatureVerificationError: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Webhook general error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['user_id']
        user = User.query.get(user_id)
        if user:
            user.membership = 'premium'
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Database error updating user {user_id} to premium: {e}")
                return jsonify({'error': 'Database error during upgrade'}), 500
            
    return jsonify({'status': 'success'})

# Verify stripe session for the success and failure pages
@upgrade_membership_bp.route('/verify-session', methods=['GET'])
def verify_session():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({'valid': False, 'message': 'Session ID is required'}), 400
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == "paid":
            return jsonify({'valid': True})
        else:
            return jsonify({'valid': False})
    except stripe.error.StripeError as e:
        print(f"Error verifying Stripe session: {e}")
        return jsonify({'valid': False, 'message': str(e)}), 400
    except Exception as e:
        print(f"Unexpected error verifying Stripe session: {e}")
        return jsonify({'valid': False, 'message': 'An unexpected error occurred'}), 500