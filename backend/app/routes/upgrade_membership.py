from flask import Blueprint
from app.controllers.payment_controller import PaymentController

upgrade_membership_bp = Blueprint('upgrade_membership', __name__)
payment_controller = PaymentController()

# Create Stripe checkout session
upgrade_membership_bp.route('/upgrade-membership', methods=['POST'])(payment_controller.create_checkout_session)

# Process Stripe webhook
upgrade_membership_bp.route('/stripe/webhook', methods=['POST'])(payment_controller.webhook_handler)

# Verify Stripe session
upgrade_membership_bp.route('/verify-session', methods=['GET'])(payment_controller.verify_session)