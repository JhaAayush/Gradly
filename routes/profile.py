# routes/profile.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from models import db, User
from forms import EditProfileForm
from werkzeug.utils import secure_filename
import os

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile/<string:user_id>')
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        # Update text fields
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.cgpa = form.cgpa.data

        # Privacy flags
        current_user.show_email = form.show_email.data
        current_user.show_phone = form.show_phone.data
        current_user.show_cgpa = form.show_cgpa.data

        # Handle profile pic upload
        if form.profile_pic.data:
            filename = secure_filename(form.profile_pic.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.profile_pic.data.save(filepath)
            current_user.profile_pic = f'uploads/{filename}'

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.view_profile', user_id=current_user.id))
    return render_template('edit_profile.html', form=form)


@profile_bp.route('/search')
@login_required
def search_users():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    users = User.query.filter(User.name.ilike(f"%{q}%")).all()
    results = [{"id": user.id, "name": user.name} for user in users]
    return jsonify(results)
