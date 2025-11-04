import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, StudentBody, BodyEvent, Post
from forms import BodyEventForm, BodyPostForm

studentbody_bp = Blueprint('studentbody', __name__)

# Allowed extensions helper
ALLOWED_IMG = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG


# ============================
# Public + Profile Views
# ============================

@studentbody_bp.route('/body/<int:body_id>')
def view_body(body_id):
    body = StudentBody.query.get_or_404(body_id)
    return render_template('body_profile.html', body=body)


@studentbody_bp.route("/body/<int:body_id>/home")
def body_home(body_id):
    body = StudentBody.query.get_or_404(body_id)
    return render_template("body_home.html", body=body)


@studentbody_bp.route("/body/<int:body_id>/profile")
@login_required
def body_profile(body_id):
    body = StudentBody.query.get_or_404(body_id)
    return render_template("body_profile.html", body=body)


# ============================
# Dashboard (Events + Posts)
# ============================

@studentbody_bp.route('/body/<int:body_id>/dashboard', methods=['GET', 'POST'])
@login_required
def body_dashboard(body_id):
    body = StudentBody.query.get_or_404(body_id)

    # ✅ Ensure logged-in body is the owner
    if not isinstance(current_user, StudentBody) or current_user.id != body_id:
        abort(403)

    # Event form
    form = BodyEventForm()
    if form.validate_on_submit():
        poster_path = None
        if form.poster.data and form.poster.data.filename and allowed_file(form.poster.data.filename):
            filename = secure_filename(f"body_{body.id}_event_{form.poster.data.filename}")
            upload_folder = current_app.config.get('UPLOAD_FOLDER') or os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            form.poster.data.save(filepath)
            poster_path = f"uploads/{filename}"

        event = BodyEvent(
            title=form.title.data,
            description=form.description.data,
            poster=poster_path,
            date=form.date.data,
            body_id=body.id
        )
        db.session.add(event)
        db.session.commit()
        flash("Event created", "success")
        return redirect(url_for("studentbody.body_dashboard", body_id=body.id))

    # Post form (handled by separate route)
    post_form = BodyPostForm()

    events = BodyEvent.query.filter_by(body_id=body.id).order_by(BodyEvent.date.desc()).all()
    posts = Post.query.filter_by(body_id=body.id).order_by(Post.created_at.desc()).all()

    return render_template("body_dashboard.html", body=body, events=events, posts=posts, form=form, post_form=post_form)


# ============================
# Create Post
# ============================

@studentbody_bp.route('/body/<int:body_id>/post/create', methods=['POST'])
@login_required
def create_post(body_id):
    body = StudentBody.query.get_or_404(body_id)

    if not isinstance(current_user, StudentBody) or current_user.id != body_id:
        abort(403)

    post_form = BodyPostForm()
    if post_form.validate_on_submit():
        image_url = None
        if post_form.image.data and post_form.image.data.filename and allowed_file(post_form.image.data.filename):
            filename = secure_filename(f"body_{body.id}_post_{post_form.image.data.filename}")
            upload_folder = current_app.config.get('UPLOAD_FOLDER') or os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            post_form.image.data.save(filepath)
            image_url = f"uploads/{filename}"

        post = Post(
            body_id=body.id,
            title=post_form.title.data,
            content=post_form.content.data,
            image_url=image_url
        )
        db.session.add(post)
        db.session.commit()
        flash("Post published successfully!", "success")
    else:
        flash("Error creating post. Please check your input.", "danger")

    return redirect(url_for("studentbody.body_dashboard", body_id=body.id))


# ============================
# Event Management
# ============================

@studentbody_bp.route('/body/<int:body_id>/event/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(body_id, event_id):
    body = StudentBody.query.get_or_404(body_id)
    event = BodyEvent.query.get_or_404(event_id)

    if getattr(current_user, "email", None) != body.email:
        abort(403)

    if request.method == 'POST':
        event.title = request.form.get('title', event.title)
        event.description = request.form.get('description', event.description)
        poster_file = request.files.get('poster')
        if poster_file and poster_file.filename and allowed_file(poster_file.filename):
            # delete old poster if exists
            if event.poster:
                old_path = os.path.join(current_app.root_path, 'static', event.poster)
                if os.path.exists(old_path):
                    os.remove(old_path)
            filename = secure_filename(f"body_{body.id}_event_{event.id}_{poster_file.filename}")
            upload_folder = current_app.config.get('UPLOAD_FOLDER') or os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            poster_file.save(filepath)
            event.poster = f"uploads/{filename}"

        db.session.commit()
        flash('Event updated', 'success')
        return redirect(url_for('studentbody.body_dashboard', body_id=body.id))

    return render_template('edit_body_event.html', body=body, event=event)


@studentbody_bp.route('/body/<int:body_id>/event/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(body_id, event_id):
    body = StudentBody.query.get_or_404(body_id)
    event = BodyEvent.query.get_or_404(event_id)

    if getattr(current_user, "email", None) != body.email:
        abort(403)

    if event.poster:
        path = os.path.join(current_app.root_path, 'static', event.poster)
        if os.path.exists(path):
            os.remove(path)

    db.session.delete(event)
    db.session.commit()
    flash('Event deleted', 'info')
    return redirect(url_for('studentbody.body_dashboard', body_id=body.id))
