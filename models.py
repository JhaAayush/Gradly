from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# models.py

class User(db.Model, UserMixin):
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    cgpa = db.Column(db.Float, nullable=True)
    resume = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    profile_pic = db.Column(db.String(200), nullable=True)

    # Privacy flags
    show_email = db.Column(db.Boolean, default=True)
    show_phone = db.Column(db.Boolean, default=True)
    show_cgpa = db.Column(db.Boolean, default=True)

    # 🔑 Relationships
    work_experiences = db.relationship('WorkExperience', backref='user', lazy=True)
    internships = db.relationship('Internship', backref='user', lazy=True)
    certifications = db.relationship('Certification', backref='user', lazy=True)
    skills = db.relationship('Skill', backref='user', lazy=True)
    hobbies = db.relationship('Hobby', backref='user', lazy=True)

    def get_id(self):
        return f"U_{self.id}"

    @property
    def user_type(self):
        return "student"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    is_done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)


# models.py

# models.py

# models.py

class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.String(15), db.ForeignKey('user.id'), nullable=False)

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.String(15), db.ForeignKey('user.id'), nullable=False)

class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.String(15), db.ForeignKey('user.id'), nullable=False)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(15), db.ForeignKey('user.id'), nullable=False)

class Hobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(15), db.ForeignKey('user.id'), nullable=False)


# models.py (append or integrate)

from datetime import datetime

class StudentBody(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    body_type = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(200), nullable=False)
    logo = db.Column(db.String(200), nullable=True)

    def get_id(self):
        return f"B_{self.id}"  # unique prefix so it doesn’t collide with student IDs
    
    @property
    def user_type(self):
        return "body"


class BodyEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=True)
    poster = db.Column(db.String(200), nullable=True)  # path in static/uploads/
    date = db.Column(db.DateTime, default=datetime.utcnow)
    body_id = db.Column(db.Integer, db.ForeignKey('student_body.id'), nullable=False)

    body = db.relationship('StudentBody', backref=db.backref('events', lazy=True))
