# backend/app/controllers/profile_controller.py

import re
from flask import request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.interfaces.services.IProfileService import IProfileService
from app.services.profile_service import ProfileService
import os

# --- Validation constants & regexes ---
SORT_OPTIONS     = {"recent", "oldest", "popular"}
INT_REGEX        = r"^\d+$"
USERNAME_REGEX   = r"^[A-Za-z0-9_]{3,20}$"
BIO_MAX_LENGTH   = 200
ALLOWED_EXTS     = {"png", "jpg", "jpeg", "gif"}
FILENAME_REGEX   = r"^[A-Za-z0-9_\-]+\.(?:png|jpg|jpeg|gif)$"


class ProfileController:
    def __init__(self, profile_service: IProfileService = None):
        self.profile_service = profile_service or ProfileService()

    @jwt_required()
    def get_profile(self):
        """Handle GET request for user profile (no extra input)."""
        try:
            user_id = get_jwt_identity()
            current_app.logger.info(f"Fetching profile for user: {user_id}")

            user_data, error = self.profile_service.get_user_profile(user_id)
            if error:
                return jsonify({"error": error}), 404

            return jsonify({"user": user_data}), 200

        except Exception as e:
            current_app.logger.error(f"Error in get_profile: {e}")
            return jsonify({"error": "Failed to retrieve user profile"}), 500

    @jwt_required()
    def update_profile(self):
        """Handle PUT request to update user profile with validation."""
        try:
            user_id = get_jwt_identity()
            raw = request.get_json() or {}

            # Whitelist fields
            username = raw.get("username")
            bio      = raw.get("bio")

            if username is None and bio is None:
                return jsonify({"error": "No fields to update"}), 400

            # Validate username
            if username is not None:
                username = username.strip()
                if not re.match(USERNAME_REGEX, username):
                    return jsonify({
                        "error": "Username must be 3–20 chars: letters, digits, or underscores."
                    }), 400

            # Validate bio
            if bio is not None:
                bio = bio.strip()
                if len(bio) > BIO_MAX_LENGTH:
                    return jsonify({
                        "error": f"Bio must be ≤ {BIO_MAX_LENGTH} characters."
                    }), 400

            current_app.logger.info(f"Updating profile for user: {user_id}")
            updated, error = self.profile_service.update_profile(
                user_id,
                {"username": username, "bio": bio}
            )
            if error:
                return jsonify({"error": error}), 400

            return jsonify({
                "user": updated,
                "message": "Profile updated successfully"
            }), 200

        except Exception as e:
            current_app.logger.error(f"Error in update_profile: {e}")
            return jsonify({"error": "Failed to update profile"}), 500

    @jwt_required()
    def update_profile_picture(self):
        """Handle POST request for uploading profile picture with validation."""
        try:
            user_id = get_jwt_identity()
            file = request.files.get("profile_picture")

            if not file:
                return jsonify({"error": "No file uploaded"}), 400

            filename = secure_filename(file.filename or "")
            ext = filename.rsplit(".", 1)[-1].lower()

            # Validate extension
            if ext not in ALLOWED_EXTS:
                return jsonify({
                    "error": f"Invalid file type: must be one of {', '.join(ALLOWED_EXTS)}."
                }), 400

            current_app.logger.info(f"User {user_id} uploading profile picture: {filename}")
            # Delegate actual saving to service
            url, error = self.profile_service.update_profile_picture(user_id, file)
            if error:
                return jsonify({"error": error}), 400

            return jsonify({
                "profile_picture": url,
                "message": "Upload successful"
            }), 200

        except Exception as e:
            current_app.logger.error(f"Error in update_profile_picture: {e}")
            return jsonify({"error": "Failed to upload profile picture"}), 500

    def get_profile_image(self, filename):
        """Serve profile images, validating filename to prevent path traversal."""
        if not re.match(FILENAME_REGEX, filename):
            return jsonify({"error": "Invalid image filename"}), 400

        # Assuming your service returns the directory path and you want to serve directly:
        return self.profile_service.get_profile_image(filename)
        

    @jwt_required()
    def delete_profile(self):
        """Handle DELETE request for user profile."""
        try:
            user_id = get_jwt_identity()
            current_app.logger.info(f"Deleting profile for user: {user_id}")

            user_data, err_lookup = self.profile_service.get_user_profile(user_id)
            if err_lookup:
                return jsonify({"error": err_lookup}), 404

            success, error = self.profile_service.delete_user_profile(user_id)
            if error:
                return jsonify({"error": error}), 400

            return jsonify({
                "message": "User profile deleted successfully",
                "user_id": user_id
            }), 200

        except Exception as e:
            current_app.logger.error(f"Error in delete_profile: {e}")
            return jsonify({"error": "Failed to delete profile"}), 500

    @jwt_required()
    def get_user_posts(self):
        """Handle GET request for user's posts with query‐param validation."""
        try:
            user_id = get_jwt_identity()
            args    = request.args

            # Validate sort_by
            sort_by = args.get("sort_by", "recent")
            if sort_by not in SORT_OPTIONS:
                return jsonify({
                    "error": f"sort_by must be one of {', '.join(SORT_OPTIONS)}"
                }), 400

            # Validate limit
            raw_lim = args.get("limit", "10")
            if not re.match(INT_REGEX, raw_lim):
                return jsonify({"error": "limit must be an integer"}), 400
            limit = min(int(raw_lim), 50)

            # Validate offset
            raw_off = args.get("offset", "0")
            if not re.match(INT_REGEX, raw_off):
                return jsonify({"error": "offset must be an integer"}), 400
            offset = int(raw_off)

            current_app.logger.info(
                f"Fetching posts for user {user_id}: sort_by={sort_by}, limit={limit}, offset={offset}"
            )
            posts, error = self.profile_service.get_user_posts(
                user_id=user_id,
                sort_by=sort_by,
                limit=limit,
                offset=offset
            )
            if error:
                return jsonify({"error": error}), 400

            return jsonify({"posts": posts}), 200

        except Exception as e:
            current_app.logger.error(f"Error in get_user_posts: {e}")
            return jsonify({"error": "Failed to fetch posts"}), 500
