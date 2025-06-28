import { useState, useContext } from "react";
import { GlobalContext } from "../../utils/globalContext";
import DrawingCanvas from "../posts/DrawingCanvas";
import fetchWithAuth from "../../utils/fetchWithAuth";
import { API_ENDPOINT, CREATE_COMMENT_ROUTE } from "../../const";

export default function CommentForm({
  postId,
  parentId = null,
  onSuccess,
  onClose,
}) {
  const { getAuthToken, updateAuthToken, handleLogout, setModal } = useContext(GlobalContext);
  const [content, setContent] = useState("");
  const [image, setImage] = useState(null);
  const [drawingData, setDrawingData] = useState(null);
  const [setIsDrawing] = useState(false);
  const [mode, setMode] = useState(null);

  function handleFileChange(e) {
    setImage(e.target.files[0]);
    setDrawingData(null);
    setIsDrawing(false);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append("content", content);
    if (mode === "upload" && image) {
      formData.append("image", image);
    } else if (mode === "draw" && drawingData) {
      const blob = await fetch(drawingData).then((res) => res.blob());
      formData.append("image", blob, "drawing.png");
    }
    if (parentId) formData.append("parent_id", parentId);

    try {
      const res = await fetchWithAuth(
        `${API_ENDPOINT}/${CREATE_COMMENT_ROUTE}/${postId}`,
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
        setModal({ active: true, type: "fail", message: data.error || "Failed to post comment" });
        return;
      }

      onSuccess?.(data);
      setContent("");
      setImage(null);
      setDrawingData(null);
      onClose?.(); // close modal if needed
    } catch (err) {
      console.error("Comment error:", err);
      setModal({ active: true, type: "fail", message: "Comment submission failed." });
    }
  }

  return (
    <div className="max-h-[90vh] overflow-y-auto p-4">
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <form
          onSubmit={handleSubmit}
          className="bg-white text-black p-6 rounded-lg w-full max-w-lg space-y-4 relative"
        >
          <button
            type="button"
            onClick={onClose}
            className="absolute top-2 right-2 text-gray-500 hover:text-black"
          >
            ✕
          </button>
          <h2 className="text-lg font-bold">Add Comment</h2>

          <textarea
            className="w-full border rounded p-2"
            placeholder="Write your comment..."
            rows={4}
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />

          <div className="space-y-2">
            <label className="block text-sm font-medium">Comment Image (optional):</label>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => {
                  setMode("upload");
                  setDrawingData(null);
                  setImage(null);
                }}
                className={`px-3 py-1 rounded border ${mode === "upload" ? "bg-blue-600 text-white" : "bg-white text-black"
                  }`}
              >
                Upload
              </button>
              <button
                type="button"
                onClick={() => {
                  setMode("draw");
                  setDrawingData(null);
                  setImage(null);
                }}
                className={`px-3 py-1 rounded border ${mode === "draw" ? "bg-blue-600 text-white" : "bg-white text-black"
                  }`}
              >
                Draw
              </button>
            </div>

            {mode === "upload" && (
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className="mt-2"
              />
            )}

            {mode === "draw" && (
              <div className="mt-2">
                <DrawingCanvas onSave={setDrawingData} />
              </div>
            )}
          </div>

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Submit
          </button>
        </form>
      </div>
    </div>
  );
}