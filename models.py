from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date

db = SQLAlchemy()

# ========================
# User & Student Models
# ========================

class User(db.Model, UserMixin):
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    cgpa = db.Column(db.Float, nullable=True)
    resume = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    profile_pic = db.Column(db.String(200), nullable=True)

    # new fields
    linkedin_url = db.Column(db.String(300), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

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

    comments = db.relationship("PostComment", backref="author", lazy=True, cascade="all, delete-orphan")
    votes = db.relationship("PostVote", backref="voter", lazy=True, cascade="all, delete-orphan")

    def get_id(self):
        return f"U_{self.id}"

    @property
    def user_type(self):
        return "student"

    @property
    def is_student_body(self):
        return False


class StudentBody(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    body_type = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(200), nullable=False)
    logo = db.Column(db.String(200), nullable=True)

    # new socials
    linkedin_url = db.Column(db.String(300), nullable=True)
    instagram_url = db.Column(db.String(300), nullable=True)

    posts = db.relationship("StudentBodyPost", backref="student_body", lazy=True, cascade="all, delete-orphan")
    events = db.relationship("BodyEvent", backref="body", lazy=True, cascade="all, delete-orphan")

    def get_id(self):
        return f"B_{self.id}"

    @property
    def user_type(self):
        return "body"

    @property
    def is_student_body(self):
        return True


# ========================
# Other Entities
# ========================

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


class BodyEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=True)
    poster = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    body_id = db.Column(db.Integer, db.ForeignKey('student_body.id'), nullable=False)


# ========================
# Social Feed System
# ========================

class StudentBodyPost(db.Model):
    __tablename__ = "student_body_posts"
    id = db.Column(db.Integer, primary_key=True)
    body_id = db.Column(db.Integer, db.ForeignKey("student_body.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship("PostComment", backref="post", lazy=True, cascade="all, delete-orphan")
    votes = db.relationship("PostVote", backref="post", lazy=True, cascade="all, delete-orphan")


class PostComment(db.Model):
    __tablename__ = "post_comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("student_body_posts.id"), nullable=False)
    user_id = db.Column(db.String(15), db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PostVote(db.Model):
    __tablename__ = "post_votes"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("student_body_posts.id"), nullable=False)
    user_id = db.Column(db.String(15), db.ForeignKey("user.id"), nullable=False)
    vote = db.Column(db.Integer, nullable=False)  # +1 or -1
