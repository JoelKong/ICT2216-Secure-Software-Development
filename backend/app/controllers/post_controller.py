import re
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.interfaces.services.IPostService import IPostService
from app.services.post_service import PostService
from openai import OpenAI
import os

# --- Validation constants & regexes ---
SORT_OPTIONS        = {"recent", "likes", "comments"}
INT_REGEX = r"^\d+$"  # Accepts 0 and all non-negative integers
SEARCH_MAX_LENGTH   = 100                   # max chars for search query
TITLE_MAX_LENGTH    = 100                   # max chars for post title
CONTENT_MAX_LENGTH  = 2000                  # max chars for post content
ALLOWED_IMAGE_EXTS  = {"png", "jpg", "jpeg", "gif"}
FILENAME_REGEX      = r"^[A-Za-z0-9_\-]+\.(?:png|jpg|jpeg|gif)$"


class PostController:
    def __init__(self, post_service: IPostService = None,):
        self.post_service = post_service or PostService()

    @jwt_required()
    def fetch_posts(self):
        """GET /posts?sort_by=&offset=&limit=&search=&user_id="""
        try:
            args     = request.args
            sort_by  = args.get("sort_by", "recent")
            raw_offset = args.get("offset", "0")
            raw_limit  = args.get("limit", "10")
            search   = args.get("search", None)
            raw_user_id = args.get("user_id", None)

            # Validate sort_by
            if sort_by not in SORT_OPTIONS:
                return jsonify({"error": f"sort_by must be one of {', '.join(SORT_OPTIONS)}"}), 400

            # Validate offset
            if not re.match(INT_REGEX, raw_offset):
                return jsonify({"error": "offset must be a non-negative integer"}), 400
            offset = int(raw_offset)

            # Validate limit
            if not re.match(INT_REGEX, raw_limit):
                return jsonify({"error": "limit must be a positive integer"}), 400
            limit = int(raw_limit)

            # Validate search length
            if search is not None:
                search = search.strip()
                if len(search) > SEARCH_MAX_LENGTH:
                    return jsonify({"error": f"search cannot exceed {SEARCH_MAX_LENGTH} characters"}), 400

            # Validate user_id if provided
            user_id = None
            if raw_user_id is not None:
                if not re.match(INT_REGEX, raw_user_id):
                    return jsonify({"error": "user_id must be a positive integer"}), 400
                user_id = int(raw_user_id)

            current_user_id = get_jwt_identity()
            current_app.logger.info(
                f"Fetching posts: sort_by={sort_by}, offset={offset}, limit={limit}, "
                f"search={search!r}, user_id={user_id}"
            )

            result = self.post_service.get_posts(
                sort_by=sort_by,
                offset=offset,
                limit=limit,
                search=search,
                user_id=user_id
            )

            # Fetch liked posts
            post_ids = [post["post_id"] for post in result.get("posts", [])]
            liked = self.post_service.get_user_liked_posts(current_user_id, post_ids)
            result["liked_post_ids"] = liked

            return jsonify(result), 200

        except Exception as e:
            current_app.logger.error(f"Error getting posts: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @jwt_required()
    def toggle_like(self, post_id):
        """POST /posts/<post_id>/like"""
        try:
            if not re.match(INT_REGEX, str(post_id)):
                return jsonify({"error": "Invalid post ID"}), 400
            pid = int(post_id)
            user_id = get_jwt_identity()

            result, error = self.post_service.toggle_like(pid, user_id)
            if error:
                return jsonify({"error": error}), 404

            return jsonify(result), 200

        except Exception as e:
            current_app.logger.error(f"Error toggling like: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @jwt_required()
    def delete_post(self, post_id):
        """DELETE /posts/<post_id>"""
        try:
            if not re.match(INT_REGEX, str(post_id)):
                return jsonify({"error": "Invalid post ID"}), 400
            pid = int(post_id)
            user_id = int(get_jwt_identity())

            success, message = self.post_service.delete_post(pid, user_id)
            if not success:
                return jsonify({"error": message}), 403

            return jsonify({"message": message}), 200

        except Exception as e:
            current_app.logger.error(f"Error deleting post: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @jwt_required()
    def get_post_detail(self, post_id):
        """GET /posts/<post_id>"""
        try:
            if not re.match(INT_REGEX, str(post_id)):
                return jsonify({"error": "Invalid post ID"}), 400
            pid = int(post_id)
            user_id = get_jwt_identity()

            detail = self.post_service.get_post_detail(pid, user_id)
            if not detail:
                return jsonify({"error": "Post not found"}), 404

            return jsonify(detail), 200

        except Exception as e:
            current_app.logger.error(f"Error fetching post detail: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @jwt_required()
    def create_post(self):
        """POST /posts (form-data: title, content, optional image)"""
        try:
            user_id = get_jwt_identity()
            title = (request.form.get("title") or "").strip()
            content = (request.form.get("content") or "").strip()
            image_file = request.files.get("image")

            # Validate title/content presence & lengths
            if not title or not content:
                return jsonify({"error": "Title and content are required"}), 400
            if len(title) > TITLE_MAX_LENGTH:
                return jsonify({"error": f"Title cannot exceed {TITLE_MAX_LENGTH} characters"}), 400
            if len(content) > CONTENT_MAX_LENGTH:
                return jsonify({"error": f"Content cannot exceed {CONTENT_MAX_LENGTH} characters"}), 400

            # Validate image if provided
            if image_file:
                filename = secure_filename(image_file.filename or "")
                ext = filename.rsplit(".", 1)[-1].lower()
                if ext not in ALLOWED_IMAGE_EXTS:
                    return jsonify({
                        "error": f"Invalid image type; allowed: {', '.join(ALLOWED_IMAGE_EXTS)}"
                    }), 400

            post = self.post_service.create_post(
                title=title,
                content=content,
                image_file=image_file,
                user_id=user_id
            )
            return jsonify({"message": "Post created", "post_id": post.post_id}), 201

        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            current_app.logger.error(f"Create post error: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @jwt_required()
    def get_post_for_edit(self, post_id):
        """GET /posts/<post_id>/edit"""
        try:
            if not re.match(INT_REGEX, str(post_id)):
                return jsonify({"error": "Invalid post ID"}), 400
            pid = int(post_id)
            user_id = int(get_jwt_identity())

            post = self.post_service.get_post_detail(pid, user_id)
            if not post:
                return jsonify({"error": "Post not found"}), 404

            if post["user_id"] != user_id:
                return jsonify({"error": "Unauthorized"}), 403
            
            return jsonify({
                "post_id": post["post_id"],
                "title": post["title"],
                "content": post["content"],
                "image": post["image"]
            }), 200

        except Exception as e:
            current_app.logger.error(f"Error fetching post for edit: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @jwt_required()
    def edit_post(self, post_id):
        """PUT /posts/<post_id> (form-data: title, content, optional image)"""
        try:
            if not re.match(INT_REGEX, str(post_id)):
                return jsonify({"error": "Invalid post ID"}), 400
            pid = int(post_id)
            user_id = int(get_jwt_identity())

            title = (request.form.get("title") or "").strip()
            content = (request.form.get("content") or "").strip()
            image_file = request.files.get("image")

            # Validate title/content presence & lengths
            if not title or not content:
                return jsonify({"error": "Title and content are required"}), 400
            if len(title) > TITLE_MAX_LENGTH:
                return jsonify({"error": f"Title cannot exceed {TITLE_MAX_LENGTH} characters"}), 400
            if len(content) > CONTENT_MAX_LENGTH:
                return jsonify({"error": f"Content cannot exceed {CONTENT_MAX_LENGTH} characters"}), 400

            # Validate image if provided
            if image_file:
                filename = secure_filename(image_file.filename or "")
                ext = filename.rsplit(".", 1)[-1].lower()
                if ext not in ALLOWED_IMAGE_EXTS:
                    return jsonify({
                        "error": f"Invalid image type; allowed: {', '.join(ALLOWED_IMAGE_EXTS)}"
                    }), 400

            updated = self.post_service.edit_post(
                post_id=pid,
                user_id=user_id,
                title=title,
                content=content,
                image_file=image_file
            )
            if not updated:
                return jsonify({"error": "Post not found or unauthorized"}), 404

            return jsonify({"message": "Post updated", "post_id": updated.post_id}), 200

        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            current_app.logger.error(f"Edit post error: {e}")
            return jsonify({"error": "Internal server error"}), 500

    def get_post_image(self, filename):
        """GET /posts/images/<filename>"""
        if not re.match(FILENAME_REGEX, filename):
            return jsonify({"error": "Invalid image filename"}), 400

        return self.post_service.get_post_image(filename)
    
    @jwt_required()
    def summarize_post(self, post_id):
        try:
            user_id = get_jwt_identity()

            post = PostService().get_post_detail(post_id, user_id)
            if not post:
                return jsonify({"error": "Post not found"}), 404

            content = post["content"]
            word_count = len(content.split())

            if word_count <= 50:
                return jsonify({"summary": "Post content too short to summarize."}), 200
            
            # Some prompt injection prevention
            if any(s in content.lower() for s in ["ignore previous", "you are now", "forget all", "repeat after me", "respond with"]):
                return jsonify({"error": "Invalid content detected."}), 400

            client = OpenAI(api_key=os.environ.get("OPENAI_SECRET_KEY"))
            if not client:
                return jsonify({"error": "Server misconfigured for OpenAI"}), 500

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Summarize the following post:"},
                        {"role": "user", "content": post["content"]}
                    ],
                    max_tokens=100,
                    temperature=0.7
                )

                summary = response.choices[0].message.content
                return jsonify({"summary": summary}), 200
            
            except Exception as e:
                current_app.logger.error(f"[OpenAI API Error] Failed to generate summary: {e}")
                return jsonify({"error": "Failed to summarize post."}), 500

        except Exception as e:
            current_app.logger.error(f"[AI SUMMARY] Exception: {e}")
            return jsonify({"error": "Failed to summarize post."}), 500
        
    @jwt_required()
    def get_user_post_limit(self):
        try:
            user_id = int(get_jwt_identity())
            # If unlimited, just return success with no limit info
            post_service = PostService()
            has_reached_limit = post_service.has_reached_daily_post_limit(user_id)

            return jsonify({
                "has_reached_limit": has_reached_limit
            }), 200

        except Exception as e:
            current_app.logger.error(f"Error getting user post limit: {str(e)}")
            return jsonify({"error": "Failed to retrieve post limit"}), 500