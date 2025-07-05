import { useState, useRef, useEffect, useContext } from "react";
import { User } from "lucide-react";
import SearchBar from "./SearchBar";
import upgradeMembership from "../../utils/upgradeMembership";
import { GlobalContext } from "../../utils/globalContext";
export default function NavBar({ setSearchTerm, activeTab }) {
  const { auth, handleLogout, getAuthToken, updateAuthToken } =
    useContext(GlobalContext);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isUpgrading, setIsUpgrading] = useState(false);
  const dropdownRef = useRef(null);

  // Log out on request by removing tokens from local storage and resetting auth state
  function logout() {
    handleLogout();
  }

  const handleUpgrade = async () => {
    setIsUpgrading(true);
    try {
      await upgradeMembership(getAuthToken, updateAuthToken, handleLogout);
    } catch (error) {
      console.error("Failed to upgrade membership:", error);
    } finally {
      setIsUpgrading(false);
    }
  };

  // Close user dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <nav className="bg-white shadow-md fixed top-0 left-0 right-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <a
              href="/posts"
              className="text-gray-800 font-medium text-lg hover:text-blue-600 transition-colors"
            >
              Home
            </a>
          </div>

          {(location.pathname === "/posts" ||
            (location.pathname === "/profile" && activeTab === "posts")) && (
            <SearchBar setSearchTerm={setSearchTerm} />
          )}

          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              className="flex items-center cursor-pointer focus:outline-none"
            >
              {auth.user?.profilePicture ? (
                <img
                  src={auth.user.profile_picture}
                  alt="User profile"
                  className="h-8 w-8 rounded-full object-cover border-2 border-gray-200"
                />
              ) : (
                <div className="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center">
                  <User className="h-5 w-5 text-gray-500" />
                </div>
              )}
            </button>

            {isDropdownOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 ring-1 ring-black ring-opacity-5">
                <a
                  href="/profile"
                  className="block px-4 py-2 text-sm text-center text-gray-700 hover:bg-gray-100"
                >
                  View my profile
                </a>
                {auth.user.membership === "basic" && (
                  <button
                    onClick={handleUpgrade}
                    disabled={isUpgrading}
                    className="block px-4 py-2 w-full text-sm text-gray-700 hover:bg-gray-100 cursor-pointer disabled:opacity-75 disabled:cursor-not-allowed"
                  >
                    {isUpgrading ? (
                      <div className="flex items-center justify-center">
                        <svg
                          className="animate-spin -ml-1 mr-3 h-5 w-5"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          ></circle>
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          ></path>
                        </svg>
                        Upgrading...
                      </div>
                    ) : (
                      "Upgrade to premium"
                    )}
                  </button>
                )}
                <button
                  onClick={() => logout()}
                  className="block px-4 py-2 w-full text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
