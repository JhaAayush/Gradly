from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, FloatField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields import DateField
from wtforms import BooleanField, TelField

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

# forms.py

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = TelField('Phone', validators=[Length(min=0, max=20)])
    cgpa = FloatField('CGPA')
    profile_pic = FileField('Profile Picture')

    # Privacy toggles
    show_email = BooleanField('Show Email')
    show_phone = BooleanField('Show Phone')
    show_cgpa = BooleanField('Show CGPA')

    submit = SubmitField('Save Changes')
