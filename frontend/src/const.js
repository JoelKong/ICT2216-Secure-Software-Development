export const API_ENDPOINT = import.meta.env.VITE_API_ENDPOINT;

// Auth
export const SIGNUP_ROUTE = "api/signup";
export const LOGIN_ROUTE = "api/login";

// Posts
export const FETCH_POSTS_ROUTE = "api/posts";
export const DELETE_POSTS_ROUTE = "api/posts/delete";
export const LIKE_POST_ROUTE = "api/posts/like";

// Stripe
export const STRIPE_CHECKOUT_ROUTE = "api/upgrade-membership";
export const VITE_STRIPE_SESSION_VERIFICATION_ROUTE = "api/verify-session";
