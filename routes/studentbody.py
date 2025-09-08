# routes/studentbody.py
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, StudentBody, BodyEvent

studentbody_bp = Blueprint('studentbody', __name__)

# Allowed extensions helper
ALLOWED_IMG = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG

# View public profile
@studentbody_bp.route('/body/<int:body_id>')
def view_body(body_id):
    body = StudentBody.query.get_or_404(body_id)
    # body.events will be available via relationship
    return render_template('body_profile.html', body=body)

 
@studentbody_bp.route("/body/<int:body_id>/home")
def body_home(body_id):
    body = StudentBody.query.get_or_404(body_id)
    return render_template("body_home.html", body=body)


from forms import BodyEventForm

@studentbody_bp.route("/body/<int:body_id>/profile")
@login_required
def body_profile(body_id):
    body = StudentBody.query.get_or_404(body_id)
    return render_template("body_profile.html", body=body)


@studentbody_bp.route('/body/<int:body_id>/dashboard', methods=['GET', 'POST'])
@login_required
def body_dashboard(body_id):
    body = StudentBody.query.get_or_404(body_id)
    if not isinstance(current_user, StudentBody) or current_user.id != body_id:
        abort(403)

    form = BodyEventForm()
    if form.validate_on_submit():
        poster_path = None
        if form.poster.data and form.poster.data.filename and allowed_file(form.poster.data.filename):
            filename = secure_filename(f"body_{body.id}_event_{form.poster.data.filename}")
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            form.poster.data.save(filepath)
            poster_path = f"uploads/{filename}"

        event = BodyEvent(
            title=form.title.data,
            description=form.description.data,
            poster=poster_path,
            date=form.date.data,   # ✅ save date
            body_id=body.id
        )
        db.session.add(event)
        db.session.commit()
        flash("Event created", "success")
        return redirect(url_for("studentbody.body_dashboard", body_id=body.id))

    events = BodyEvent.query.filter_by(body_id=body.id).order_by(BodyEvent.date.desc()).all()
    return render_template("body_dashboard.html", body=body, events=events, form=form)

# Edit an event
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


# Delete an event
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


