from app.db import db

class Like(db.Model):
    __tablename__ = 'likes'

    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id', ondelete='CASCADE'), primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())