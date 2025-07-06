from app.db import db
from sqlalchemy.dialects.mysql import ENUM

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    membership = db.Column(ENUM('basic', 'premium'), default='basic')
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    totp_secret = db.Column(db.String(255), nullable=True)
    email_verified = db.Column(db.Boolean, default=False)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    likes = db.relationship('Like', backref='user', lazy=True, cascade="all, delete")
    comments = db.relationship('Comment', backref='author', lazy=True, cascade="all, delete")