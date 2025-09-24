from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime  # <-- ADDED IMPORT
from models import db, StudentBody, StudentBodyPost, PostComment, PostVote, BodyEvent  # <-- ADDED BodyEvent

posts_bp = Blueprint("posts", __name__, url_prefix="/posts")


# ---------- Create Post (Student Bodies only) ----------
@posts_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    # You’ll probably want to enforce: only student body users can post
    if not hasattr(current_user, "is_student_body") or not current_user.is_student_body:
        flash("Only student bodies can post.", "error")
        return redirect(url_for("posts.feed"))

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        image = request.files.get("image")

        image_url = None
        if image:
            filename = secure_filename(image.filename)
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            image.save(path)
            # Make sure the path for url_for is correct
            image_url = f"uploads/{filename}"

        new_post = StudentBodyPost(
            body_id=current_user.id,  # Assumes the logged-in student body has an 'id'
            title=title,
            content=content,
            image_url=image_url,
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for("posts.feed"))

    return render_template("create_post.html")


# ---------- Feed ----------
from flask import Blueprint, render_template
from flask_login import login_required
from models import StudentBodyPost, BodyEvent


@posts_bp.route("/posts/feed")
@login_required
def feed():
    """Renders the main feed page with posts, events, and user's vote status."""
    posts = StudentBodyPost.query.order_by(StudentBodyPost.created_at.desc()).all()
    events = BodyEvent.query.order_by(BodyEvent.date.desc()).limit(6).all()

    # Create a dictionary mapping post_id to the user's vote (1 for up, -1 for down)
    user_votes_q = PostVote.query.filter_by(user_id=current_user.id).all()
    user_votes = {pv.post_id: pv.vote for pv in user_votes_q}

    return render_template("feed.html", posts=posts, events=events, user_votes=user_votes)

#
# Corrected 'vote' function
#
@posts_bp.route("/vote/<int:post_id>/<action>", methods=["POST"])
@login_required
def vote(post_id, action):
    """Handles voting logic for a post."""
    if action not in ("upvote", "downvote"):
        return jsonify({"success": False, "error": "Invalid action"}), 400

    post = StudentBodyPost.query.get_or_404(post_id)
    existing_vote = PostVote.query.filter_by(post_id=post.id, user_id=current_user.id).first()
    
    value = 1 if action == "upvote" else -1

    if existing_vote:
        # If the user clicks the same button again, remove their vote
        if existing_vote.vote == value:
            db.session.delete(existing_vote)
        # If they click the other button, change their vote
        else:
            existing_vote.vote = value
    # If no vote exists, create a new one
    else:
        new_vote = PostVote(post_id=post.id, user_id=current_user.id, vote=value)
        db.session.add(new_vote)

    db.session.commit()

    # Recalculate the post's total score
    score = sum(v.vote for v in post.votes)

    # Determine the user's current vote status to send back to the frontend
    final_user_vote = PostVote.query.filter_by(post_id=post.id, user_id=current_user.id).first()
    if final_user_vote:
        vote_status = "up" if final_user_vote.vote == 1 else "down"
    else:
        vote_status = "none" # User has no vote on this post

    return jsonify({
        "success": True, 
        "score": int(score), 
        "vote_status": vote_status
    })



# ---------- Comment ----------
@posts_bp.route("/comment/<int:post_id>", methods=["POST"])
@login_required
def comment(post_id):
    post = StudentBodyPost.query.get_or_404(post_id)
    content = request.form.get("comment")
    if content:
        new_comment = PostComment(post_id=post.id, user_id=current_user.id, content=content)
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for("posts.feed"))