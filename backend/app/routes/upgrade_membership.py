from flask import Blueprint
from app.controllers.payment_controller import PaymentController
from app.services.payment_service import PaymentService

upgrade_membership_bp = Blueprint('upgrade_membership', __name__)

# Create service instance
payment_service = PaymentService()

# Create controller with injected service
payment_controller = PaymentController(payment_service=payment_service)

# Create Stripe checkout session
upgrade_membership_bp.route('/upgrade-membership', methods=['POST'])(payment_controller.create_checkout_session)

# Process Stripe webhook
upgrade_membership_bp.route('/stripe/webhook', methods=['POST'])(payment_controller.webhook_handler)

# Verify Stripe session
upgrade_membership_bp.route('/verify-session', methods=['GET'])(payment_controller.verify_session)