import { useEffect, useState } from "react";
import { QRCodeCanvas } from "qrcode.react";
import { useNavigate } from "react-router-dom";
import { API_ENDPOINT, GET_TOTP, VERIFY_OTP } from "../../const";

function SetupTotp() {
  const [totpUrl, setTotpUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showQr, setShowQr] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchOtpUrl = async () => {
      try {
        const response = await fetch(`${API_ENDPOINT}/${GET_TOTP}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch OTP setup URL");
        }

        const data = await response.json();
        setTotpUrl(data.otpUrl);
        setShowQr(data.showQr);  
        setLoading(false);
      } catch (error) {
        console.error("Fetch OTP setup error:", error);
        setError("Failed to load OTP setup. Please try again.");
        setLoading(false);
      }
    };

    fetchOtpUrl();
  }, []);

  const handleSubmit = async () => {
    const code = document.querySelector(".input-field").value;

    if (!code) {
      alert("Please enter the OTP code.");
      return;
    }

    try {
      const response = await fetch(`${API_ENDPOINT}/${VERIFY_OTP}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify({ code }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("access_token", data.access_token);
        alert("TOTP Verified!");
        navigate("/posts");
      } else {
        alert(data.error || "Invalid OTP code. Please try again.");
      }
    } catch (error) {
      console.error("Fetch TOTP error:", error);
      alert("Error verifying OTP. Please try again.");
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="flex items-center justify-center h-screen p-4">
      <div className="w-full max-w-sm text-center space-y-6">
        {showQr && totpUrl && (
          <>
            <p className="font-bold text-xl">Scan this QR in your authenticator:</p>
            <QRCodeCanvas value={totpUrl} size={200} className="mx-auto" />
          </>
        )}

        <p className="font-bold text-lg">
          {showQr
            ? "Then enter the 6-digit code below:"
            : "Enter the 6-digit code from your authenticator app:"}
        </p>

        <input
          type="text"
          placeholder="123456"
          className="input-field w-full p-2 border bg-white rounded-md text-center mx-auto"
        />

        <button
          onClick={handleSubmit}
          className="w-full bg-green-500 text-white py-2 rounded-md hover:bg-blue-600 transition"
        >
          Verify Code
        </button>
      </div>
    </div>
  );
}
export default SetupTotp;
