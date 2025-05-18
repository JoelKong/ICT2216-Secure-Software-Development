import { useState, useEffect, useRef } from "react";
import { Heart, MessageCircle, ArrowUp } from "lucide-react";
import formatTimestamp from "../../utils/formatTimestamp";
import { useNavigate } from "react-router-dom";
import { FETCH_POSTS_ROUTE, API_ENDPOINT, LIKE_POST_ROUTE } from "../../const";

export default function SimplifiedPost({
  scrollContainerRef,
  searchTerm = "",
  userId = null,
}) {
  const [likedPosts, setLikedPosts] = useState({});
  const [sortBy, setSortBy] = useState("recent");
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [offset, setOffset] = useState(0);
  const [showBackToTop, setShowBackToTop] = useState(false);
  const fetchTimerRef = useRef(null);
  const navigate = useNavigate();
  const limit = 10;

  // Fetch all posts
  async function fetchPosts(sortBy, offsetToFetch) {
    if (loading || !hasMore) return;
    setLoading(true);

    const token = localStorage.getItem("access_token");
    const params = new URLSearchParams({
      sort_by: sortBy,
      limit,
      offset: offsetToFetch,
    });
    if (searchTerm) params.append("search", searchTerm);
    if (userId) params.append("user_id", userId);

    try {
      const res = await fetch(
        `${API_ENDPOINT}/${FETCH_POSTS_ROUTE}?${params.toString()}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const data = await res.json();

      // If no data received
      if (data.length === 0) {
        setHasMore(false);
        setLoading(false);
        return;
      }

      if (offsetToFetch === 0) {
        setPosts(data);
      } else {
        const existingPostIds = new Set(posts.map((post) => post.post_id));
        const newPosts = data.filter(
          (post) => !existingPostIds.has(post.post_id)
        );

        // Only append non-duplicate posts
        if (newPosts.length > 0) {
          setPosts((prev) => [...prev, ...newPosts]);
        }

        if (newPosts.length < data.length || data.length < limit) {
          setHasMore(false);
        }
      }

      setOffset(offsetToFetch + limit);
    } catch (err) {
      console.error("Error fetching posts:", err);
      setHasMore(false);
    } finally {
      setLoading(false);
    }
  }

  // Navigate to specific post detail page
  const handlePostClick = (postId) => {
    navigate(`/posts/${postId}`);
  };

  // Toggle like function
  async function toggleLike(postId) {
    const token = localStorage.getItem("access_token");
    try {
      // await fetch(`${API_ENDPOINT}/${LIKE_POST_ROUTE}/${postId}`, {
      //   method: "POST",
      //   headers: {
      //     Authorization: `Bearer ${token}`,
      //   },
      // });

      setLikedPosts((prev) => ({
        ...prev,
        [postId]: !prev[postId],
      }));
    } catch (err) {
      console.error("Error toggling like:", err);
    }
  }

  // Go back to top
  const handleBackToTop = () => {
    scrollContainerRef.current?.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Reset and fetch when sort changes
  useEffect(() => {
    if (fetchTimerRef.current) {
      clearTimeout(fetchTimerRef.current);
    }

    setPosts([]);
    setOffset(0);
    setHasMore(true);

    setTimeout(() => {
      fetchPosts(sortBy, 0);
    }, 50);
  }, [sortBy, searchTerm]);

  useEffect(() => {
    if (hasMore && offset === 0) {
      fetchPosts(sortBy, 0);
    }
  }, [sortBy, hasMore]);

  // Lazy load on scroll
  useEffect(() => {
    const handleScroll = () => {
      const el = scrollContainerRef.current;
      if (!el) return;

      const scrollPosition = el.scrollTop + el.clientHeight;
      const documentHeight = el.scrollHeight;
      const distanceFromBottom = documentHeight - scrollPosition;

      // Load more content when user is 100px from bottom
      if (distanceFromBottom < 100 && !loading && hasMore) {
        if (fetchTimerRef.current) {
          clearTimeout(fetchTimerRef.current);
        }

        // Set a short delay (300ms) to debounce rapid scroll events
        fetchTimerRef.current = setTimeout(() => {
          fetchPosts(sortBy, offset);
        }, 300);
      }

      setShowBackToTop(el.scrollTop > 400);
    };

    const scrollContainer = scrollContainerRef.current;
    if (scrollContainer) {
      scrollContainer.addEventListener("scroll", handleScroll);
      return () => {
        scrollContainer.removeEventListener("scroll", handleScroll);
        if (fetchTimerRef.current) {
          clearTimeout(fetchTimerRef.current);
        }
      };
    }
  }, [offset, hasMore, loading, sortBy, scrollContainerRef]);

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
          className="border-2 rounded px-2 py-1 text-sm bg-white hover:bg-gray-100 cursor-pointer"
        >
          <option value="recent">Sort by Recent</option>
          <option value="likes">Sort by Likes</option>
          <option value="comments">Sort by Comments</option>
        </select>
      </div>

      <div className="space-y-4">
        {posts.map((post) => (
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
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleLike(post.post_id);
                  }}
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
                  onClick={(e) => {
                    e.stopPropagation();
                    handlePostClick(post.post_id);
                  }}
                >
                  <MessageCircle className="h-5 w-5" />
                  <span>{post.comments}</span>
                </button>
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="text-center text-black py-4 text-xl">Loading...</div>
        )}
        {posts.length === 0 && !loading && (
          <div className="text-center text-black py-4 text-xl">
            No Posts Found
          </div>
        )}
        {!hasMore && posts.length > 0 && (
          <div className="text-center text-black py-4">No more posts.</div>
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
