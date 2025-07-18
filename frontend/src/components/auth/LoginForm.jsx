import { useContext, useState } from "react";
import LoadingSpinner from "../global/LoadingSpinner";
import { API_ENDPOINT, LOGIN_ROUTE } from "../../const";
import checkRateLimit from "../../utils/checkRateLimit";
import { useNavigate } from "react-router-dom";
import { GlobalContext } from "../../utils/globalContext";

export default function LoginForm({ setIsSignup, setIsAuthChecked }) {
  const { setModal, rateLimit, setRateLimit, setAuth } =
    useContext(GlobalContext);
  const [loginFormData, setLoginFormData] = useState({
    email: "",
    password: "",
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setLoginFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Login function to send login details to Flask backend
  async function handleLogin(e) {
    e.preventDefault();
    setLoading(true);
    try {
      let error = "";

      // Check if rate limit reached
      if (checkRateLimit(rateLimit, setRateLimit, setModal)) {
        setLoading(false);
        return;
      }

      // Input Validation
      if (!loginFormData.email || !loginFormData.password) {
        error = "All fields are required";
      }

      if (error) {
        setModal({
          active: true,
          type: "fail",
          message: error,
        });
        setLoading(false);
        return;
      }

      console.log("API_ENDPOINT:", API_ENDPOINT);
      console.log("LOGIN_ROUTE:", LOGIN_ROUTE);
      console.log("Full URL:", `${API_ENDPOINT}/${LOGIN_ROUTE}`);


      const response = await fetch(`${API_ENDPOINT}/${LOGIN_ROUTE}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(loginFormData),
      });

      // Handle 429 Too Many Requests specifically
      if (response.status === 429) {
        // Force client-side rate limiter to cooldown mode
        setRateLimit({
          attempts: 5,
          cooldown: true,
        });

        setModal({
          active: true,
          type: "fail",
          message:
            "Too many login attempts. Please wait a few minutes before trying again.",
        });

        setLoading(false);
        return;
      }

      const data = await response.json();

      if (response.ok) {
        setModal({
          active: true,
          type: "pass",
          message: data.message,
        });
        setRateLimit({ attempts: 0, cooldown: false });
        localStorage.setItem("access_token", data.access_token);
        setIsAuthChecked(false);
        setAuth({
          isAuthenticated: true,
          token: data.access_token,
          user: null,
        });
        if (data.totp_verified) {
        navigate("/verify_totp");
      } else {
        navigate("/setup_totp");
      }
      } else {
        setModal({
          active: true,
          type: "fail",
          message: data.error,
        });
      }
    } catch (error) {
      setModal({
        active: true,
        type: "fail",
        message: "Something went wrong. Please try again.",
      });
      console.error("Error during login:", error);
    } finally {
      setLoading(false);
      setLoginFormData({
        email: "",
        password: "",
      });
    }
  }

  return (
    <section className="flex flex-col items-center w-11/12 md:w-7/12 pb-10 mt-4 border-2 rounded-lg bg-white">
      <div className="font-semibold text-2xl text-center w-1/2 border-b-2 mt-4 p-2 tracking-wider">
        Log in
      </div>
      <div className="flex flex-col items-center w-3/4 mt-4">
        <form
          data-testid="loginform"
          className="flex flex-col items-center w-full mt-4"
          onSubmit={(e) => handleLogin(e)}
        >
          <div className="flex md:flex-row flex-col w-full h-full md:items-baseline justify-center mb-6">
            <label
              htmlFor="email"
              className="font-semibold text-lg md:w-1/4 w-full text-left"
            >
              Email:
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={loginFormData.email}
              onChange={handleChange}
              placeholder="Enter your Email"
              className="w-full p-2 border-2 rounded-lg tracking-wider"
            />
          </div>
          <div className="flex md:flex-row flex-col w-full h-full md:items-baseline justify-center mb-6">
            <label
              htmlFor="password"
              className="font-semibold text-lg md:w-1/4 w-full text-left"
            >
              Password:
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={loginFormData.password}
              onChange={handleChange}
              placeholder="Enter your Password"
              className="w-full p-2 border-2 rounded-lg tracking-wider"
            />
          </div>
          <button
            type="submit"
            onClick={(e) => handleLogin(e)}
            disabled={!loginFormData.email || !loginFormData.password}
            className="w-full p-2 bg-blue-500 text-white rounded-lg disabled:bg-blue-300 disabled:cursor-not-allowed hover:bg-blue-600 cursor-pointer transition duration-200"
          >
            {loading ? <LoadingSpinner /> : "Log in"}
          </button>
        </form>
        <div className="flex flex-row items-center justify-center mt-4">
          <p className="font-semibold text-lg">Don't have an account?</p>
          <p
            onClick={() => setIsSignup(true)}
            className="font-bold text-lg text-blue-500 hover:underline ml-2 cursor-pointer"
          >
            Sign up
          </p>
        </div>
      </div>
    </section>
  );
}
