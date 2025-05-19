import { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import LoginForm from "../../components/auth/LoginForm";
import SignupForm from "../../components/auth/SignupForm";
import { GlobalContext } from "../../utils/globalContext";

export default function AuthPage({ setIsAuthChecked }) {
  const { auth } = useContext(GlobalContext);
  const [isSignup, setIsSignup] = useState(false);
  const navigate = useNavigate();

  // If already logged in, redirect to /posts
  useEffect(() => {
    if (auth.isAuthenticated) {
      navigate("/posts");
    }
  }, [auth.isAuthenticated, navigate]);

  return (
    <section className="w-screen h-screen flex flex-col justify-center items-center mt-6 overflow-y-auto">
      <div className="flex flex-col justify-center items-center">
        <h1 className="font-bold text-2xl md:text-4xl tracking-wider">
          The Leonardo Discussion Room
        </h1>
        <h2 className="font-semibold text-md md:text-2xl italic underline mt-4">
          Enhancing Forums With Creativity And Clarity
        </h2>
      </div>
      {isSignup ? (
        <SignupForm
          setIsSignup={setIsSignup}
          setIsAuthChecked={setIsAuthChecked}
        />
      ) : (
        <LoginForm
          setIsSignup={setIsSignup}
          setIsAuthChecked={setIsAuthChecked}
        />
      )}
    </section>
  );
}
