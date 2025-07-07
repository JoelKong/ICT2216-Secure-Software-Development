import { useState, useEffect, useRef, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import fetchWithAuth from "../../utils/fetchWithAuth";
import { API_ENDPOINT, FETCH_POSTS_ROUTE, EDIT_POST_ROUTE } from "../../const";
import { GlobalContext } from "../../utils/globalContext";
import DrawingCanvas from "./DrawingCanvas";

export default function EditPostForm() {
  const { postId } = useParams();
  const navigate = useNavigate();
  const { getAuthToken, updateAuthToken, handleLogout, setModal } =
    useContext(GlobalContext);

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [existingImage, setExistingImage] = useState(null);
  const [changeImage, setChangeImage] = useState(false);
  const [imageMode, setImageMode] = useState("upload");
  const [uploadedImage, setUploadedImage] = useState(null);
  const [savedDrawing, setSavedDrawing] = useState(null);
  const drawingCanvasRef = useRef(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Fetch existing post data on mount
  useEffect(() => {
    console.log("Effect triggered:");
    console.log("postId:", postId);
    console.log("getAuthToken:", getAuthToken);
    console.log("updateAuthToken:", updateAuthToken);
    console.log("handleLogout:", handleLogout);
    console.log("setModal:", setModal);
    async function fetchPost() {
      try {
        const res = await fetchWithAuth(
          `${API_ENDPOINT}/${FETCH_POSTS_ROUTE}/${postId}/edit`,
          { method: "GET" },
          getAuthToken,
          updateAuthToken,
          handleLogout
        );
        if (!res.ok) {
          navigate("/");
          return;
        }
        const data = await res.json();
        setTitle(data.title);
        setContent(data.content);
        setExistingImage(
          data.image
            ? `${API_ENDPOINT}/api/posts${
                data.image.startsWith("/") ? data.image : "/" + data.image
              }`
            : null
        );
      } catch (err) {
        console.error(err);
        setModal({
          active: true,
          type: "fail",
          message: "Failed to load post data.",
        });
      }
    }
    fetchPost();
  }, [postId, getAuthToken, updateAuthToken, handleLogout, setModal]);

  // Handle form submit
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    const formData = new FormData();
    formData.append("title", title);
    formData.append("content", content);

    if (changeImage) {
      if (imageMode === "upload" && uploadedImage) {
        formData.append("image", uploadedImage);
      } else if (imageMode === "draw") {
        if (!savedDrawing) {
          setModal({
            active: true,
            type: "fail",
            message: "Please save your drawing before submitting.",
          });
          setIsSubmitting(false);
          return;
        }
        const blob = await (await fetch(savedDrawing)).blob();
        formData.append("image", blob, "drawing.png");
      }
    }

    try {
      const res = await fetchWithAuth(
        `${API_ENDPOINT}/${EDIT_POST_ROUTE}/${postId}`,
        {
          method: "PUT",
          body: formData,
        },
        getAuthToken,
        updateAuthToken,
        handleLogout
      );

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || "Failed to update post");
      }

      setModal({ active: true, type: "success", message: "Post updated!" });
      navigate(`/posts/${postId}`);
    } catch (err) {
      console.error(err);
      setModal({ active: true, type: "fail", message: err.message });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="p-6 bg-white rounded space-y-4 max-w-2xl mx-auto"
    >
      <h2 className="text-2xl font-bold">Edit Post</h2>

      <input
        type="text"
        placeholder="Post title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
        className="border px-4 py-2 rounded w-full"
      />

      <textarea
        placeholder="Write your post here..."
        value={content}
        onChange={(e) => setContent(e.target.value)}
        rows={6}
        required
        className="border px-4 py-2 rounded w-full"
      ></textarea>

      {!changeImage && existingImage && (
        <div>
          <p>Current Image:</p>
          <img src={existingImage} alt="Post" className="w-64 mb-2 rounded" />
          <button
            type="button"
            onClick={() => setChangeImage(true)}
            className="bg-yellow-400 text-black px-3 py-1 rounded hover:bg-yellow-500 cursor-pointer"
          >
            Change Image
          </button>
        </div>
      )}

      {changeImage && (
        <>
          {/* Image mode selector */}
          <div className="flex space-x-6 mb-4">
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="radio"
                name="imageMode"
                value="upload"
                checked={imageMode === "upload"}
                onChange={() => {
                  setImageMode("upload");
                  setUploadedImage(null);
                }}
              />
              <span>Upload Image</span>
            </label>
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="radio"
                name="imageMode"
                value="draw"
                checked={imageMode === "draw"}
                onChange={() => {
                  setImageMode("draw");
                  setUploadedImage(null);
                }}
              />
              <span>Draw Image</span>
            </label>
          </div>

          {/* Upload input */}
          {imageMode === "upload" && (
            <label className="bg-gray-200 text-black px-4 py-2 rounded cursor-pointer inline-block hover:bg-gray-300">
              Upload Image
              <input
                type="file"
                accept="image/*"
                onChange={(e) => {
                  setUploadedImage(e.target.files[0]);
                }}
                className="block mt-2"
              />
            </label>
          )}

          {imageMode === "draw" && (
            <DrawingCanvas
              ref={drawingCanvasRef}
              width={400}
              height={300}
              backgroundColor="#fff"
              onSave={(dataUrl) => {
                setSavedDrawing(dataUrl); // Save the dataURL for preview and submission
                setUploadedImage(null); // Clear uploaded image if any
              }}
            />
          )}

          {/* Cancel image change */}
          <button
            type="button"
            className="mt-4 bg-gray-300 text-black px-4 py-2 rounded hover:bg-gray-400 cursor-pointer mr-4"
            onClick={() => {
              setChangeImage(false);
              setImageMode("upload");
              setUploadedImage(null);
              if (drawingCanvasRef.current) drawingCanvasRef.current.clear();
            }}
          >
            Cancel Image Change
          </button>
        </>
      )}

      <button
        type="submit"
        disabled={isSubmitting}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 cursor-pointer"
      >
        {isSubmitting ? "Saving..." : "Update Post"}
      </button>
    </form>
  );
}
