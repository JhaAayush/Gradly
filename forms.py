from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, FloatField
from wtforms.validators import DataRequired, Email, Length, Optional
from wtforms.fields import DateField
from wtforms import BooleanField, TelField
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField

class RegisterForm(FlaskForm):
    roll_number = StringField('Roll Number', validators=[DataRequired(), Length(min=5, max=20)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email_or_roll = StringField('Email or Roll Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired()])
    due_date = DateField('Deadline', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Task')

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Add Event')

class EditProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[Optional()])
    cgpa = FloatField("CGPA", validators=[Optional()])
    profile_pic = FileField("Profile Picture")
    linkedin_url = StringField("LinkedIn URL", validators=[Optional()])
    resume = FileField("Resume (PDF)")
    dob = DateField("Date of Birth", format="%Y-%m-%d", validators=[Optional()])
    show_email = BooleanField("Show Email")
    show_phone = BooleanField("Show Phone")
    show_cgpa = BooleanField("Show CGPA")

    submit = SubmitField("Save Changes")

# Updated forms to handle multiple entries - these will be used for validation only
class WorkExperienceForm(FlaskForm):
    organization = StringField("Organization", validators=[DataRequired()])
    role = StringField("Role", validators=[Optional()])
    start_date = DateField("Start Date", format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField("End Date", format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField("Add Work Experience")

class InternshipForm(FlaskForm):
    organization = StringField("Organization", validators=[DataRequired()])
    role = StringField("Role", validators=[Optional()])
    start_date = DateField("Start Date", format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField("End Date", format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField("Add Internship")

class CertificationForm(FlaskForm):
    title = StringField("Certification", validators=[DataRequired()])
    submit = SubmitField("Add Certification")

class SkillForm(FlaskForm):
    name = StringField("Skill", validators=[DataRequired()])
    submit = SubmitField("Add Skill")

class HobbyForm(FlaskForm):
    name = StringField("Hobby", validators=[DataRequired()])
    submit = SubmitField("Add Hobby")

class BodyEventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=250)])
    description = TextAreaField("Description", validators=[Length(max=1000)])
    poster = FileField("Poster")  # optional, allow uploads
    date = DateField("Event Date", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Save Event")

class BodyLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class BodyPostForm(FlaskForm):
    title = StringField("Post Title", validators=[DataRequired(), Length(max=200)])
    content = TextAreaField("Content", validators=[DataRequired(), Length(max=5000)])
    image = FileField("Image", validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField("Publish Post")
