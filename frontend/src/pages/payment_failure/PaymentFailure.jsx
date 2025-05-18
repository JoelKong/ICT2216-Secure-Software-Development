import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

export default function PaymentFailure() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const sessionId = searchParams.get("session_id");

  useEffect(() => {
    if (!sessionId) {
      navigate("/");
      return;
    }
    // Optionally verify session or just show failure
  }, [sessionId, navigate]);

  return (
    <div>
      <h2>Payment Failed or Cancelled</h2>
      <button onClick={() => navigate("/")}>Go Home</button>
    </div>
  );
}
