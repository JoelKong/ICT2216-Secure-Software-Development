import { useState } from "react";

export default function LoginForm({ setIsSignup, setModal }) {
  // State for login form data and modal
  const [loginFormData, setLoginFormData] = useState({
    username: "",
    password: "",
  });

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
    try {
      const response = await fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(loginFormData),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Login successful:", data);
        // Handle successful login (e.g., redirect or store token)
      } else {
        console.error("Login failed");
        // Handle login failure (e.g., show error message)
      }
    } catch (error) {
      setModal({
        active: true,
        type: "fail",
        message: "Something went wrong. Please try again.",
      });
      console.error("Error during login:", error);
    }
  }

  return (
    <section className="flex flex-col items-center w-11/12 md:w-7/12 pb-10 mt-4 border-2 rounded-lg">
      <div className="font-semibold text-2xl text-center w-1/2 border-b-2 mt-4 p-2 tracking-wider">
        Log in
      </div>
      <div className="flex flex-col items-center w-3/4 mt-4">
        <form
          className="flex flex-col items-center w-full mt-4"
          onSubmit={(e) => handleLogin(e)}
        >
          <div className="flex md:flex-row flex-col w-full h-full md:items-baseline justify-center mb-6">
            <label
              htmlFor="username"
              className="font-semibold text-lg w-1/4 text-left"
            >
              Username:
            </label>
            <input
              type="text"
              name="username"
              value={loginFormData.username}
              onChange={handleChange}
              placeholder="Enter your Username"
              className="w-full p-2 border-2 rounded-lg tracking-wider"
            />
          </div>
          <div className="flex md:flex-row flex-col w-full h-full md:items-baseline justify-center mb-6">
            <label
              htmlFor="password"
              className="font-semibold text-lg w-1/4 text-left"
            >
              Password:
            </label>
            <input
              type="password"
              name="password"
              value={loginFormData.password}
              onChange={handleChange}
              placeholder="Enter your Password"
              className="w-full p-2 border-2 rounded-lg tracking-wider"
            />
          </div>
          <button
            type="submit"
            onClick={() => handleLogin(e)}
            className="w-full p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 cursor-pointer transition duration-200"
          >
            Log in
          </button>
        </form>
        <div className="flex flex-row items-center justify-center mt-4">
          <p className="font-semibold text-lg">Don't have an account?</p>
          <p
            onClick={() => setIsSignup(true)}
            className="font-bold text-lg text-blue-400 hover:underline ml-2 cursor-pointer"
          >
            Sign up
          </p>
        </div>
      </div>
    </section>
  );
}
