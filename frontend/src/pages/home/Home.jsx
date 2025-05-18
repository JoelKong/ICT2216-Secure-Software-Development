import SimplifiedPost from "../../components/home/SimplifiedPost";
import { useEffect, useState } from "react";
import { Plus } from "lucide-react";
import { useNavigate } from "react-router-dom";
import NavBar from "../../components/global/NavBar";

export default function HomePage({ user, searchTerm, scrollContainerRef }) {
  const navigate = useNavigate();

  // Need to useeffect to grab posts check token maybe on simplifiedpost

  return (
    <>
      <div className="min-h-screen">
        <div className="pt-20 w-full px-4">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6 max-w-6xl mx-auto">
            <div className="flex flex-col items-center text-center md:text-left w-full md:w-1/3 font-semibold space-y-2">
              <p>You are currently on {user.membership} plan</p>
              <p>You can create {user.post_limit} posts today</p>
              {user.membership !== "premium" && (
                <button className="border-2 px-3 py-2 bg-blue-300 hover:bg-blue-400 cursor-pointer text-sm rounded-lg transition">
                  Upgrade to premium plan to enjoy unlimited posting
                </button>
              )}
            </div>

            <div className="w-full md:w-1/3 text-center font-bold text-lg underline md:text-xl tracking-wide">
              Welcome, {user.username}
            </div>

            <div className="w-full md:w-1/3 flex justify-center md:justify-center">
              <button
                className="bg-violet-600 hover:bg-violet-700 cursor-pointer text-white font-medium px-4 py-2 rounded-md shadow-md flex items-center transition-colors"
                onClick={() => navigate("/create-posts")}
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
