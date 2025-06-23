import SimplifiedPost from "../../components/home/SimplifiedPost";
import { useContext, useEffect, useRef, useState } from "react";
import { GlobalContext } from "../../utils/globalContext";
import {
  EditProfileFieldModal,
  DeleteAccountModal,
} from "../../components/profile/ProfileModalForm";
import fetchWithAuth from "../../utils/fetchWithAuth";
import { API_ENDPOINT, FETCH_USER_ROUTE } from "../../const";
import checkRateLimit from "../../utils/checkRateLimit";
import handleRateLimitResponse from "../../utils/handleRateLimitResponse";

export default function Profile({ scrollContainerRef, searchTerm }) {
  const {
    auth,
    getAuthToken,
    updateAuthToken,
    handleLogout,
    setModal,
    rateLimit,
    setRateLimit,
  } = useContext(GlobalContext);
  const [profile, setProfile] = useState(null);
  const [editingField, setEditingField] = useState(null);
  const [editValue, setEditValue] = useState("");
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const fileInputRef = useRef(null);
  const [activeTab, setActiveTab] = useState("profile");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      if (!auth.isAuthenticated) return;
      
      setIsLoading(true);
      try {
        const res = await fetchWithAuth(
          `${API_ENDPOINT}/${FETCH_USER_ROUTE}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          },
          getAuthToken,
          updateAuthToken,
          handleLogout
        );

        if (!res.ok) {
          if (res.status === 401) {
            handleLogout();
            return;
          }
          const errorData = await res
            .json()
            .catch(() => ({ error: "Failed to fetch profile" }));
          throw new Error(errorData.error || `HTTP error! status: ${res.status}`);
        }

        const data = await res.json();
        setProfile(data.user);
      } catch (error) {
        console.error("Error fetching profile:", error);
        setModal({
          active: true,
          type: "fail",
          message: error.message || "Failed to fetch profile",
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfile();
  }, [auth.isAuthenticated]);

  const handleEditClick = (label, value) => {
    setEditValue(label === "Password" ? "" : value);
    setEditingField(label);
  };

  const handleSave = async () => {
    const labelToKey = {
      Username: "username",
      Email: "email",
      Password: "password",
    };
    const key = labelToKey[editingField];
    const updatedField = { [key]: editValue };

    try {
      if (checkRateLimit(rateLimit, setRateLimit, setModal)) {
        return;
      }

      const res = await fetchWithAuth(
        `${API_ENDPOINT}/${FETCH_USER_ROUTE}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(updatedField),
        },
        getAuthToken,
        updateAuthToken,
        handleLogout
      );

      if (handleRateLimitResponse(res, setRateLimit, setModal, "update profile")) {
        return;
      }

      if (!res.ok) {
        const errorData = await res
          .json()
          .catch(() => ({ error: "Failed to update profile" }));
        throw new Error(errorData.error || `HTTP error! status: ${res.status}`);
      }

      setProfile((prev) => ({
        ...prev,
        ...(key === "password" ? {} : { [key]: editValue }),
      }));
      setEditingField(null);
      setRateLimit({
        attempts: 0,
        cooldown: false,
      });
      setModal({
        active: true,
        type: "success",
        message: "Profile updated successfully",
      });
    } catch (error) {
      console.error("Error updating profile:", error);
      setModal({
        active: true,
        type: "fail",
        message: error.message || "Failed to update profile",
      });
    }
  };

  const handleCancel = () => setEditingField(null);

  const handleDeleteAccount = async () => {
    try {
      if (checkRateLimit(rateLimit, setRateLimit, setModal)) {
        return;
      }

      const res = await fetchWithAuth(
        `${API_ENDPOINT}/${FETCH_USER_ROUTE}`,
        {
          method: "DELETE",
        },
        getAuthToken,
        updateAuthToken,
        handleLogout
      );

      if (handleRateLimitResponse(res, setRateLimit, setModal, "delete account")) {
        return;
      }

      if (!res.ok) {
        const errorData = await res
          .json()
          .catch(() => ({ error: "Failed to delete account" }));
        throw new Error(errorData.error || `HTTP error! status: ${res.status}`);
      }

      setRateLimit({
        attempts: 0,
        cooldown: false,
      });
      handleLogout();
      window.location.href = "/";
    } catch (error) {
      console.error("Error deleting account:", error);
      setModal({
        active: true,
        type: "fail",
        message: error.message || "Failed to delete account",
      });
    }
  };

  const handleProfilePicClick = () => {
    fileInputRef.current.click();
  };

  const handleProfilePicChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("profile_picture", file);

    try {
      if (checkRateLimit(rateLimit, setRateLimit, setModal)) {
        return;
      }

      const res = await fetchWithAuth(
        `${API_ENDPOINT}/${FETCH_USER_ROUTE}/picture`,
        {
          method: "POST",
          body: formData,
        },
        getAuthToken,
        updateAuthToken,
        handleLogout
      );

      if (handleRateLimitResponse(res, setRateLimit, setModal, "update profile picture")) {
        return;
      }

      if (!res.ok) {
        const errorData = await res
          .json()
          .catch(() => ({ error: "Failed to upload profile picture" }));
        throw new Error(errorData.error || `HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      setProfile((prev) => ({
        ...prev,
        profile_picture: data.profile_picture,
      }));
      setRateLimit({
        attempts: 0,
        cooldown: false,
      });
      setModal({
        active: true,
        type: "success",
        message: "Profile picture updated successfully",
      });
    } catch (err) {
      console.error("Upload error:", err);
      setModal({
        active: true,
        type: "fail",
        message: err.message || "Failed to upload profile picture",
      });
    }
  };

  if (!auth.isAuthenticated) {
    return (
      <div className="mt-40 text-center text-xl">
        Please log in to view your profile
      </div>
    );
  }

  if (isLoading) {
    return <div className="mt-40 text-center text-xl">Loading profile...</div>;
  }

  return (
    <div className="mt-40 px-4 md:px-10">
      <div className="flex flex-col md:flex-row space-y-6 md:space-y-0 md:space-x-8 items-start min-h-screen">
        {/* Sidebar Tabs */}
        <div className="w-full md:w-48 flex md:flex-col space-x-4 md:space-x-0 md:space-y-2 border-b md:border-b-0 md:border-r pb-2 md:pb-0 md:pr-4">
          <button
            className={`py-2 px-4 text-left font-medium rounded ${
              activeTab === "profile"
                ? "bg-blue-100 text-blue-600 font-semibold"
                : "text-gray-600 hover:bg-gray-100"
            }`}
            onClick={() => setActiveTab("profile")}
          >
            Profile
          </button>
          <button
            className={`py-2 px-4 text-left font-medium rounded ${
              activeTab === "posts"
                ? "bg-blue-100 text-blue-600 font-semibold"
                : "text-gray-600 hover:bg-gray-100"
            }`}
            onClick={() => setActiveTab("posts")}
          >
            Posts
          </button>
        </div>

        {/* Content Panel */}
        <div className="flex-1 w-full">
          {activeTab === "profile" ? (
            profile ? (
              <div className="bg-white rounded-lg shadow-md p-6 w-full overflow-auto">
                <div className="flex flex-col md:flex-row items-center md:items-start space-y-6 md:space-y-0 md:space-x-10">
                  <div
                    className="relative cursor-pointer"
                    onClick={handleProfilePicClick}
                  >
                    <img
                      src={profile.profile_picture || "/default-profile.png"}
                      alt="Profile"
                      className="w-24 h-24 md:w-32 md:h-32 rounded-full object-cover"
                    />
                    <input
                      type="file"
                      accept="image/*"
                      ref={fileInputRef}
                      className="hidden"
                      onChange={handleProfilePicChange}
                    />
                  </div>

                  <div className="w-full">
                    <h1 className="text-2xl font-bold mb-4">General</h1>
                    <div className="grid grid-cols-3 gap-4 w-full">
                      <div className="space-y-4 text-left">
                        {["Username", "Email", "Password", "Membership", "Post limit", "Joined since"].map((label) => (
                          <div key={label} className="font-semibold">
                            {label}
                          </div>
                        ))}
                      </div>
                      <div className="space-y-4 text-gray-700 flex flex-col items-center">
                        {[
                          profile.username,
                          profile.email,
                          "••••••••",
                          profile.membership,
                          profile.post_limit,
                          new Date(profile.created_at).toLocaleDateString(),
                        ].map((value, idx) => (
                          <div key={idx} className="w-full text-center">
                            {value}
                          </div>
                        ))}
                      </div>
                      <div className="space-y-4 text-right flex flex-col items-end pr-5">
                        {["Username", "Email", "Password", "", "", ""].map((label, idx) =>
                          ["Username", "Email", "Password"].includes(label) ? (
                            <button
                              key={label}
                              className="text-gray-500 hover:text-gray-700"
                              onClick={() => handleEditClick(label, profile[label.toLowerCase()])}
                              title={`Edit ${label}`}
                            >
                              ➤
                            </button>
                          ) : (
                            // empty div to maintain vertical spacing alignment
                            <div key={idx} className="h-[1.5rem]"></div>
                          )
                        )}
                      </div>
                    </div>

                    <div className="mt-10">
                      <h1 className="text-2xl font-bold mb-4">Advanced</h1>
                      <div className="grid grid-cols-2 gap-4 w-full items-center">
                        <div className="font-semibold">Delete Account</div>
                        <div className="text-right">
                          <button
                            className="text-gray-500 hover:text-gray-700 pr-5"
                            onClick={() => setShowDeleteConfirm(true)}
                            title="Delete Account"
                          >
                            ➤
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {editingField && (
                  <EditProfileFieldModal
                    fieldLabel={editingField}
                    fieldValue={editValue}
                    isDate={false}
                    onChange={setEditValue}
                    onSave={handleSave}
                    onCancel={handleCancel}
                    isPassword={editingField === "Password"}
                  />
                )}

                {showDeleteConfirm && (
                  <DeleteAccountModal
                    onConfirm={handleDeleteAccount}
                    onCancel={() => setShowDeleteConfirm(false)}
                  />
                )}
              </div>
            ) : (
              <p>Loading profile...</p>
            )
          ) : (
            <div className="p-1">
              <SimplifiedPost
                scrollContainerRef={scrollContainerRef}
                searchTerm={searchTerm}
                userId={auth.user.user_id}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
