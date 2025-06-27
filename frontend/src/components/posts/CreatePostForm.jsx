import { useState, useContext, useEffect, useRef } from "react";
import { GlobalContext } from "../../utils/globalContext";
import fetchWithAuth from "../../utils/fetchWithAuth";
import { API_ENDPOINT, CREATE_POST_ROUTE } from "../../const";
import { useNavigate } from "react-router-dom";
import { fabric } from "fabric";

export default function CreatePostForm() {
  const { getAuthToken, updateAuthToken, handleLogout, setModal } = useContext(GlobalContext);
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  // New state to choose image input method
  const [imageMode, setImageMode] = useState("upload"); // "upload" or "draw"

  const [image, setImage] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Brush settings state
  const [brushSize, setBrushSize] = useState(2);
  const [brushColor, setBrushColor] = useState("#000000");

  const canvasRef = useRef(null);
  const fabricRef = useRef(null); // reference to Fabric canvas object
  const [drawnImage, setDrawnImage] = useState(null); // to preview/export

  useEffect(() => {
    if (imageMode === "draw") {
      const fabricCanvas = new fabric.Canvas(canvasRef.current, {
        isDrawingMode: true,
        backgroundColor: "#fff",
      });
      fabricCanvas.setHeight(300);
      fabricCanvas.setWidth(400);
      fabricCanvas.freeDrawingBrush.width = brushSize;
      fabricCanvas.freeDrawingBrush.color = brushColor;
      fabricRef.current = fabricCanvas;

      return () => {
        fabricCanvas.dispose();
        fabricRef.current = null;
        setDrawnImage(null);
      };
    } else {
      // Clean up if switching away from draw mode
      if (fabricRef.current) {
        fabricRef.current.dispose();
        fabricRef.current = null;
        setDrawnImage(null);
      }
    }
  }, [imageMode]);

  // Update brush properties when brushSize or brushColor changes (only if canvas exists)
  useEffect(() => {
    if (fabricRef.current) {
      fabricRef.current.freeDrawingBrush.width = brushSize;
      fabricRef.current.freeDrawingBrush.color = brushColor;
    }
  }, [brushSize, brushColor]);

  async function handleSubmit(e) {
    e.preventDefault();
    setIsSubmitting(true);

    const formData = new FormData();
    formData.append("title", title);
    formData.append("content", content);

    if (imageMode === "upload") {
      if (image) formData.append("image", image);
    } else if (imageMode === "draw") {
      if (drawnImage) {
        const blob = await (await fetch(drawnImage)).blob();
        formData.append("image", blob, "drawing.png");
      } else {
        setModal({
          active: true,
          type: "fail",
          message: "Please draw an image before submitting.",
        });
        setIsSubmitting(false);
        return;
      }
    }

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

        {/* Image Mode Selector */}
        <div className="flex space-x-4 items-center mb-4">
          <label>
            <input
              type="radio"
              name="imageMode"
              value="upload"
              checked={imageMode === "upload"}
              onChange={() => setImageMode("upload")}
              className="mr-2"
            />
            Upload Image
          </label>

          <label>
            <input
              type="radio"
              name="imageMode"
              value="draw"
              checked={imageMode === "draw"}
              onChange={() => setImageMode("draw")}
              className="mr-2"
            />
            Draw Image
          </label>
        </div>

        {/* Conditionally show upload or drawing */}
        {imageMode === "upload" && (
          <label className="bg-gray-200 text-black px-4 py-2 rounded cursor-pointer inline-block hover:bg-gray-300">
            Upload Image
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setImage(e.target.files[0])}
              className="block"
            />
          </label>
        )}

        {imageMode === "draw" && (
          <div>
            {/* Brush controls */}
            <div className="flex items-center space-x-4 mb-2">
              <label className="flex items-center space-x-2">
                <span>Brush Size:</span>
                <input
                  type="range"
                  min="1"
                  max="20"
                  value={brushSize}
                  onChange={(e) => setBrushSize(Number(e.target.value))}
                />
                <span>{brushSize}px</span>
              </label>

              <label className="flex items-center space-x-2">
                <span>Brush Color:</span>
                <input
                  type="color"
                  value={brushColor}
                  onChange={(e) => setBrushColor(e.target.value)}
                />
              </label>
            </div>
            <canvas
              ref={canvasRef}
              className="border border-gray-300 rounded"
            />
            <div className="mt-3 flex gap-2">
              <button
                type="button"
                onClick={() => {
                  fabricRef.current.clear();
                  fabricRef.current.backgroundColor = "#fff";
                  setDrawnImage(null);
                }}
                className="px-4 py-1 bg-red-500 text-white rounded hover:bg-red-600"
              >
                Clear Canvas
              </button>

              <button
                type="button"
                onClick={() => {
                  const dataURL = fabricRef.current.toDataURL({
                    format: "png",
                    quality: 0.8,
                  });
                  setDrawnImage(dataURL);
                }}
                className="px-4 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                Save Drawing
              </button>
            </div>

            {drawnImage && (
              <div className="mt-4">
                <p className="mb-1">Preview:</p>
                <img
                  src={drawnImage}
                  alt="Drawn preview"
                  className="border rounded max-w-full"
                />
              </div>
            )}
          </div>
        )}

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