import { Navigate } from "react-router-dom";

export default function PrivateRoute({ isAuthenticated, children }) {
  return isAuthenticated ? children : <Navigate to="/" />;
}
