import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

export default function PaymentSuccess() {
  const [valid, setValid] = useState(null);
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const sessionId = searchParams.get("session_id");

  // Verify session before showing content
  //   useEffect(() => {
  //     if (!sessionId) {
  //       navigate("/");
  //       return;
  //     }
  //     fetch(
  //       `${API_ENDPOINT}/${VITE_STRIPE_SESSION_VERIFICATION_ROUTE}?session_id=${sessionId}`
  //     )
  //       .then((res) => res.json())
  //       .then((data) => {
  //         if (data.valid) setValid(true);
  //         else navigate("/");
  //       })
  //       .catch(() => navigate("/"));
  //   }, [sessionId, navigate]);

  if (valid === null)
    return (
      <div className="w-screen h-screen flex justify-center items-center">
        <div className="w-full h-full flex justify-between items-center">
          Verifying payment
        </div>
      </div>
    );

  return (
    <div>
      <h2>Payment Successful!</h2>
      <button onClick={() => navigate("/")}>Go Home</button>
    </div>
  );
}
