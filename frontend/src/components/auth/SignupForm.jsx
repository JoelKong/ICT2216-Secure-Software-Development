import { useState } from "react";
import LoadingSpinner from "../global/LoadingSpinner";
import { API_ENDPOINT, SIGNUP_ROUTE } from "../../const";
import checkRateLimit from "../../utils/checkRateLimit";
import { useNavigate } from "react-router-dom";

export default function SignupForm({
  setIsSignup,
  setModal,
  rateLimit,
  setRateLimit,
  setAuth,
}) {
  // State for login form data
  const [signupFormData, setSignupFormData] = useState({
    email: "",
    username: "",
    password: "",
    confirmPassword: "",
  });

  // State for loading processes
  const [loading, setLoading] = useState(false);

  // Navigation
  const navigate = useNavigate();

  // State for password validation
  const [passwordValid, setPasswordValid] = useState({
    length: false,
    uppercase: false,
    lowercase: false,
    number: false,
    specialChar: false,
  });

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setSignupFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Password validation check when password field changes
    if (name === "password") {
      validatePassword(value);
    }
  };

  // Password validation function
  function validatePassword(password) {
    setPasswordValid({
      length: password.length >= 8,
      uppercase: /[A-Z]/.test(password),
      lowercase: /[a-z]/.test(password),
      number: /\d/.test(password),
      specialChar: /[!@#$%^&*(),.?":{}|<>]/.test(password),
    });
  }

  // Signup function to send signup details to backend
  async function handleSignup(e) {
    e.preventDefault();
    setLoading(true);
    try {
      let error = "";

      // Check if rate limit reached
      if (checkRateLimit(rateLimit, setRateLimit, setModal)) {
        return;
      }

      // Input Validation
      if (
        !signupFormData.email ||
        !signupFormData.username ||
        !signupFormData.password ||
        !signupFormData.confirmPassword
      ) {
        error = "All fields are required";
      }

      // Regex validation for email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(signupFormData.email)) {
        error = "Please enter a valid email address";
      }

      // Password strength validation (minimum 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character)
      if (
        !passwordValid.length ||
        !passwordValid.uppercase ||
        !passwordValid.lowercase ||
        !passwordValid.number ||
        !passwordValid.specialChar
      ) {
        error =
          "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.";
      }

      // Confirmation of password validation
      if (signupFormData.password !== signupFormData.confirmPassword) {
        error = "Passwords do not match.";
      }

      if (error) {
        setModal({
          active: true,
          type: "fail",
          message: error,
        });
        return;
      }

      const response = await fetch(`${API_ENDPOINT}/${SIGNUP_ROUTE}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(signupFormData),
      });
      const data = await response.json();

      if (response.ok) {
        setModal({
          active: true,
          type: "pass",
          message: data.message,
        });
        setRateLimit({ attempts: 0, cooldown: false });
        setAuth({ isAuthenticated: true, token: data.token, user: data.user });
        // TODO: save token in localstorage
        navigate("/posts");
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
      console.error("Error during signup:", error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="flex flex-col items-center w-11/12 md:w-7/12 pb-10 mt-4 border-2 rounded-lg overflow-y-auto bg-white mb-6">
      <div className="font-semibold text-2xl text-center w-1/2 border-b-2 mt-4 p-2 tracking-wider">
        Sign up
      </div>
      <div className="flex flex-col items-center w-3/4 mt-4">
        <form
          className="flex flex-col items-center w-full mt-4"
          onSubmit={(e) => handleSignup(e)}
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
              value={signupFormData.email}
              onChange={handleChange}
              placeholder="Enter your Email"
              className="w-full p-2 border-2 rounded-lg tracking-wider"
            />
          </div>
          <div className="flex md:flex-row flex-col w-full h-full md:items-baseline justify-center mb-6">
            <label
              htmlFor="username"
              className="font-semibold text-lg md:w-1/4 w-full text-left"
            >
              Username:
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={signupFormData.username}
              onChange={handleChange}
              placeholder="Enter your Username"
              className="w-full p-2 border-2 rounded-lg tracking-wider"
            />
          </div>
          <div className="flex flex-col w-full">
            <div className="flex md:flex-row flex-col w-full h-full md:items-baseline justify-center mb-2">
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
                value={signupFormData.password}
                onChange={handleChange}
                placeholder="Enter your Password"
                className="w-full p-2 border-2 rounded-lg tracking-wider"
              />
            </div>
            <div className="w-full text-sm text-gray-600 mb-6">
              <ul className="flex flex-row flex-wrap justify-evenly">
                <li
                  className={`${
                    passwordValid.length ? "text-green-600" : "text-red-500"
                  }`}
                >
                  Minimum 8 characters
                </li>
                <li
                  className={`${
                    passwordValid.uppercase ? "text-green-600" : "text-red-500"
                  }`}
                >
                  At least one uppercase letter
                </li>
                <li
                  className={`${
                    passwordValid.lowercase ? "text-green-600" : "text-red-500"
                  }`}
                >
                  At least one lowercase letter
                </li>
                <li
                  className={`${
                    passwordValid.number ? "text-green-600" : "text-red-500"
                  }`}
                >
                  At least one number
                </li>
                <li
                  className={`${
                    passwordValid.specialChar
                      ? "text-green-600"
                      : "text-red-500"
                  }`}
                >
                  At least one special character
                </li>
              </ul>
            </div>
          </div>

          <div className="flex md:flex-row flex-col w-full h-full md:items-baseline justify-center mb-6">
            <label
              htmlFor="confirmPassword"
              className="font-semibold text-lg md:w-1/4 w-full text-left"
            >
              Confirm Password:
            </label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={signupFormData.confirmPassword}
              onChange={handleChange}
              placeholder="Re-enter your Password"
              className="w-full p-2 border-2 rounded-lg tracking-wider"
            />
          </div>
          <button
            type="submit"
            onClick={(e) => handleSignup(e)}
            disabled={
              !signupFormData.email ||
              !signupFormData.username ||
              !signupFormData.password ||
              !signupFormData.confirmPassword
            }
            className="w-full p-2 bg-blue-500 text-white rounded-lg disabled:bg-blue-300 disabled:cursor-not-allowed hover:bg-blue-600 cursor-pointer transition duration-200"
          >
            {loading ? <LoadingSpinner /> : "Sign up"}
          </button>
        </form>
        <div className="flex flex-row items-center justify-center mt-4">
          <p className="font-semibold text-lg">Already have an account?</p>
          <p
            onClick={() => setIsSignup(false)}
            className="font-bold text-lg text-blue-500 hover:underline ml-2 cursor-pointer"
          >
            Log in
          </p>
        </div>
      </div>
    </section>
  );
}
