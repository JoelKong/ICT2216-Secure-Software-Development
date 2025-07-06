import { Navigate, useLocation } from "react-router-dom";
import jwt_decode from "jwt-decode";

// Assumes you have a `getAuthToken()` from context
import { useContext } from "react";
import { GlobalContext } from "../../utils/globalContext";

export default function PrivateRoute({ isAuthenticated, children }) {
  const { getAuthToken } = useContext(GlobalContext);
  const location = useLocation();

  if (!isAuthenticated) return <Navigate to="/" replace />;

  try {
    const token = getAuthToken();
    const decoded = jwt_decode(token);

    // Allow setup_totp page even if not verified yet
    if (decoded.totp_verified || location.pathname === "/setup_totp") {
      return children;
    } else {
      return <Navigate to="/setup_totp" replace />;
    }
  } catch (e) {
    console.error("Invalid token:", e);
    return <Navigate to="/" replace />;
  }
}
