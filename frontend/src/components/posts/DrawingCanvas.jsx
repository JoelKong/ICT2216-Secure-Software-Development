import React, {
  useEffect,
  useRef,
  useImperativeHandle,
  forwardRef,
  useState,
} from "react";
import { fabric } from "fabric";

const DrawingCanvas = forwardRef(
  (
    {
      width = 400,
      height = 300,
      backgroundColor = "#fff",
      onSave,
      initialBrushColor = "#000",
      initialBrushWidth = 2,
    },
    ref
  ) => {
    const canvasRef = useRef(null);
    const fabricRef = useRef(null);

    // Undo/Redo stacks
    const undoStack = useRef([]);
    const redoStack = useRef([]);

    // Brush states
    const [brushColor, setBrushColor] = useState(initialBrushColor);
    const [brushWidth, setBrushWidth] = useState(initialBrushWidth);
    const [isEraser, setIsEraser] = useState(false);

    // Track saved drawing data URL
    const [savedImage, setSavedImage] = useState(null);

    // Save current state to undo stack
    const saveState = () => {
      if (!fabricRef.current) return;
      const json = fabricRef.current.toJSON();
      undoStack.current.push(json);
      if (undoStack.current.length > 50) {
        undoStack.current.shift();
      }
      redoStack.current = [];
    };

    // Load canvas state (undo or redo)
    const loadState = (state) => {
      if (!fabricRef.current) return;
      fabricRef.current.loadFromJSON(state, () => {
        fabricRef.current.renderAll();
      });
    };

    useEffect(() => {
      const fabricCanvas = new fabric.Canvas(canvasRef.current, {
        isDrawingMode: true,
        selection: false,
      });

      fabricCanvas.setWidth(width);
      fabricCanvas.setHeight(height);
      fabricCanvas.setBackgroundColor(
        backgroundColor,
        fabricCanvas.renderAll.bind(fabricCanvas)
      );

      fabricCanvas.freeDrawingBrush.width = brushWidth;
      fabricCanvas.freeDrawingBrush.color = isEraser
        ? backgroundColor
        : brushColor;

      fabricRef.current = fabricCanvas;

      undoStack.current = [];
      redoStack.current = [];
      saveState();

      // When user draws a path, clear saved image (must save again)
      fabricCanvas.on("path:created", () => {
        setSavedImage(null);
        saveState();
      });

      return () => {
        fabricCanvas.dispose();
        fabricRef.current = null;
      };
    }, [width, height, backgroundColor, brushColor, brushWidth, isEraser]);

    // Update brush settings on changes
    useEffect(() => {
      if (!fabricRef.current) return;
      fabricRef.current.isDrawingMode = true;
      fabricRef.current.freeDrawingBrush.width = brushWidth;
      fabricRef.current.freeDrawingBrush.color = isEraser
        ? backgroundColor
        : brushColor;
    }, [brushColor, brushWidth, isEraser, backgroundColor]);

    // Expose methods to parent via ref
    useImperativeHandle(ref, () => ({
      clear: () => {
        if (fabricRef.current) {
          fabricRef.current.clear();
          fabricRef.current.setBackgroundColor(
            backgroundColor,
            fabricRef.current.renderAll.bind(fabricRef.current)
          );
          undoStack.current = [];
          redoStack.current = [];
          saveState();
          setSavedImage(null);
        }
      },
      saveDrawing: () => {
        if (fabricRef.current) {
          return fabricRef.current.toDataURL({
            format: "png",
            quality: 0.8,
          });
        }
        return null;
      },
      setBrushColor: (color) => {
        setBrushColor(color);
        setIsEraser(false);
      },
      setBrushWidth: (width) => {
        setBrushWidth(width);
      },
      toggleEraser: () => {
        setIsEraser((prev) => !prev);
      },
      undo: () => {
        if (undoStack.current.length > 1 && fabricRef.current) {
          const currentState = undoStack.current.pop();
          redoStack.current.push(currentState);
          const prevState = undoStack.current[undoStack.current.length - 1];
          loadState(prevState);
        }
      },
      redo: () => {
        if (redoStack.current.length > 0 && fabricRef.current) {
          const nextState = redoStack.current.pop();
          undoStack.current.push(nextState);
          loadState(nextState);
        }
      },
    }));

    // Save drawing handler
    const handleSaveDrawing = () => {
      if (!fabricRef.current) return;
      const dataUrl = fabricRef.current.toDataURL({
        format: "png",
        quality: 0.8,
      });
      setSavedImage(dataUrl);
      if (onSave) onSave(dataUrl);
    };

    // Redraw handler
    const handleRedraw = () => {
      if (!fabricRef.current) return;
      fabricRef.current.clear();
      fabricRef.current.setBackgroundColor(
        backgroundColor,
        fabricRef.current.renderAll.bind(fabricRef.current)
      );
      undoStack.current = [];
      redoStack.current = [];
      saveState();
      setSavedImage(null);
      if (onSave) onSave(null);
    };

    return (
      <div>
        <canvas
          ref={canvasRef}
          className="border border-gray-300 rounded cursor-crosshair"
          width={width}
          height={height}
          style={{ touchAction: "none" }}
        />
        <div className="flex items-center gap-4 mt-2">
          {/* Brush color picker */}
          <label>
            Brush Color:{" "}
            <input
              type="color"
              className="cursor-pointer"
              value={isEraser ? backgroundColor : brushColor}
              disabled={isEraser}
              onChange={(e) => setBrushColor(e.target.value)}
            />
          </label>

          {/* Brush size */}
          <label>
            Brush Size:{" "}
            <input
              type="range"
              min="1"
              max="50"
              value={brushWidth}
              onChange={(e) => setBrushWidth(parseInt(e.target.value, 10))}
            />
            <span className="ml-1">{brushWidth}</span>
          </label>

          {/* Eraser toggle */}
          <button
            type="button"
            onClick={() => setIsEraser((prev) => !prev)}
            className={`px-2 py-1 rounded cursor-pointer ${
              isEraser ? "bg-red-500 text-white" : "bg-gray-300"
            }`}
          >
            {isEraser ? "Eraser On" : "Eraser Off"}
          </button>

          {/* Undo */}
          <button
            type="button"
            onClick={() => {
              if (ref && ref.current) ref.current.undo();
            }}
            className="px-2 py-1 bg-yellow-400 rounded hover:bg-yellow-500 cursor-pointer"
          >
            Undo
          </button>

          {/* Redo */}
          <button
            type="button"
            onClick={() => {
              if (ref && ref.current) ref.current.redo();
            }}
            className="px-2 py-1 bg-green-400 rounded hover:bg-green-500 cursor-pointer"
          >
            Redo
          </button>
        </div>

        {/* Save / Preview Section */}
        {!savedImage ? (
          <button
            type="button"
            onClick={handleSaveDrawing}
            className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 cursor-pointer"
          >
            Save Drawing
          </button>
        ) : (
          <div className="mt-4">
            <p className="mb-2 font-semibold">Preview:</p>
            <img
              src={savedImage}
              alt="Drawing preview"
              className="border border-gray-300 rounded max-w-full max-h-48"
            />
            <button
              type="button"
              onClick={handleRedraw}
              className="mt-2 bg-yellow-400 text-black px-4 py-2 rounded cursor-pointer hover:bg-yellow-500"
            >
              Redraw
            </button>
          </div>
        )}
      </div>
    );
  }
);

export default DrawingCanvas;
DrawingCanvas.displayName = "DrawingCanvas";
