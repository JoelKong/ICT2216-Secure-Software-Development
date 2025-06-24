import SimplifiedPost from "../../components/home/SimplifiedPost";
import {
  EditProfileFieldModal,
  DeleteAccountModal,
} from "../../components/profile/ProfileModalForm";
import useProfile from "../../components/profile/ProfileFunctions";

export default function Profile({ scrollContainerRef, searchTerm }) {
  const {
    profile,
    editingField,
    editValue,
    showDeleteConfirm,
    fileInputRef,
    activeTab,
    isLoading,
    auth,
    setEditValue,
    setActiveTab,
    setShowDeleteConfirm,
    handleEditClick,
    handleSave,
    handleCancel,
    handleDeleteAccount,
    handleProfilePicClick,
    handleProfilePicChange,
    profilePictureUrl
  } = useProfile();

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
                  <div className="relative">
                    <div 
                      className="cursor-pointer w-24 h-24 md:w-32 md:h-32 rounded-full overflow-hidden"
                      onClick={handleProfilePicClick}
                    >
                      {profilePictureUrl ? (
                        <img
                          src={profilePictureUrl}
                          alt="Profile"
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            e.target.onerror = null;
                            e.target.parentElement.innerHTML = `
                              <div class="w-full h-full rounded-full bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center shadow-inner">
                                <span class="text-3xl font-medium text-gray-600">
                                  ${profile?.username?.charAt(0).toUpperCase() || 'U'}
                                </span>
                              </div>
                            `;
                          }}
                        />
                      ) : (
                        <div className="w-full h-full rounded-full bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center shadow-inner">
                          <span className="text-3xl font-medium text-gray-600">
                            {profile?.username?.charAt(0).toUpperCase() || 'U'}
                          </span>
                        </div>
                      )}
                    </div>
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
                        {["Username", "Email", "Password", "Membership", "Joined since"].map((label) => (
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
