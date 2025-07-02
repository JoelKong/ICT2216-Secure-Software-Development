import { useEffect, useState, useContext } from "react";
import { API_ENDPOINT, FETCH_COMMENTS_ROUTE } from "../../const";
import fetchWithAuth from "../../utils/fetchWithAuth";
import { GlobalContext } from "../../utils/globalContext";
import CommentThread from "./CommentThread";
import CommentForm from "./CommentForm";

export default function CommentSection({ postId }) {
  const { getAuthToken, updateAuthToken, handleLogout } = useContext(GlobalContext);
  const [comments, setComments] = useState([]);
  const [showForm, setShowForm] = useState(false);

  function buildCommentTree(flatComments) {
    const map = new Map();
    const roots = [];

    // Initialize map and set up reply containers
    flatComments.forEach((comment) => {
      comment.replies = [];
      map.set(comment.comment_id, comment);
    });

    flatComments.forEach((comment) => {
      if (comment.parent_id) {
        const parent = map.get(comment.parent_id);
        if (parent) {
          parent.replies.push(comment);
        } else {
          roots.push(comment); // fallback
        }
      } else {
        roots.push(comment);
      }
    });

    return roots;
  }


  async function loadComments() {
    try {
      const res = await fetchWithAuth(
        `${API_ENDPOINT}/${FETCH_COMMENTS_ROUTE}/${postId}`,
        { method: "GET" },
        getAuthToken,
        updateAuthToken,
        handleLogout
      );

      if (!res.ok) throw new Error("Failed to load comments");
      const data = await res.json();
      const tree = buildCommentTree(data.comments || []);
      setComments(tree);
    } catch (err) {
      console.error("Error loading comments:", err);
    }
  }

  useEffect(() => {
    loadComments();
  }, [postId]);

  function handleNewComment(newComment) {
    setComments((prevTree) => {
      // Flatten existing tree to flat list
      const flatList = flattenComments(prevTree);

      // Add new comment to flat list
      flatList.push(newComment);

      // Rebuild tree from updated flat list
      return buildCommentTree(flatList);
    });
  }

  // Utility to flatten comment tree to a flat array
  function flattenComments(tree) {
    const flat = [];
    function recurse(nodes) {
      nodes.forEach(node => {
        flat.push(node);
        if (node.replies?.length) recurse(node.replies);
      });
    }
    recurse(tree);
    return flat;
  }


  return (
    <div className="mt-8 space-y-4">
      <h2 className="text-xl font-semibold">Comments</h2>
      <button
        onClick={() => setShowForm(true)}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Add Comment
      </button>

      {showForm && (
        <CommentForm
          postId={postId}
          onSuccess={handleNewComment}
          onClose={() => setShowForm(false)}
        />
      )}

      {comments.length === 0 ? (
        <p className="text-gray-400">No comments yet.</p>
      ) : (
        comments.map((comment) => (
          <CommentThread key={comment.comment_id} comment={comment} />
        ))
      )}
    </div>
  );
}