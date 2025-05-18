from flask import Blueprint, request, jsonify
from app.models.posts import Post
from app.models.users import User
from app.models.likes import Like
from app.models.comments import Comment
from app.db import db

posts_bp = Blueprint('posts', __name__)

# TODO: SECURE THIS CHECK ACCESS TOKEN VALID
@posts_bp.route('/posts', methods=['GET'])
def fetch_posts():
    sort_by = request.args.get('sort_by', 'recent')
    limit = min(int(request.args.get('limit', 10)), 50)
    offset = int(request.args.get('offset', 0))
    search = request.args.get('search', '').strip()
    user_id = request.args.get('user_id', '').strip() # if want to view specific profile posts

    # Simulate getting user_id from token
    current_user_id = 1

    # Define sort criteria based on sort_by parameter
    sort_map = {
        'recent': Post.updated_at.desc(),
        'likes': db.func.count(Like.post_id).desc(),
        'comments': db.func.count(Comment.comment_id).desc()
    }
    sort_criteria = sort_map.get(sort_by, Post.updated_at.desc())

    posts_query = db.session.query(
        Post,
        User,
        db.func.count(db.distinct(Comment.comment_id)).label("comment_count"),
        db.func.count(db.distinct(Like.like_id)).label("like_count")
    )\
    .join(User, Post.user_id == User.user_id)\
    .outerjoin(Comment, Post.post_id == Comment.post_id)\
    .outerjoin(Like, Post.post_id == Like.post_id)\
    .group_by(Post.post_id, User.user_id)

    if search:
        posts_query = posts_query.filter(Post.title.ilike(f'%{search}%'))
    if user_id:
        posts_query = posts_query.filter(Post.user_id == user_id)

    posts_query = posts_query.order_by(sort_criteria, Post.post_id.desc())\
        .offset(offset)\
        .limit(limit)
    
    posts = posts_query.all()
    post_ids = [post.post_id for post, _, _, _ in posts]

    # Query likes for current user for these posts
    liked_post_ids = set()
    if post_ids:
        liked = Like.query.filter(
            Like.user_id == current_user_id,
            Like.post_id.in_(post_ids)
        ).all()
        liked_post_ids = set(like.post_id for like in liked)

    result = []
    for post, user, comment_count, like_count in posts:
        result.append({
            "post_id": post.post_id,
            "title": post.title,
            "content": post.content,
            "image": post.image,
            "username": user.username,
            "likes": like_count,
            "comments": comment_count,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat() if post.updated_at else None,
        })

    return jsonify({
        "posts": result,
        "liked_post_ids": list(liked_post_ids)
    })

@posts_bp.route('/posts/like/<int:post_id>', methods=['POST'])
def toggle_like(post_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    # TODO: Validate token and get user_id from token
    # user_id = get_user_id_from_token(token)
    user_id = 1  # Placeholder for demonstration

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    existing_like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()
    if existing_like:
        db.session.delete(existing_like)
        liked = False
    else:
        new_like = Like(post_id=post_id, user_id=user_id)
        db.session.add(new_like)
        liked = True

    db.session.commit()

    # Count likes using relationship
    likes_count = Like.query.filter_by(post_id=post_id).count()

    return jsonify({"likes": likes_count})
