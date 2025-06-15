from .base_repository import BaseRepository
from app.models.comments import Comment

class CommentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Comment)