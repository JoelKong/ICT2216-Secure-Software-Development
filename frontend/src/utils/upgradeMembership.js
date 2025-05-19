import { loadStripe } from "@stripe/stripe-js";
import { STRIPE_CHECKOUT_ROUTE, API_ENDPOINT } from "../const";

export default async function upgradeMembership(token) {
  const stripe_publishable_key = import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY;
  const stripe = await loadStripe(stripe_publishable_key);

  // Create checkout session
  const response = await fetch(`${API_ENDPOINT}/${STRIPE_CHECKOUT_ROUTE}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    // credentials: "include"
  });

  const session = await response.json();
  console.log(session);

  // Redirect to Stripe Checkout
  const { error } = await stripe.redirectToCheckout({
    sessionId: session.id,
  });

  if (error) {
    console.error("Stripe Checkout error:", error);
    return error;
  }
}
