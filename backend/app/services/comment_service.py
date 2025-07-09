from app.interfaces.services.ICommentService import ICommentService
from app.interfaces.repositories.ICommentRepository import ICommentRepository
from app.repositories.comment_repository import CommentRepository
from app.models.comments import Comment
from typing import List, Optional, Dict, Any
from flask import current_app, send_from_directory
import os
import time
import magic

ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

class CommentService(ICommentService):
    def __init__(self, comment_repository: ICommentRepository = None):
        self.comment_repository = comment_repository or CommentRepository()
        self.UPLOAD_FOLDER = '/data/comment_uploads'

    def _is_valid_mime(self, file) -> bool:
        file.seek(0)
        mime = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)
        return mime in ALLOWED_MIME_TYPES

    def _is_valid_size(self, file) -> bool:
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        return size <= MAX_FILE_SIZE

    def get_comments_by_post(self, post_id: int) -> List[Dict[str, Any]]:
        try:
            comments = self.comment_repository.get_by_post_id(post_id)
            # Format comments (handle nested, lazy loading etc. outside this method)
            result = []
            for c in comments:
                result.append({
                    "comment_id": c.comment_id,
                    "post_id": c.post_id,
                    "parent_id": c.parent_id,
                    "user_id": c.user_id,
                    "username": c.username,
                    "content": c.content,
                    "image": c.image,
                    "created_at": c.created_at.isoformat()
                })
            return result
        except Exception as e:
            current_app.logger.error(f"Error getting comments for post {post_id}: {str(e)}")
            raise

    def create_comment(self, post_id: int, user_id: int, content: str, parent_id: Optional[int] = None, image_file=None) -> Comment:
        try:
            image_url = None
            if image_file and image_file.filename:

                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
                if '.' not in image_file.filename or image_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                    raise ValueError("File type not allowed")
                
                if not self._is_valid_mime(image_file):
                    raise ValueError("Invalid file content")
        
                if not self._is_valid_size(image_file):
                    raise ValueError("File too large")
                
                # Save image file
                filename = f"user_{user_id}_comment_{int(time.time())}.{image_file.filename.rsplit('.', 1)[1].lower()}"
                filepath = os.path.join(self.UPLOAD_FOLDER, filename)
                os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
                image_file.save(filepath)
                image_url = f"/comment_uploads/{filename}"

                current_app.logger.info(f"Saved comment image to {filepath}")

            comment = Comment(
                post_id=post_id,
                user_id=user_id,
                content=content,
                parent_id=parent_id,
                image=image_url
            )
            return self.comment_repository.create_comment(comment)
        except Exception as e:
            current_app.logger.error(f"Error creating comment: {str(e)}")
            raise

    def get_comment_image(self, filename):
        """Serve comment image from comment_uploads folder"""
        try:
            # Security check - prevent directory traversal
            if '..' in filename or filename.startswith('/'):
                raise ValueError("Invalid filename")
                
            return send_from_directory(self.UPLOAD_FOLDER, filename)
        except Exception as e:
            current_app.logger.error(f"Error serving file {filename}: {str(e)}")
            raise 