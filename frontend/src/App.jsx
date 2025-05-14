import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import Modal from "./components/global/Modal";
import "./App.css";
import AuthPage from "./pages/auth/AuthPage";

function App() {
  // Set up global modal
  const [modal, setModal] = useState({
    active: false,
    type: "fail",
    message: "",
  });

  // Set up front end side rate limiting based off request attempts
  const [rateLimit, setRateLimit] = useState({
    attempts: 0,
    cooldown: false,
  });

  // Turn off modal
  useEffect(() => {
    const timeout = setTimeout(() => {
      setModal({ active: false, type: "fail", message: "" });
    }, 3000);
    return () => clearTimeout(timeout);
  }, [modal]);

  // Set rate limit timer for 10 second cooldown
  useEffect(() => {
    if (rateLimit.cooldown) {
      const timer = setTimeout(() => {
        setRateLimit({ attempts: 0, cooldown: false });
      }, 10000);
      return () => clearTimeout(timer);
    }
  }, [rateLimit.cooldown]);

  return (
    <>
      {modal.active && <Modal modal={modal} />}
      <main className="w-screen h-screen fixed bg-gradient-to-b from-blue-500 to-purple-500 overflow-y-auto overflow-x-clip">
        <Routes>
          <Route
            path="/"
            element={
              <AuthPage
                setModal={setModal}
                rateLimit={rateLimit}
                setRateLimit={setRateLimit}
              />
            }
          />
        </Routes>
      </main>
    </>
  );
}

export default App;
