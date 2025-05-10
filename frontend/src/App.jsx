import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import Modal from "./components/global/Modal";
import LoginPage from "./pages/login/LoginPage";
import "./App.css";

function App() {
  // Set up global modal
  const [modal, setModal] = useState({
    active: false,
    type: "fail",
    message: "",
  });

  // Turn off modal
  useEffect(() => {
    const timeout = setTimeout(() => {
      setModal({ active: false, type: "fail", message: "" });
    }, 3000);
    return () => clearTimeout(timeout);
  }, [modal]);

  return (
    <>
      {modal.active && <Modal modal={modal} />}
      <main className="w-screen h-screen fixed bg-gradient-to-b from-blue-500 to-purple-500 overflow-y-auto overflow-x-clip">
        <Routes>
          <Route path="/" element={<LoginPage setModal={setModal} />} />
        </Routes>
      </main>
    </>
  );
}

export default App;
