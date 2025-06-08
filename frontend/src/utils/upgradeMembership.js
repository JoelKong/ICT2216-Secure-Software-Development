import { loadStripe } from "@stripe/stripe-js";
import { STRIPE_CHECKOUT_ROUTE, API_ENDPOINT } from "../const";
import fetchWithAuth from "./fetchWithAuth";

// Update function signature to accept context functions
export default async function upgradeMembership(
  getAuthToken,
  updateAuthToken,
  logoutUser
) {
  const stripe_publishable_key = import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY;
  if (!stripe_publishable_key) {
    console.error("Stripe publishable key not found.");
    return { error: { message: "Stripe configuration error." } };
  }
  const stripe = await loadStripe(stripe_publishable_key);

  try {
    // Create checkout session using fetchWithAuth
    const response = await fetchWithAuth(
      `${API_ENDPOINT}/${STRIPE_CHECKOUT_ROUTE}`,
      {
        method: "POST",
      },
      getAuthToken,
      updateAuthToken,
      logoutUser
    );

    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ error: "Failed to create Stripe session" }));
      console.error("Failed to create Stripe session:", errorData);
      return {
        error: {
          message: errorData.error || `HTTP error! status: ${response.status}`,
        },
      };
    }

    const session = await response.json();

    if (!session.id) {
      console.error("Stripe session ID not found in response:", session);
      return { error: { message: "Failed to retrieve Stripe session ID." } };
    }

    // Redirect to Stripe Checkout
    const { error: stripeRedirectError } = await stripe.redirectToCheckout({
      sessionId: session.id,
    });

    if (stripeRedirectError) {
      console.error("Stripe Checkout redirect error:", stripeRedirectError);
      return { error: stripeRedirectError };
    }
  } catch (error) {
    console.error("Error during upgrade membership process:", error);
    return {
      error: { message: error.message || "An unexpected error occurred." },
    };
  }
}
