import { useEffect, useContext } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { API_ENDPOINT } from "../../const";
import { GlobalContext } from "../../utils/globalContext";

export default function EmailVerification({ setIsAuthChecked }) {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const salt = searchParams.get("salt"); 
  const { setAuth, setModal } = useContext(GlobalContext);
  const navigate = useNavigate();

  useEffect(() => {
    async function verify() {
      try {
        const response = await fetch(`${API_ENDPOINT}/api/verify_email?token=${token}&salt=${salt}`);
        const data = await response.json();

        if (response.ok) {
          localStorage.setItem("access_token", data.access_token);
          setAuth({
            isAuthenticated: true,
            token: data.access_token,
            user: null,
          });
          setIsAuthChecked(false);
          setModal({
            active: true,
            type: "pass",
            message: "Email verified successfully!",
          });
          navigate("/setup_totp");
        } else {
          setModal({
            active: true,
            type: "fail",
            message: data.error || "Verification failed.",
          });
        }
      } catch {
        setModal({
          active: true,
          type: "fail",
          message: "Server error verifying email.",
        });
      }
    }

    if (token) verify();
  }, [token]);

  return (
    <div className="text-white text-xl flex justify-center items-center h-screen">
      Verifying your email...
    </div>
  );
}
