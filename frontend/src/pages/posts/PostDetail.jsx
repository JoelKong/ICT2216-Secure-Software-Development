import { useParams } from "react-router-dom";
import { useEffect, useState, useContext } from "react";
import { GlobalContext } from "../../utils/globalContext";
import fetchWithAuth from "../../utils/fetchWithAuth";
import { API_ENDPOINT, FETCH_POSTS_ROUTE, LIKE_POST_ROUTE  } from "../../const";
import { Heart, MessageCircle } from "lucide-react";
import checkRateLimit from "../../utils/checkRateLimit";
import { editPost, deletePost } from "../../utils/postHelpers";
import { useNavigate } from "react-router-dom";
import CommentSection from "../../components/comments/CommentSection";

export default function PostDetail() {
  const { postId } = useParams();
  const { getAuthToken, updateAuthToken, handleLogout, auth, setModal, rateLimit, setRateLimit } = useContext(GlobalContext);

  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);

  const [liked, setLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(0);

  const [showComments, setShowComments] = useState(false);

  const navigate = useNavigate();

  function handleEditPost(postId) {
    editPost(navigate, postId);
  }

  async function handleDeletePost(postId) {
    await deletePost(postId, {
      getAuthToken,
      updateAuthToken,
      handleLogout,
      rateLimit,
      setRateLimit,
      setModal,
      onSuccess: () => navigate("/posts"),
    });
  }

  async function toggleLike() {
    try {
      // Check if rate limit reached (using your util)
      if (checkRateLimit(rateLimit, setRateLimit, setModal)) {
        return; // Exit if on cooldown
      }

      const res = await fetchWithAuth(
        `${API_ENDPOINT}/${LIKE_POST_ROUTE}/${postId}`,
        {
          method: "POST",
        },
        getAuthToken,
        updateAuthToken,
        handleLogout
      );

      if (res.ok) {
        const data = await res.json();
        setLiked(!liked);
        setLikesCount(data.likes);
        setRateLimit({ attempts: 0, cooldown: false });
      } else {
        const errorData = await res.json();
        setModal({
          active: true,
          type: "fail",
          message: errorData.error || "Failed to like post",
        });
      }
    } catch (err) {
      console.error("Error toggling like:", err);
      setModal({
        active: true,
        type: "fail",
        message: "An error occurred while liking the post.",
      });
    }
  }

  useEffect(() => {
    async function fetchPost() {
      try {
        const res = await fetchWithAuth(
          `${API_ENDPOINT}/${FETCH_POSTS_ROUTE}/${postId}`,
          { method: "GET" },
          getAuthToken,
          updateAuthToken,
          handleLogout
        );

        if (!res.ok) throw new Error("Post not found");

        const data = await res.json();
        setPost(data); // <-- Use data directly, not data.post

        // Set likes state
        setLikesCount(data.likes || 0);

        // Assuming API sends if user liked post or not in e.g. data.liked
        setLiked(data.liked || false);
      } catch (err) {
        console.error("Failed to fetch post:", err);
        setPost(null);
      } finally {
        setLoading(false);
      }
    }

    fetchPost();
  }, [postId]);

  if (loading) return <div className="text-center text-white">Loading...</div>;
  if (!post) return <div className="text-center text-white">Post not found.</div>;

  const postImageUrl = post?.image
    ? `${API_ENDPOINT}/api/posts${post.image.startsWith('/') ? post.image : '/' + post.image}`
    : null;

  return (
    <div className="pt-20 p-6 max-w-3xl mx-auto text-white">
      <h1 className="text-3xl font-bold mb-4">{post.title}</h1>
      <p className="text-gray-200 mb-2">by {post.username}</p>
      <p className="mb-6">{post.content}</p>
      {postImageUrl && (
        <img
          src={postImageUrl}
          alt={post.title}
          className="w-full max-h-[400px] object-cover rounded"
        />
      )}
      <div className="flex items-center space-x-4 mt-4">
        {/* Like Button */}
        <button
          onClick={toggleLike}
          aria-label="Like post"
          className={`flex items-center space-x-1 cursor-pointer ${
            liked ? "text-red-500" : "text-gray-500"
          } hover:text-red-500`}
        >
          <Heart className={`h-6 w-6 ${liked ? "fill-current" : ""}`} />
          <span>{likesCount}</span>
        </button>

        {/* Comment Button*/}
        <button
          className="flex items-center space-x-1 cursor-pointer text-gray-500 hover:text-blue-500"
          aria-label="Comment button"
          onClick={() => setShowComments((prev) => !prev)}
        >
          <MessageCircle className="h-6 w-6" />
          <span>{post.comments || 0}</span>
          {showComments ? "Hide Comments" : "Show Comments"}
        </button>

        {/* Edit and Delete Buttons - only visible if user's own post */}
        {auth.user && auth.user.user_id === post.user_id && (
          <>
            <button
              className="ml-4 px-3 py-1 bg-yellow-400 text-black rounded hover:bg-yellow-500"
              onClick={() => handleEditPost(post.post_id)}
            >
              Edit
            </button>
            <button
              className="ml-2 px-3 py-1 bg-red-400 text-black rounded hover:bg-red-500"
              onClick={() => handleDeletePost(post.post_id)}
            >
              Delete
            </button>
          </>
        )}
      </div>
      {showComments && <CommentSection postId={post.post_id} />}
    </div>
  );
}
