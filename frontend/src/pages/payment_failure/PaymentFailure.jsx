import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import {
  API_ENDPOINT,
  VITE_STRIPE_SESSION_VERIFICATION_ROUTE,
} from "../../const";
import { GlobalContext } from "../../utils/globalContext";

export default function PaymentFailure() {
  const { auth } = useContext(GlobalContext);
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const sessionId = searchParams.get("session_id");

  // Verify session before showing content
  useEffect(() => {
    if (!sessionId) {
      navigate("/");
      return;
    }
    fetch(
      `${API_ENDPOINT}/${VITE_STRIPE_SESSION_VERIFICATION_ROUTE}?session_id=${sessionId}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth.token}`,
        },
        // credentials: "include",
      }
    )
      .then((res) => res.json())
      .then((data) => {
        if (data.valid) setValid(true);
        else navigate("/");
      })
      .catch(() => navigate("/"));
  }, [sessionId, navigate]);

  return (
    <div className="w-screen h-screen flex justify-center items-center">
      <div className="border-2 w-11/12 md:w-1/2 h-1/3 rounded-lg flex flex-col justify-evenly items-center bg-gray-300">
        <p className="text-xl font-bold">Payment Failed or Cancelled</p>
        <button
          className="border-2 rounded-md cursor-pointer bg-blue-300 hover:bg-blue-400 p-4 text-lg font-semibold"
          onClick={() => navigate("/")}
        >
          Back to Home
        </button>
      </div>
    </div>
  );
}
