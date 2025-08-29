# routes/tasks.py
from flask import Blueprint, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models import db, Task
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from forms import TaskForm  # ✅ THIS is missing

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/task/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    task.is_done = not task.is_done
    db.session.commit()
    flash('Task status updated!', 'success')
    return redirect(url_for('dashboard.dashboard'))

@tasks_bp.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!', 'info')
    return redirect(url_for('dashboard.dashboard'))

@tasks_bp.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.due_date = form.due_date.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('edit_task.html', form=form, task=task)
