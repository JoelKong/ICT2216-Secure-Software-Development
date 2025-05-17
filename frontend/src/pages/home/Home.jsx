import SimplifiedPost from "../../components/home/SimplifiedPost";
import { useEffect } from "react";
import { Plus } from "lucide-react";

export default function HomePage({ user }) {
  // Need to useeffect to grab posts check token maybe on simplifiedpost

  return (
    <div className="min-h-screen">
      <div className="pt-20 w-full flex justify-end">
        <button className="bg-violet-600 hover:bg-violet-700 mr-6 cursor-pointer text-white font-medium px-4 py-2 rounded-md shadow-md flex items-center transition-colors">
          <Plus className="h-5 w-5 mr-1" />
          Create Post
        </button>
      </div>
      <div className="max-w-4xl mx-auto pb-10 px-4 sm:px-6">
        <SimplifiedPost />
      </div>
    </div>
  );
}
