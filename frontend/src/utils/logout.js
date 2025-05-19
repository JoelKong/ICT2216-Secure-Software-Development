export default function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user");
  navigate("/");
}
