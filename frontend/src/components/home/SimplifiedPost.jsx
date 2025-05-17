import { useState } from "react";
import { Heart, MessageCircle, ArrowUp } from "lucide-react";
import formatTimestamp from "../../utils/formatTimestamp";
import { useNavigate } from "react-router-dom";

export default function SimplifiedPost() {
  const [likedPosts, setLikedPosts] = useState({});
  const [sortBy, setSortBy] = useState("recent");
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [offset, setOffset] = useState(0);
  const [showBackToTop, setShowBackToTop] = useState(false);
  const navigate = useNavigate();
  const limit = 10;

  // Fetch all posts
  async function fetchPosts(sortBy, offset) {
    setLoading(true);
    const token = localStorage.getItem("access_token");
    try {
      const res = await fetch(
        `/api/posts?sort_by=${sortBy}&limit=${limit}&offset=${offset}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const data = await res.json();
      if (data.length < limit) setHasMore(false);
      setPosts((prev) => (offset === 0 ? data : [...prev, ...data]));
    } catch (err) {
      setHasMore(false);
    }
    setLoading(false);
  }

  // Navigate to specific post detail page
  const handlePostClick = (postId) => {
    navigate(`/posts/${postId}`);
  };

  // Go back to top
  const handleBackToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  //   // Reset and fetch when sort changes
  //   useEffect(() => {
  //     setPosts([]);
  //     setOffset(0);
  //     setHasMore(true);
  //     fetchPosts(sortBy, 0);
  //   }, [sortBy]);

  //   // Lazy load on scroll
  //   useEffect(() => {
  //     if (!hasMore || loading) return;
  //     const handleScroll = () => {
  //       if (
  //         window.innerHeight + window.scrollY >= document.body.offsetHeight - 100
  //       ) {
  //         if (!loading && hasMore) {
  //           fetchPosts(sortBy, offset + limit);
  //           setOffset((prev) => prev + limit);
  //         }
  //       }
  //       setShowBackToTop(window.scrollY > 400);
  //     };
  //     window.addEventListener("scroll", handleScroll);
  //     return () => window.removeEventListener("scroll", handleScroll);
  //     // eslint-disable-next-line
  //   }, [offset, hasMore, loading, sortBy]);

  // Dummy data for posts
  const dummyPosts = [
    {
      post_id: 1,
      title: "Getting started with React and Tailwind CSS",
      content:
        "I've been using React with Tailwind CSS for my latest project and I'm loving the combination. The utility-first approach of Tailwind makes styling components so much faster, and React's component model works perfectly with it. Here's what I've learned so far... As someone who's worked with both Flask and Django for several years, I wanted to share my thoughts on when to use each framework. Django gives you a lot out of the box, which is great for rapid development, but Flask's minimalist approach give ",
      image: "/api/placeholder/400/300",
      username: "reactfan42",
      likes: 124,
      comments: 47,
      created_at: "2025-05-15T14:30:00",
      updated_at: "2025-05-15T14:30:00",
    },
    {
      post_id: 2,
      title: "Flask vs Django - Which Python framework should you choose?",
      content:
        "As someone who's worked with both Flask and Django for several years, I wanted to share my thoughts on when to use each framework. Django gives you a lot out of the box, which is great for rapid development, but Flask's minimalist approach gives you more flexibility...",
      image: "",
      username: "pythondev99",
      likes: 89,
      comments: 36,
      created_at: "2025-05-15T12:15:00",
      updated_at: "2025-05-15T12:45:00",
    },
    {
      post_id: 3,
      title: "Optimizing database queries in production",
      content:
        "After our site started experiencing slowdowns, we discovered some inefficient database queries were to blame. Here's how we identified and fixed the bottlenecks, resulting in a 60% decrease in response time...",
      image: "/api/placeholder/400/300",
      username: "dbwizard",
      likes: 213,
      comments: 52,
      created_at: "2025-05-15T10:20:00",
      updated_at: "2025-05-15T10:20:00",
    },
    {
      post_id: 4,
      title: "Authentication best practices for modern web apps",
      content:
        "Security is crucial for any web application. In this post, I'll cover the essential authentication practices every developer should implement, including password hashing, JWT implementation, refresh tokens, and more...",
      image: "",
      username: "securityguru",
      likes: 178,
      comments: 29,
      created_at: "2025-05-15T04:30:00",
      updated_at: "2025-05-15T05:15:00",
    },
    {
      post_id: 5,
      title: "My journey learning TypeScript as a JavaScript developer",
      content:
        "After years of writing vanilla JavaScript, I finally decided to give TypeScript a serious try. The learning curve was steeper than I expected, but the benefits have been well worth it. Let me share what I've learned and the challenges I faced...",
      image: "/api/placeholder/400/300",
      username: "jsdevlearner",
      likes: 97,
      comments: 41,
      created_at: "2025-05-14T18:45:00",
      updated_at: "2025-05-14T19:30:00",
    },
  ];

  const sortedPosts = [...dummyPosts].sort((a, b) => {
    if (sortBy === "recent") {
      const getEffectiveDate = (post) => post.updated_at ?? post.created_at;
      return new Date(getEffectiveDate(b)) - new Date(getEffectiveDate(a));
    }
    if (sortBy === "likes") {
      return b.likes - a.likes;
    }
    if (sortBy === "comments") {
      return b.comments - a.comments;
    }
    return 0;
  });

  return (
    <div className="mt-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          {sortBy === "recent"
            ? "Recent Discussions"
            : sortBy === "likes"
            ? "Most Liked Discussions"
            : "Most Commented Discussions"}
        </h1>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="border rounded px-2 py-1 text-sm bg-white hover:bg-gray-100 cursor-pointer"
        >
          <option value="recent">Sort by Recent</option>
          <option value="likes">Sort by Likes</option>
          <option value="comments">Sort by Comments</option>
        </select>
      </div>

      <div className="space-y-4">
        {sortedPosts.map((post) => (
          <div
            key={post.post_id}
            className="bg-white hover:bg-gray-100 rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
            onClick={() => handlePostClick(post.post_id)}
          >
            <div className="p-4 sm:p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                {post.title}
              </h2>

              <div className="text-sm text-gray-500 mb-3">
                Posted by <span className="text-blue-600">{post.username}</span>{" "}
                · {formatTimestamp(post.updated_at ?? post.created_at)}
                {post.updated_at &&
                  post.updated_at !== post.created_at &&
                  " (edited)"}
              </div>

              <div className="mb-4">
                <p className="text-gray-700 line-clamp-3">{post.content}</p>

                {post.image && (
                  <div className="mt-3 max-h-64 overflow-hidden rounded-md">
                    <img
                      src={post.image}
                      alt={post.title}
                      className="w-full object-cover"
                    />
                  </div>
                )}
              </div>

              <div
                className="flex items-center space-x-4 pt-2 border-t border-gray-100"
                onClick={(e) => e.stopPropagation()}
              >
                <button
                  onClick={() => toggleLike(post.post_id)}
                  className={`flex items-center space-x-1 cursor-pointer ${
                    likedPosts[post.post_id] ? "text-red-500" : "text-gray-500"
                  } hover:text-red-500`}
                >
                  <Heart
                    className={`h-5 w-5 ${
                      likedPosts[post.post_id] ? "fill-current" : ""
                    }`}
                  />
                  <span>
                    {likedPosts[post.post_id] ? post.likes + 1 : post.likes}
                  </span>
                </button>

                <button
                  className="flex items-center cursor-pointer space-x-1 text-gray-500 hover:text-blue-500"
                  onClick={() => handlePostClick(post.post_id)}
                >
                  <MessageCircle className="h-5 w-5" />
                  <span>{post.comments}</span>
                </button>
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="text-center text-gray-500 py-4">Loading...</div>
        )}
        {!hasMore && posts.length > 0 && (
          <div className="text-center text-gray-400 py-4">No more posts.</div>
        )}
      </div>
      {showBackToTop && (
        <button
          onClick={handleBackToTop}
          className="fixed bottom-8 scale-110 right-8 cursor-pointer bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700 transition"
          aria-label="Back to top"
        >
          <ArrowUp className="w-5 h-5" />
        </button>
      )}
    </div>
  );
}
