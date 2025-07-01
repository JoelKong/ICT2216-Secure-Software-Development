import { useState } from "react";
import CommentForm from "./CommentForm";
import { API_ENDPOINT } from "../../const";

export default function CommentThread({ comment }) {
  const [showReplies, setShowReplies] = useState(false);
  const [showReplyForm, setShowReplyForm] = useState(false);

  const commentImageUrl = comment?.image
      ? `${API_ENDPOINT}/api/comments${comment.image.startsWith('/') ? comment.image : '/' + comment.image}`
      : null;

  return (
    <div className="ml-4 border-l pl-4 mb-4">
      <div className="text-sm mb-2">
        <p className="font-semibold">{comment.username}</p>
        <p>{comment.content}</p>
        {commentImageUrl && (
          <img
            src={commentImageUrl}
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