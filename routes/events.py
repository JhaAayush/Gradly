from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import db, BodyEvent, StudentBody
from forms import BodyEventForm

events_bp = Blueprint('events', __name__)

@events_bp.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data, description=form.description.data)
        db.session.add(event)
        db.session.commit()
        flash('Event added!', 'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('add_event.html', form=form)
