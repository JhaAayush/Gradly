from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models import db, StudentBody, Post, PostComment, PostVote, BodyEvent

posts_bp = Blueprint("posts", __name__, url_prefix="/posts")


# ---------- Create Post (Student Bodies only) ----------
@posts_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        image = request.files.get("image")

        image_url = None
        if image:
            filename = secure_filename(image.filename)
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            image.save(path)
            image_url = f"uploads/{filename}"

        post_data = {
            "title": title,
            "content": content,
            "image_url": image_url,
        }
        if current_user.user_type == "student":
            post_data["user_id"] = current_user.id
        else:
            post_data["body_id"] = current_user.id

        new_post = Post(**post_data)
        db.session.add(new_post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for("posts.feed"))

    return render_template("create_post.html")


# ---------- Feed ----------
@posts_bp.route("/feed")
@login_required
def feed():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    events = BodyEvent.query.order_by(BodyEvent.date.desc()).limit(6).all()
    user_votes_q = PostVote.query.filter_by(user_id=current_user.id).all()
    user_votes = {pv.post_id: pv.vote for pv in user_votes_q}
    return render_template("feed.html", posts=posts, events=events, user_votes=user_votes)


# ---------- Vote ----------
@posts_bp.route("/vote/<int:post_id>/<action>", methods=["POST"])
@login_required
def vote(post_id, action):
    if action not in ("upvote", "downvote"):
        return jsonify({"success": False, "error": "Invalid action"}), 400

    post = Post.query.get_or_404(post_id)
    value = 1 if action == "upvote" else -1
    existing_vote = PostVote.query.filter_by(post_id=post.id, user_id=current_user.id).first()

    if existing_vote:
        if existing_vote.vote == value:
            db.session.delete(existing_vote)
        else:
            existing_vote.vote = value
    else:
        db.session.add(PostVote(post_id=post.id, user_id=current_user.id, vote=value))

    db.session.commit()
    score = sum(v.vote for v in post.votes)

    return jsonify({"success": True, "score": score})


# ---------- Comment ----------
@posts_bp.route("/comment/<int:post_id>", methods=["POST"])
@login_required
def comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get("comment")
    if content:
        new_comment = PostComment(post_id=post.id, user_id=current_user.id, content=content)
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for("posts.feed"))
