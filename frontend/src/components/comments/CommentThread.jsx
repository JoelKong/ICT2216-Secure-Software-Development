import { useState } from "react";
import CommentForm from "./CommentForm";

export default function CommentThread({ comment }) {
  const [showReplies, setShowReplies] = useState(false);
  const [showReplyForm, setShowReplyForm] = useState(false);

  return (
    <div className="ml-4 border-l pl-4 mb-4">
      <div className="text-sm mb-2">
        <p className="font-semibold">{comment.username}</p>
        <p>{comment.content}</p>
        {comment.image && (
          <img
            src={`${import.meta.env.VITE_API_BASE_URL}${comment.image}`}
            alt="comment"
            className="mt-2 max-w-xs rounded"
          />
        )}
        <button
          onClick={() => setShowReplyForm(true)}
          className="text-blue-500 text-xs mt-1"
        >
          Reply
        </button>
        {comment.replies?.length > 0 && (
          <button
            onClick={() => setShowReplies((s) => !s)}
            className="text-blue-400 text-xs ml-2"
          >
            {showReplies ? "Hide Replies" : `View Replies (${comment.replies.length})`}
          </button>
        )}
      </div>

      {showReplyForm && (
        <CommentForm
          postId={comment.post_id}
          parentId={comment.comment_id}
          onSuccess={() => setShowReplyForm(false)}
          onClose={() => setShowReplyForm(false)}
        />
      )}

      {showReplies &&
        comment.replies?.map((reply) => (
          <CommentThread key={reply.comment_id} comment={reply} />
        ))}
    </div>
  );
}