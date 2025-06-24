import { useState, useEffect } from "react";

// Edit Modal
export function EditProfileFieldModal({
  fieldLabel,
  fieldValue,
  isDate,
  onSave,
  onCancel,
  onChange,
  isPassword = false,
}) {
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordValid, setPasswordValid] = useState({
    length: false,
    uppercase: false,
    lowercase: false,
    number: false,
    specialChar: false,
  });

  useEffect(() => {
    if (isPassword) {
      const password = fieldValue;
      setPasswordValid({
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /\d/.test(password),
        specialChar: /[!@#$%^&*(),.?":{}|<>]/.test(password),
      });
    }
  }, [fieldValue, isPassword]);

  const canSave =
    !isPassword ||
    (Object.values(passwordValid).every(Boolean) && fieldValue === confirmPassword);

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 bg-white/20 backdrop-blur">
      <div className="bg-white rounded-lg shadow-lg p-6 w-96 max-w-full">
        <h2 className="text-xl font-bold mb-4">Edit {fieldLabel}</h2>

        <input
          type={isDate ? "date" : isPassword ? "password" : "text"}
          className="w-full border border-gray-300 rounded p-2 mb-4"
          value={fieldValue}
          onChange={(e) => onChange(e.target.value)}
          autoFocus
          placeholder={isPassword ? "New Password" : undefined}
        />

        {isPassword && (
          <>
            <input
              type="password"
              className="w-full border border-gray-300 rounded p-2 mb-2"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm New Password"
            />
            <ul className="text-sm mb-4">
              <li className={passwordValid.length ? "text-green-600" : "text-red-600"}>
                Minimum 8 characters
              </li>
              <li className={passwordValid.uppercase ? "text-green-600" : "text-red-600"}>
                At least one uppercase letter
              </li>
              <li className={passwordValid.lowercase ? "text-green-600" : "text-red-600"}>
                At least one lowercase letter
              </li>
              <li className={passwordValid.number ? "text-green-600" : "text-red-600"}>
                At least one number
              </li>
              <li className={passwordValid.specialChar ? "text-green-600" : "text-red-600"}>
                At least one special character
              </li>
              <li
                className={
                  fieldValue === confirmPassword && fieldValue.length > 0
                    ? "text-green-600"
                    : "text-red-600"
                }
              >
                Passwords must match
              </li>
            </ul>
          </>
        )}

        <div className="flex justify-end space-x-4">
          <button
            onClick={onCancel}
            className="px-4 py-2 rounded border border-gray-300 hover:bg-gray-100"
          >
            Cancel
          </button>
          <button
            onClick={onSave}
            disabled={!canSave}
            className={`px-4 py-2 rounded text-white ${
              canSave ? "bg-blue-500 hover:bg-blue-600" : "bg-blue-300 cursor-not-allowed"
            }`}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
}

// Delete Modal
export function DeleteAccountModal({ onConfirm, onCancel }) {
  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 bg-white/20 backdrop-blur">
      <div className="bg-white p-6 rounded shadow-md max-w-sm w-full">
        <h2 className="text-lg font-bold mb-4">Confirm Deletion</h2>
        <p className="mb-4">
          Are you sure you want to delete your account? This action cannot be undone.
        </p>
        <div className="flex justify-end space-x-4">
          <button
            onClick={onCancel}
            className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
