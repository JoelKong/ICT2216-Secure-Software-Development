import { Routes, Route } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import { GlobalContext } from "./utils/globalContext";
import Modal from "./components/global/Modal";
import AuthPage from "./pages/auth/AuthPage";
import HomePage from "./pages/home/Home";
import PrivateRoute from "./components/global/PrivateRoute";
import "./App.css";
import Profile from "./pages/profile/Profile";
import NavBar from "./components/global/NavBar";
import PaymentSuccess from "./pages/payment_success/PaymentSuccess";
import PaymentFailure from "./pages/payment_failure/PaymentFailure";
import { API_ENDPOINT, FETCH_USER_ROUTE } from "./const";

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
    isAuthenticated: false,
    token: null,
    user: null,
  });
  const [isAuthChecked, setIsAuthChecked] = useState(false);

  // Fetch user profile with token
  async function fetchUser(token) {
    console.log("fetching user");
    try {
      const res = await fetch(`${API_ENDPOINT}/${FETCH_USER_ROUTE}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          // credentials: "include"
        },
      });
      const data = await res.json();
      if (data.user) {
        setAuth({ isAuthenticated: true, token: token, user: data.user });
        setIsAuthChecked(true);
      } else {
        setAuth({ isAuthenticated: false, token: null, user: null });
        setIsAuthChecked(false);
        localStorage.removeItem("access_token");
      }
    } catch (err) {
      console.error(err);
      setAuth({ isAuthenticated: false, token: null, user: null });
      setIsAuthChecked(false);
      localStorage.removeItem("access_token");
    }
  }

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

  // Fetch user
  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token) {
      fetchUser(token);
    } else {
      setIsAuthChecked(true);
    }
  }, [isAuthChecked]);

  if (!isAuthChecked) {
    // Prevent any route rendering until auth is checked
    return (
      <div className="w-screen h-screen justify-center items-center">
        Loading...
      </div>
    );
  }

  return (
    <>
      {modal.active && <Modal modal={modal} />}
      <main
        className="w-screen h-screen fixed bg-gradient-to-b from-blue-500 to-purple-500 overflow-y-auto overflow-x-clip"
        ref={scrollContainerRef}
      >
        <GlobalContext.Provider
          value={{ auth, rateLimit, setAuth, setModal, setRateLimit }}
        >
          <Routes>
            <Route
              path="/"
              element={<AuthPage setIsAuthChecked={setIsAuthChecked} />}
            />
            <Route
              path="/posts"
              element={
                <PrivateRoute isAuthenticated={auth.isAuthenticated}>
                  <NavBar setSearchTerm={setSearchTerm} />
                  <HomePage
                    searchTerm={searchTerm}
                    scrollContainerRef={scrollContainerRef}
                  />
                </PrivateRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <PrivateRoute isAuthenticated={auth.isAuthenticated}>
                  <NavBar setSearchTerm={setSearchTerm} />
                  <Profile
                    scrollContainerRef={scrollContainerRef}
                    searchTerm={searchTerm}
                  />
                </PrivateRoute>
              }
            />
            <Route
              path="/success"
              element={
                <PrivateRoute isAuthenticated={auth.isAuthenticated}>
                  <PaymentSuccess />
                </PrivateRoute>
              }
            />
            <Route
              path="/failure"
              element={
                <PrivateRoute isAuthenticated={auth.isAuthenticated}>
                  <PaymentFailure />
                </PrivateRoute>
              }
            />
          </Routes>
        </GlobalContext.Provider>
      </main>
    </>
  );
}

export default App;
