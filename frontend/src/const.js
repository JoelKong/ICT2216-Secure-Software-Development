export const API_ENDPOINT = import.meta.env.VITE_API_ENDPOINT;

// Auth
export const SIGNUP_ROUTE = "api/signup";
export const LOGIN_ROUTE = "api/login";
export const REFRESH_ROUTE = "api/refresh";

// Posts
export const FETCH_POSTS_ROUTE = "api/posts";
export const CREATE_POST_ROUTE = "api/posts/create";
export const EDIT_POST_ROUTE = "api/posts/edit";
export const DELETE_POSTS_ROUTE = "api/posts/delete";
export const LIKE_POST_ROUTE = "api/posts/like";

// Profile/Global
export const FETCH_USER_ROUTE = "api/profile";

// Stripe
export const STRIPE_CHECKOUT_ROUTE = "api/upgrade-membership";
export const VITE_STRIPE_SESSION_VERIFICATION_ROUTE = "api/verify-session";
