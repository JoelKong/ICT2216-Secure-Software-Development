import { useParams } from "react-router-dom";
import { useEffect, useState, useContext } from "react";
import { GlobalContext } from "../../utils/globalContext";
import fetchWithAuth from "../../utils/fetchWithAuth";
import { API_ENDPOINT, FETCH_POSTS_ROUTE } from "../../const";

export default function PostDetail() {
  const { postId } = useParams();
  const { getAuthToken, updateAuthToken, handleLogout } = useContext(GlobalContext);

  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);

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

  return (
    <div className="pt-20 p-6 max-w-3xl mx-auto text-white">
      <h1 className="text-3xl font-bold mb-4">{post.title}</h1>
      <p className="text-gray-200 mb-2">by {post.username}</p>
      <p className="mb-6">{post.content}</p>
      {post.image && (
        <img
          src={post.image}
          alt={post.title}
          className="w-full max-h-[400px] object-cover rounded"
        />
      )}
    </div>
  );
}
