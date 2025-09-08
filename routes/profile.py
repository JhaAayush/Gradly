# routes/profile.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from models import db, User, WorkExperience, Internship, Certification, Skill, Hobby
from forms import EditProfileForm, WorkExperienceForm, InternshipForm, CertificationForm, SkillForm, HobbyForm
from werkzeug.utils import secure_filename
import os
from resume_parser import parse_resume
from models import User, StudentBody

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile/<string:user_id>')
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)


@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    profile_form = EditProfileForm()
    work_form = WorkExperienceForm()
    internship_form = InternshipForm()
    cert_form = CertificationForm()
    skill_form = SkillForm()
    hobby_form = HobbyForm()

    if request.method == 'GET':
        # Prefill only non-file fields
        profile_form.name.data = current_user.name
        profile_form.email.data = current_user.email
        profile_form.phone.data = current_user.phone
        profile_form.cgpa.data = current_user.cgpa
        profile_form.show_email.data = current_user.show_email
        profile_form.show_phone.data = current_user.show_phone
        profile_form.show_cgpa.data = current_user.show_cgpa

    if profile_form.submit.data and profile_form.validate_on_submit():
        current_user.name = profile_form.name.data
        current_user.email = profile_form.email.data
        current_user.phone = profile_form.phone.data
        current_user.cgpa = profile_form.cgpa.data
        current_user.show_email = profile_form.show_email.data
        current_user.show_phone = profile_form.show_phone.data
        current_user.show_cgpa = profile_form.show_cgpa.data
        
        # ✅ Handle resume upload
        if profile_form.resume.data and hasattr(profile_form.resume.data, "filename") and profile_form.resume.data.filename:
            if current_user.resume:
                old_resume_path = os.path.join(current_app.root_path, "static", current_user.resume)
                if os.path.exists(old_resume_path):
                    os.remove(old_resume_path)
            file = profile_form.resume.data
            ext = os.path.splitext(file.filename)[1]  # keep .pdf, .docx, etc.
            filename = secure_filename(f"{current_user.id}_resume{ext}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            current_user.resume = f'uploads/{filename}'

        # ✅ Handle profile pic upload
        if profile_form.profile_pic.data and hasattr(profile_form.profile_pic.data, "filename") and profile_form.profile_pic.data.filename:
            if current_user.profile_pic:
                old_pic_path = os.path.join(current_app.root_path, "static", current_user.profile_pic)
                if os.path.exists(old_pic_path):
                    os.remove(old_pic_path)
            file = profile_form.profile_pic.data
            ext = os.path.splitext(file.filename)[1]
            filename = secure_filename(f"{current_user.id}_profile{ext}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            current_user.profile_pic = f'uploads/{filename}'

        db.session.commit()
        flash("Profile updated!", "success")
        # --- CHANGE --- Redirect to the user's profile page
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Add work experience
    if work_form.submit.data and work_form.validate_on_submit():
        work = WorkExperience(
            organization=work_form.organization.data,
            role=work_form.role.data,
            start_date=work_form.start_date.data,
            end_date=work_form.end_date.data,
            user_id=current_user.id
        )
        db.session.add(work)
        db.session.commit()
        flash("Work experience added!", "success")
        # --- CHANGE --- Redirect to the user's profile page
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Add internship
    if internship_form.submit.data and internship_form.validate_on_submit():
        internship = Internship(
            organization=internship_form.organization.data,
            role=internship_form.role.data,
            start_date=internship_form.start_date.data,
            end_date=internship_form.end_date.data,
            user_id=current_user.id
        )
        db.session.add(internship)
        db.session.commit()
        flash("Internship added!", "success")
        # --- CHANGE --- Redirect to the user's profile page
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Add certification
    if cert_form.submit.data and cert_form.validate_on_submit():
        cert = Certification(title=cert_form.title.data, user_id=current_user.id)
        db.session.add(cert)
        db.session.commit()
        flash("Certification added!", "success")
        # --- CHANGE --- Redirect to the user's profile page
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Add skill
    if skill_form.submit.data and skill_form.validate_on_submit():
        skill = Skill(name=skill_form.name.data, user_id=current_user.id)
        db.session.add(skill)
        db.session.commit()
        flash("Skill added!", "success")
        # --- CHANGE --- Redirect to the user's profile page
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Add hobby
    if hobby_form.submit.data and hobby_form.validate_on_submit():
        hobby = Hobby(name=hobby_form.name.data, user_id=current_user.id)
        db.session.add(hobby)
        db.session.commit()
        flash("Hobby added!", "success")
        # --- CHANGE --- Redirect to the user's profile page
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    return render_template(
        "edit_profile.html",
        profile_form=profile_form,
        work_form=work_form,
        internship_form=internship_form,
        cert_form=cert_form,
        skill_form=skill_form,
        hobby_form=hobby_form
    )


@profile_bp.route("/search")
@login_required
def search_users():
    q = request.args.get("q", "").strip()
    results = []

    if q:
        users = User.query.filter(User.name.ilike(f"%{q}%")).all()
        bodies = StudentBody.query.filter(StudentBody.name.ilike(f"%{q}%")).all()

        for u in users:
            results.append({
                "id": u.id,
                "name": u.name,
                "type": "student",
                "url": url_for("profile.view_profile", user_id=u.id)
            })

        for b in bodies:
            results.append({
                "id": b.id,
                "name": b.name,
                "type": "body",
                "url": url_for("studentbody.body_profile", body_id=b.id)
            })

    return jsonify(results)
