import SimplifiedPost from "../../components/home/SimplifiedPost";
import { Plus } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import upgradeMembership from "../../utils/upgradeMembership";
import { useContext } from "react";
import { GlobalContext } from "../../utils/globalContext";

export default function HomePage({ searchTerm, scrollContainerRef }) {
  const { auth, getAuthToken, updateAuthToken, handleLogout } =
    useContext(GlobalContext);
  const navigate = useNavigate();
  const [isUpgrading, setIsUpgrading] = useState(false);

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

  return (
    <>
      <div className="min-h-screen">
        <div className="pt-20 w-full px-4">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6 max-w-6xl mx-auto">
            <div className="flex flex-col items-center text-center md:text-left w-full md:w-1/3 font-semibold space-y-2">
              <p>You are currently on {auth.user.membership} plan</p>
              {auth.user.membership === "basic" ? (
                <p>You can create {auth.user.post_limit} posts today</p>
              ) : (
                <p>You can create unlimited posts</p>
              )}
              {auth.user.membership !== "premium" && (
                <button
                  className="border-2 px-3 py-2 bg-blue-300 hover:bg-blue-400 cursor-pointer text-sm rounded-lg transition disabled:opacity-75 disabled:cursor-not-allowed"
                  onClick={handleUpgrade}
                  disabled={isUpgrading}
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
                    "Upgrade to premium plan to enjoy unlimited posting"
                  )}
                </button>
              )}
            </div>

            <div className="w-full md:w-1/3 text-center font-bold text-lg underline md:text-xl tracking-wide">
              Welcome, {auth.user.username}
            </div>

            <div className="w-full md:w-1/3 flex justify-center md:justify-center">
              <button
                className="bg-violet-600 hover:bg-violet-700 cursor-pointer text-white font-medium px-4 py-2 rounded-md shadow-md flex items-center transition-colors"
                onClick={() => navigate("/create-post")}
              >
                <Plus className="h-5 w-5 mr-1" />
                Create Post
              </button>
            </div>
          </div>
        </div>

        <div className="max-w-4xl mx-auto pb-10 px-4 sm:px-6">
          <SimplifiedPost
            scrollContainerRef={scrollContainerRef}
            searchTerm={searchTerm}
          />
        </div>
      </div>
    </>
  );
}
