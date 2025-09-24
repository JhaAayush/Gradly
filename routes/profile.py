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

    # Handle Profile Form
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
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Handle Multiple Work Experience Entries
    if 'submit_work' in request.form:
        work_entries_count = int(request.form.get('work_entries_count', 0))
        saved_count = 0
        
        for i in range(work_entries_count):
            organization = request.form.get(f'work_organization_{i}', '').strip()
            role = request.form.get(f'work_role_{i}', '').strip()
            start_date_str = request.form.get(f'work_start_date_{i}')
            end_date_str = request.form.get(f'work_end_date_{i}')
            
            if organization:  # Only save if organization is provided
                start_date = None
                end_date = None
                
                if start_date_str:
                    try:
                        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                    except ValueError:
                        pass
                
                if end_date_str:
                    try:
                        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                    except ValueError:
                        pass
                
                work = WorkExperience(
                    organization=organization,
                    role=role if role else None,
                    start_date=start_date,
                    end_date=end_date,
                    user_id=current_user.id
                )
                db.session.add(work)
                saved_count += 1
        
        if saved_count > 0:
            db.session.commit()
            flash(f"{saved_count} work experience(s) added successfully!", "success")
        else:
            flash("Please fill in at least one organization name.", "warning")
        
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Handle Multiple Internship Entries
    if 'submit_intern' in request.form:
        intern_entries_count = int(request.form.get('intern_entries_count', 0))
        saved_count = 0
        
        for i in range(intern_entries_count):
            organization = request.form.get(f'intern_organization_{i}', '').strip()
            role = request.form.get(f'intern_role_{i}', '').strip()
            start_date_str = request.form.get(f'intern_start_date_{i}')
            end_date_str = request.form.get(f'intern_end_date_{i}')
            
            if organization:
                start_date = None
                end_date = None
                
                if start_date_str:
                    try:
                        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                    except ValueError:
                        pass
                
                if end_date_str:
                    try:
                        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                    except ValueError:
                        pass
                
                internship = Internship(
                    organization=organization,
                    role=role if role else None,
                    start_date=start_date,
                    end_date=end_date,
                    user_id=current_user.id
                )
                db.session.add(internship)
                saved_count += 1
        
        if saved_count > 0:
            db.session.commit()
            flash(f"{saved_count} internship(s) added successfully!", "success")
        else:
            flash("Please fill in at least one organization name.", "warning")
        
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Handle Multiple Certification Entries
    if 'submit_cert' in request.form:
        cert_entries_count = int(request.form.get('cert_entries_count', 0))
        saved_count = 0
        
        for i in range(cert_entries_count):
            title = request.form.get(f'cert_title_{i}', '').strip()
            
            if title:
                cert = Certification(title=title, user_id=current_user.id)
                db.session.add(cert)
                saved_count += 1
        
        if saved_count > 0:
            db.session.commit()
            flash(f"{saved_count} certification(s) added successfully!", "success")
        else:
            flash("Please fill in at least one certification title.", "warning")
        
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Handle Multiple Skill Entries
    if 'submit_skill' in request.form:
        skill_entries_count = int(request.form.get('skill_entries_count', 0))
        saved_count = 0
        
        for i in range(skill_entries_count):
            name = request.form.get(f'skill_name_{i}', '').strip()
            
            if name:
                # Check if skill already exists to avoid duplicates
                existing_skill = Skill.query.filter_by(name=name, user_id=current_user.id).first()
                if not existing_skill:
                    skill = Skill(name=name, user_id=current_user.id)
                    db.session.add(skill)
                    saved_count += 1
        
        if saved_count > 0:
            db.session.commit()
            flash(f"{saved_count} skill(s) added successfully!", "success")
        else:
            flash("Please fill in at least one skill name or all skills already exist.", "warning")
        
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Handle Multiple Hobby Entries
    if 'submit_hobby' in request.form:
        hobby_entries_count = int(request.form.get('hobby_entries_count', 0))
        saved_count = 0
        
        for i in range(hobby_entries_count):
            name = request.form.get(f'hobby_name_{i}', '').strip()
            
            if name:
                # Check if hobby already exists to avoid duplicates
                existing_hobby = Hobby.query.filter_by(name=name, user_id=current_user.id).first()
                if not existing_hobby:
                    hobby = Hobby(name=name, user_id=current_user.id)
                    db.session.add(hobby)
                    saved_count += 1
        
        if saved_count > 0:
            db.session.commit()
            flash(f"{saved_count} hobby/hobbies added successfully!", "success")
        else:
            flash("Please fill in at least one hobby name or all hobbies already exist.", "warning")
        
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Keep original single-entry handlers for backward compatibility
    # Add work experience (single entry)
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
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Add internship (single entry)
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
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Add certification (single entry)
    if cert_form.submit.data and cert_form.validate_on_submit():
        cert = Certification(title=cert_form.title.data, user_id=current_user.id)
        db.session.add(cert)
        db.session.commit()
        flash("Certification added!", "success")
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Add skill (single entry)
    if skill_form.submit.data and skill_form.validate_on_submit():
        skill = Skill(name=skill_form.name.data, user_id=current_user.id)
        db.session.add(skill)
        db.session.commit()
        flash("Skill added!", "success")
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    # Add hobby (single entry)
    if hobby_form.submit.data and hobby_form.validate_on_submit():
        hobby = Hobby(name=hobby_form.name.data, user_id=current_user.id)
        db.session.add(hobby)
        db.session.commit()
        flash("Hobby added!", "success")
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
