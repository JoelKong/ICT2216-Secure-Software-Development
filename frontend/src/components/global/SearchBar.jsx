import { useState } from "react";
import { Search, X } from "lucide-react";

export default function SearchBar({ setSearchTerm }) {
  const [searchValue, setSearchValue] = useState("");

  // Update parent search term on input change
  const handleChange = (e) => {
    setSearchValue(e.target.value);
  };

  // Optional: Only search on Enter
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      setSearchTerm(searchValue);
    }
  };

  return (
    <div className="flex-1 max-w-md mx-4">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          value={searchValue}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          className="block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md leading-5 bg-gray-50 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="Search discussions..."
        />
        {searchValue && (
          <button
            className="absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer"
            onClick={() => {
              setSearchValue("");
              setSearchTerm("");
            }}
          >
            <X className="h-4 w-4 text-gray-400 hover:text-gray-600" />
          </button>
        )}
      </div>
    </div>
  );
}
