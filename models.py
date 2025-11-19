from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date, timedelta
import os
import click
from sqlalchemy import event
from flask import current_app
from flask.cli import with_appcontext

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
    posts = db.relationship("Post", backref="user", lazy=True, cascade="all, delete-orphan")

    def get_id(self):
        return f"U_{self.id}"

    @property
    def user_type(self):
        return "student"


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

    posts = db.relationship("Post", backref="student_body", lazy=True, cascade="all, delete-orphan")
    events = db.relationship("BodyEvent", backref="body", lazy=True, cascade="all, delete-orphan")

    def get_id(self):
        return f"B_{self.id}"

    @property
    def user_type(self):
        return "body"


# ========================
# Other Entities
# ========================

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    is_done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'))


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

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Author relationship
    user_id = db.Column(db.String(15), db.ForeignKey("user.id"), nullable=True)
    body_id = db.Column(db.Integer, db.ForeignKey("student_body.id"), nullable=True)

    # Polymorphic relationship to author
    @property
    def author(self):
        return self.user or self.student_body

    comments = db.relationship("PostComment", backref="post", lazy=True, cascade="all, delete-orphan")
    votes = db.relationship("PostVote", backref="post", lazy=True, cascade="all, delete-orphan")


class PostComment(db.Model):
    __tablename__ = "post_comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.String(15), db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PostVote(db.Model):
    __tablename__ = "post_votes"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.String(15), db.ForeignKey("user.id"), nullable=False)
    vote = db.Column(db.Integer, nullable=False)  # +1 or -1


# ========================
# Messaging System
# ========================

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_one_id = db.Column(db.String(50), nullable=False)
    user_two_id = db.Column(db.String(50), nullable=False)
    messages = db.relationship('Message', backref='conversation', lazy=True, cascade="all, delete-orphan")
    last_message_time = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (
        db.UniqueConstraint('user_one_id', 'user_two_id', name='_user_pair_uc'),
    )


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    sender_id = db.Column(db.String(50), nullable=False) 
    receiver_id = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)


# ========================
# NEW: Event Listeners & CLI
# ========================

@event.listens_for(Post, 'after_delete')
def delete_post_image(mapper, connection, target):
    """
    Listens for a Post object deletion and removes the associated
    image file from the static/uploads folder.
    """
    if target.image_url:
        try:
            # Assumes UPLOAD_FOLDER is 'static/uploads'
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            filename = os.path.basename(target.image_url)
            file_path = os.path.join(upload_folder, filename)

            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            # Log the error but don't block deletion
            print(f"Error deleting file {target.image_url}: {e}")


def register_cli_commands(app):
    """Registers CLI commands with the Flask app."""
    
    @app.cli.command("cleanup-posts")
    @with_appcontext
    def cleanup_posts_command():
        """Deletes posts older than 7 days."""
        try:
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            old_posts = Post.query.filter(Post.created_at <= seven_days_ago).all()
            
            if not old_posts:
                click.echo("No old posts found to delete.")
                return

            post_count = len(old_posts)
            
            # The 'after_delete' event listener will handle file deletion
            for post in old_posts:
                db.session.delete(post)
            
            db.session.commit()
            click.echo(f"Successfully deleted {post_count} old post(s).")

        except Exception as e:
            db.session.rollback()
            click.echo(f"Error during post cleanup: {e}")