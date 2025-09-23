# routes/dashboard.py
from flask import Blueprint, render_template, flash, request, url_for, redirect
from flask_login import login_required, current_user
from models import Task, Event, db
from forms import TaskForm
from models import Task, BodyEvent, StudentBody


dashboard_bp = Blueprint('dashboard', __name__)  # This name is IMPORTANT

@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # student’s own tasks
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date).all()
    
    # events created by student bodies, ordered by soonest first
    body_events = BodyEvent.query.order_by(BodyEvent.date.asc()).limit(5).all()

    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            due_date=form.due_date.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added with deadline!', 'success')
        return redirect(url_for('dashboard.dashboard'))

    return render_template(
        "dashboard.html",
        tasks=tasks,
        events=body_events,   # ✅ pass body events here
        form=form
    )

