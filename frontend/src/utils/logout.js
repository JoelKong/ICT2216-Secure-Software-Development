import { useNavigate } from "react-router-dom";

export default function logout() {
  const navigate = useNavigate();

  localStorage.removeItem("access_token");
  localStorage.removeItem("user");
  navigate("/");
}
