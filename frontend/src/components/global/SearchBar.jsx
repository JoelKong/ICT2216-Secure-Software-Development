import { useState, useRef, useEffect } from "react";
import { Search, X } from "lucide-react";

export default function SearchBar() {
  const [searchValue, setSearchValue] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [isSearchFocused, setIsSearchFocused] = useState(false);
  const searchRef = useRef(null);

  // Mock suggestions - in a real app, these would come from your API
  const mockSuggestions = [
    "React discussion",
    "Tailwind CSS tips",
    "Flask backend setup",
    "Authentication best practices",
    "Database optimization",
    "Frontend frameworks",
    "API integration",
    "Performance tuning",
  ];

  // Filter suggestions based on input
  useEffect(() => {
    if (!searchValue.trim()) {
      setSuggestions([]);
      return;
    }

    const filteredItems = mockSuggestions.filter((item) =>
      item.toLowerCase().includes(searchValue.toLowerCase())
    );
    setSuggestions(filteredItems);
  }, [searchValue]);

  // Handle suggestion selection
  const handleSelectSuggestion = (suggestion) => {
    setSearchValue(suggestion);
    setIsSearchFocused(false);
    // Here you would typically trigger a search with the selected suggestion
    console.log("Selected:", suggestion);
  };

  // Handle key navigation
  const [activeIndex, setActiveIndex] = useState(-1);

  const handleKeyDown = (e) => {
    if (!suggestions.length) return;

    // Arrow down
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActiveIndex((prevIndex) =>
        prevIndex < suggestions.length - 1 ? prevIndex + 1 : 0
      );
    }
    // Arrow up
    else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActiveIndex((prevIndex) =>
        prevIndex > 0 ? prevIndex - 1 : suggestions.length - 1
      );
    }
    // Enter
    else if (e.key === "Enter" && activeIndex >= 0) {
      e.preventDefault();
      handleSelectSuggestion(suggestions[activeIndex]);
    }
    // Escape
    else if (e.key === "Escape") {
      setIsSearchFocused(false);
    }
  };

  return (
    <div className="flex-1 max-w-md mx-4">
      <div className="relative" ref={searchRef}>
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          onFocus={() => setIsSearchFocused(true)}
          onKeyDown={handleKeyDown}
          className="block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md leading-5 bg-gray-50 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="Search discussions..."
        />
        {searchValue && (
          <button
            className="absolute inset-y-0 right-0 pr-3 flex items-center"
            onClick={() => {
              setSearchValue("");
              setActiveIndex(-1);
            }}
          >
            <X className="h-4 w-4 text-gray-400 hover:text-gray-600" />
          </button>
        )}

        {/* Suggestions dropdown */}
        {isSearchFocused && suggestions.length > 0 && (
          <ul className="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm">
            {suggestions.map((suggestion, index) => (
              <li
                key={index}
                onClick={() => handleSelectSuggestion(suggestion)}
                className={`cursor-pointer py-2 px-3 hover:bg-blue-50 ${
                  activeIndex === index ? "bg-blue-50" : ""
                }`}
              >
                {suggestion}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
