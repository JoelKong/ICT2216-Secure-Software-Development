import fetchWithAuth from "./fetchWithAuth";
import checkRateLimit from "./checkRateLimit";
import handleRateLimitResponse from "./handleRateLimitResponse";
import { API_ENDPOINT, DELETE_POSTS_ROUTE } from "../const";

export function editPost(navigate, postId) {
  if (!postId) return;
  navigate(`/edit-post/${postId}`);
}

export async function deletePost(
  postId,
  {
    getAuthToken,
    updateAuthToken,
    handleLogout,
    rateLimit,
    setRateLimit,
    setModal,
    onSuccess = () => {},
    onFail = () => {},
  }
) {
  if (!window.confirm("Are you sure you want to delete this post?")) return;

  try {
    if (checkRateLimit(rateLimit, setRateLimit, setModal)) {
      return;
    }

    const res = await fetchWithAuth(
      `${API_ENDPOINT}/${DELETE_POSTS_ROUTE}/${postId}`,
      { method: "DELETE" },
      getAuthToken,
      updateAuthToken,
      handleLogout
    );

    const data = await res.json();

    if (handleRateLimitResponse(res, setRateLimit, setModal, "delete post")) {
      return;
    }

    if (!res.ok) {
      setModal({
        active: true,
        type: "fail",
        message: data.error || "Failed to delete post",
      });
      onFail(data);
      return;
    }

    setModal({
      active: true,
      type: "success",
      message: "Post deleted successfully",
    });
    setRateLimit({ attempts: 0, cooldown: false });

    onSuccess();
  } catch (err) {
    console.error(err);
    setModal({
      active: true,
      type: "fail",
      message: "An error occurred while deleting the post.",
    });
    onFail(err);
  }
}
