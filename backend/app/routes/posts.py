from flask import Blueprint, request, jsonify
from app.models.posts import Post
from app.models.users import User
from app.db import db

posts_bp = Blueprint('posts', __name__)

# TODO: SECURE THIS CHECK ACCESS TOKEN VALID
@posts_bp.route('/posts', methods=['GET'])
def fetch_posts():
    sort_by = request.args.get('sort_by', 'recent')
    limit = min(int(request.args.get('limit', 10)), 50)
    offset = int(request.args.get('offset', 0))
    search = request.args.get('search', '').strip()
    user_id = request.args.get('user_id', '').strip()

    # Define sort criteria based on sort_by parameter
    sort_map = {
        'recent': Post.updated_at.desc(),
        'likes': Post.likes.desc(),
        'comments': Post.comments.desc()
    }
    sort_criteria = sort_map.get(sort_by, Post.updated_at.desc())

    # Build query with optional filters
    posts_query = db.session.query(Post, User)\
        .join(User, Post.user_id == User.user_id)

    if search:
        posts_query = posts_query.filter(Post.title.ilike(f'%{search}%'))
    if user_id:
        posts_query = posts_query.filter(Post.user_id == user_id)

    posts_query = posts_query.order_by(sort_criteria, Post.post_id.desc())\
        .offset(offset)\
        .limit(limit)
    
    posts = posts_query.all()

    result = []
    for post, user in posts:
        result.append({
            "post_id": post.post_id,
            "title": post.title,
            "content": post.content,
            "image": post.image,
            "username": user.username,
            "likes": post.likes,
            "comments": post.comments,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat() if post.updated_at else None,
        })

    return jsonify(result)

# @posts_bp.route('/posts/like/<int:post_id>', methods=['POST'])
# def toggle_like(post_id):
#     token = request.headers.get("Authorization", "").replace("Bearer ", "")
#     # TODO: Validate token and get user_id
#     # user_id = get_user_id_from_token(token)
#     user_id = 1  # Placeholder for demonstration

#     post = Post.query.get(post_id)
#     if not post:
#         return jsonify({"error": "Post not found"}), 404

#     # Example: Assume a PostLike table exists to track user likes
#     from app.models.post_likes import PostLike

#     like = PostLike.query.filter_by(post_id=post_id, user_id=user_id).first()
#     if like:
#         db.session.delete(like)
#         post.likes = post.likes - 1 if post.likes > 0 else 0
#         liked = False
#     else:
#         new_like = PostLike(post_id=post_id, user_id=user_id)
#         db.session.add(new_like)
#         post.likes = post.likes + 1
#         liked = True

#     db.session.commit()
#     return jsonify({"liked": liked, "likes": post.likes})