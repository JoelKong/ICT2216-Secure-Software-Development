// Central route definitions for the frontend API calls
// Do not expose any of the sensitive logic or secrets inside this file
//Ensure that the backend routes are also protected by auth, rate limiting, input validation, etc.
export const API_ENDPOINT = import.meta.env.PROD
  ? ""
  : import.meta.env.VITE_API_ENDPOINT;

// Auth
// Sensitive actions - ensure server-side validation, rate limiting, etc.
export const SIGNUP_ROUTE = "api/signup";
export const LOGIN_ROUTE = "api/login";
export const REFRESH_ROUTE = "api/refresh";

// Posts
export const FETCH_POSTS_ROUTE = "api/posts";
export const CREATE_POST_ROUTE = "api/posts/create";
export const EDIT_POST_ROUTE = "api/posts/edit";
export const DELETE_POSTS_ROUTE = "api/posts/delete";
export const LIKE_POST_ROUTE = "api/posts/like";
export const FETCH_POST_SUMMARY_ROUTE = "api/posts/summary";
export const FETCH_USER_POST_LIMIT = "api/posts/limit";

// Comments
export const FETCH_COMMENTS_ROUTE = `api/comments`;
export const CREATE_COMMENT_ROUTE = `api/comments/create`;

// Profile/Global
export const FETCH_USER_ROUTE = "api/profile";

// Stripe
// Payment-related endpoints - ensure server checks authentication and session validity
export const STRIPE_CHECKOUT_ROUTE = "api/upgrade-membership";
export const VITE_STRIPE_SESSION_VERIFICATION_ROUTE = "api/verify-session";

//OTP
export const VERIFY_OTP = "api/verify_totp";
export const GET_TOTP = "api/get_user_totp_secret";
