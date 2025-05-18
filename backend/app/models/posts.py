from app.db import db

class Post(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True)

# dk why gpt gave this
    # comments = db.relationship('Comment', backref='post', cascade="all, delete", lazy=True)
