import { API_ENDPOINT, REFRESH_ROUTE } from "../const";

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((promise) => {
    if (error) {
      promise.reject(error);
    } else {
      promise.resolve(token);
    }
  });
  failedQueue = [];
};

/**
 * A wrapper around fetch that handles JWT token refresh.
 * @param {string} url - The URL to fetch.
 * @param {object} options - Fetch options.
 * @param {function} getAuthToken - Function to get the current access token.
 * @param {function} updateAuthToken - Function to update the access token in context/localStorage.
 * @param {function} logout - Function to handle user logout.
 * @returns {Promise<Response>} - The fetch Response object.
 */
export default async function fetchWithAuth(
  url,
  options = {},
  getAuthToken,
  updateAuthToken,
  logout
) {
  const makeRequest = async (token) => {
    const requestOptions = {
      ...options,
      headers: {
        "Content-Type": "application/json", // Default, can be overridden by options.headers
        ...options.headers,
      },
    };
    if (token) {
      requestOptions.headers["Authorization"] = `Bearer ${token}`;
    }

    let response = await fetch(url, requestOptions);

    if (response.status === 401) {
      if (!isRefreshing) {
        isRefreshing = true;
        try {
          const refreshResponse = await fetch(
            `${API_ENDPOINT}/${REFRESH_ROUTE}`,
            {
              method: "POST",
              // Cookies (including the HttpOnly refresh token) are sent automatically by the browser
              // if the backend is configured correctly with CORS (supports_credentials=True).
            }
          );

          if (refreshResponse.ok) {
            const { access_token: newAccessToken } =
              await refreshResponse.json();
            updateAuthToken(newAccessToken);
            isRefreshing = false;
            processQueue(null, newAccessToken);
            // Retry the original request with the new token
            requestOptions.headers[
              "Authorization"
            ] = `Bearer ${newAccessToken}`;
            return fetch(url, requestOptions);
          } else {
            // Refresh failed
            isRefreshing = false;
            const error = new Error("Session expired. Please login again.");
            processQueue(error, null);
            if (logout) logout();
            throw error;
          }
        } catch (error) {
          console.error("Token refresh error:", error);
          isRefreshing = false;
          processQueue(error, null);
          if (logout) logout(); // Ensure logout on any refresh error
          throw error; // Re-throw to be caught by the calling function
        }
      } else {
        // If refresh is already in progress, queue the original request
        return new Promise((resolve, reject) => {
          failedQueue.push({
            resolve: (newToken) => {
              // This will be called by processQueue
              requestOptions.headers["Authorization"] = `Bearer ${newToken}`;
              resolve(fetch(url, requestOptions));
            },
            reject,
          });
        });
      }
    }
    return response;
  };

  const currentToken = getAuthToken();
  return makeRequest(currentToken);
}
