import { useState } from "react";
import LoginForm from "../../components/login/LoginForm";
import SignupForm from "../../components/login/SignupForm";

export default function LoginPage({ setModal }) {
  const [isSignup, setIsSignup] = useState(false);

  return (
    <section className="w-screen h-screen flex flex-col justify-center items-center mt-6 overflow-y-auto">
      <div className="flex flex-col justify-center items-center">
        <h1 className="font-bold text-2xl md:text-4xl tracking-wider">
          Leonardo Da Vinci's Recap
        </h1>
        <h2 className="font-semibold text-md md:text-2xl italic underline mt-4">
          Enhancing Forums With Creativity And Clarity
        </h2>
      </div>
      {isSignup ? (
        <SignupForm setIsSignup={setIsSignup} setModal={setModal} />
      ) : (
        <LoginForm setIsSignup={setIsSignup} setModal={setModal} />
      )}
    </section>
  );
}
