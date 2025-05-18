import { Routes, Route } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import Modal from "./components/global/Modal";
import AuthPage from "./pages/auth/AuthPage";
import HomePage from "./pages/home/Home";
import PrivateRoute from "./components/global/PrivateRoute";
import "./App.css";
import Profile from "./pages/profile/Profile";
import NavBar from "./components/global/NavBar";

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

  // Global screen ref to track scroll position
  const scrollContainerRef = useRef(null);

  // Global search term for navbar
  const [searchTerm, setSearchTerm] = useState("");

  // Authenticate user based off token
  const [auth, setAuth] = useState({
    isAuthenticated: true, // TODO: i bypass first till they fix session
    token: null,
    user: { user_id: 1 },
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

  // For caching token if we wan do this
  // useEffect(() => {
  //   const token = localStorage.getItem("token");
  //   const user = JSON.parse(localStorage.getItem("user"));
  //   if (token && user) {
  //     setAuth({ isAuthenticated: true, token, user });
  //   }
  // }, []);

  useEffect(() => {
    console.log(auth);
  }, []);

  return (
    <>
      {modal.active && <Modal modal={modal} />}
      <main
        className="w-screen h-screen fixed bg-gradient-to-b from-blue-500 to-purple-500 overflow-y-auto overflow-x-clip"
        ref={scrollContainerRef}
      >
        <Routes>
          <Route
            path="/"
            element={
              <AuthPage
                setModal={setModal}
                rateLimit={rateLimit}
                setRateLimit={setRateLimit}
                setAuth={setAuth}
              />
            }
          />
          <Route
            path="/posts"
            element={
              <PrivateRoute isAuthenticated={auth.isAuthenticated}>
                <NavBar
                  user={auth.user}
                  setAuth={setAuth}
                  setSearchTerm={setSearchTerm}
                />
                <HomePage
                  user={auth.user}
                  searchTerm={searchTerm}
                  scrollContainerRef={scrollContainerRef}
                  setModal={setModal}
                  rateLimit={rateLimit}
                  setRateLimit={setRateLimit}
                />
              </PrivateRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <PrivateRoute isAuthenticated={auth.isAuthenticated}>
                <NavBar
                  user={auth.user}
                  setAuth={setAuth}
                  setSearchTerm={setSearchTerm}
                />
                <Profile
                  scrollContainerRef={scrollContainerRef}
                  searchTerm={searchTerm}
                  userId={auth.user?.user_id}
                />
              </PrivateRoute>
            }
          />
        </Routes>
      </main>
    </>
  );
}

export default App;
