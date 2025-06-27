import { useState, useContext } from "react";
import { GlobalContext } from "../../utils/globalContext";
import fetchWithAuth from "../../utils/fetchWithAuth";
// import { API_ENDPOINT } from "../../const";
import { API_ENDPOINT, CREATE_POST_ROUTE } from "../../const";
import { useNavigate } from "react-router-dom";

export default function CreatePostForm() {
  const { getAuthToken, updateAuthToken, handleLogout, setModal } =
    useContext(GlobalContext);
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [image, setImage] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setIsSubmitting(true);

    const formData = new FormData();
    formData.append("title", title);
    formData.append("content", content);
    if (image) formData.append("image", image);

    try {
      const res = await fetchWithAuth(
        `${API_ENDPOINT}/${CREATE_POST_ROUTE}`,
        {
          method: "POST",
          body: formData,
        },
        getAuthToken,
        updateAuthToken,
        handleLogout
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Failed to create post");
      }

      setModal({
        active: true,
        type: "success",
        message: "Post created successfully!",
      });

      navigate(`/posts/${data.post_id}`);
    } catch (err) {
      console.error(err);
      setModal({
        active: true,
        type: "fail",
        message: err.message,
      });
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded-lg shadow-md space-y-4 max-w-2xl mx-auto"
    >
        <h2 className="text-2xl font-bold text-gray-800">Create a New Post</h2>

        <input
            type="text"
            placeholder="Post title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className="w-full border px-4 py-2 rounded"
        />

        <textarea
            placeholder="Write your post here..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={6}
            required
            className="w-full border px-4 py-2 rounded"
        ></textarea>

        <label className="bg-gray-200 text-black px-4 py-2 rounded cursor-pointer inline-block hover:bg-gray-300">
            Upload Image
            <input
                type="file"
                accept="image/*"
                onChange={(e) => setImage(e.target.files[0])}
                className="block"
            />
        </label>

        <button
            type="submit"
            disabled={isSubmitting}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
            {isSubmitting ? "Posting..." : "Post"}
        </button>
    </form>
  );
}