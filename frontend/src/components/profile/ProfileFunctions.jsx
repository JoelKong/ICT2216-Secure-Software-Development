import { useContext, useEffect, useRef, useState } from "react";
import { GlobalContext } from "../../utils/globalContext";
import fetchWithAuth from "../../utils/fetchWithAuth";
import { API_ENDPOINT, FETCH_USER_ROUTE } from "../../const";
import checkRateLimit from "../../utils/checkRateLimit";
import handleRateLimitResponse from "../../utils/handleRateLimitResponse";

export default function useProfile() {
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

  return {
    profile,
    editingField,
    editValue,
    showDeleteConfirm,
    fileInputRef,
    activeTab,
    isLoading,
    setEditValue,
    setActiveTab,
    setShowDeleteConfirm,
    handleEditClick,
    handleSave,
    handleCancel,
    handleDeleteAccount,
    handleProfilePicClick,
    handleProfilePicChange,
    auth
  };
}