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
import fetchWithAuth from "./utils/fetchWithAuth";
import { useNavigate } from "react-router-dom";
import PostDetail from "./pages/posts/PostDetail";
import CreatePost from "./pages/posts/CreatePost";


function App() {
  const navigate = useNavigate();

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

  const [activeTab, setActiveTab] = useState("profile"); // default to 'profile'

  const getAuthToken = () => localStorage.getItem("access_token");

  const updateAuthToken = (newToken) => {
    localStorage.setItem("access_token", newToken);
    setAuth((prev) => ({
      ...prev,
      token: newToken,
      isAuthenticated: !!newToken,
    }));
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setAuth({ isAuthenticated: false, token: null, user: null });
    setSearchTerm("");
    setIsAuthChecked(true);
    navigate("/");
  };

  // Fetch user profile with token
  async function fetchUser() {
    try {
      const res = await fetchWithAuth(
        `${API_ENDPOINT}/${FETCH_USER_ROUTE}`,
        {
          method: "GET",
        },
        getAuthToken,
        updateAuthToken,
        handleLogout
      );
      const data = await res.json();
      if (res.ok && data.user) {
        setAuth({
          isAuthenticated: true,
          token: getAuthToken(),
          user: data.user,
        });
        setIsAuthChecked(true);
      } else {
        handleLogout();
      }
    } catch (err) {
      console.error("Failed to fetch user or session expired:", err);
      if (!auth.isAuthenticated) {
        handleLogout();
      }
    } finally {
      setIsAuthChecked(true);
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
      }, 30000);
      return () => clearTimeout(timer);
    }
  }, [rateLimit.cooldown]);

  // Fetch user
  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token) {
      fetchUser();
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
          value={{
            auth,
            rateLimit,
            setAuth,
            setModal,
            setRateLimit,
            getAuthToken,
            updateAuthToken,
            handleLogout,
          }}
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
              path="/posts/:postId"
              element={
                <PrivateRoute isAuthenticated={auth.isAuthenticated}>
                  <NavBar />
                  <PostDetail />
                </PrivateRoute>
              }
            />
            <Route
              path="/create-post"
              element={
                <PrivateRoute isAuthenticated={auth.isAuthenticated}>
                  <NavBar />
                  <CreatePost />
                </PrivateRoute>
              }
            />

            <Route
              path="/profile"
              element={
                <PrivateRoute isAuthenticated={auth.isAuthenticated}>
                  <NavBar
                    setSearchTerm={setSearchTerm}
                    activeTab={activeTab}
                  />
                  <Profile
                    scrollContainerRef={scrollContainerRef}
                    searchTerm={searchTerm}
                    activeTab={activeTab}
                    setActiveTab={setActiveTab}
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
