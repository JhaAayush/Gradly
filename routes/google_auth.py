import os
from flask import Blueprint, redirect, request, url_for, session, render_template, flash
from flask_login import login_user
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from models import db, User, StudentBody
from forms import CompleteProfileForm

load_dotenv()

google_auth_bp = Blueprint('google_auth', __name__)

# --- Google OAuth Configuration ---
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = 'http://127.0.0.1:5000/google/callback'

AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://www.googleapis.com/oauth2/v4/token"
SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]

@google_auth_bp.route('/login/<user_type>')
def login(user_type):
    session['user_type'] = user_type # Store whether it's a 'student' or 'body'
    google = OAuth2Session(GOOGLE_CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)
    authorization_url, state = google.authorization_url(AUTHORIZATION_BASE_URL, prompt="select_account")
    session['oauth_state'] = state
    return redirect(authorization_url)

@google_auth_bp.route('/callback')
def callback():
    if 'oauth_state' not in session:
        return 'Missing state parameter.', 400

    google = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=REDIRECT_URI, state=session['oauth_state'])
    try:
        token = google.fetch_token(TOKEN_URL, client_secret=GOOGLE_CLIENT_SECRET, authorization_response=request.url)
    except Exception as e:
        flash(f'An error occurred during authentication: {e}', 'danger')
        return redirect(url_for('auth.login'))

    user_info = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    
    user_type = session.get('user_type', 'student') # Default to student
    user_email = user_info['email']
    user_google_id = user_info['id']
    user_name = user_info['name']
    user_picture = user_info.get('picture')

    # --- Handle Student Login/Registration ---
    if user_type == 'student':
        user = User.query.filter_by(google_id=user_google_id).first()
        if not user:
            user = User.query.filter_by(email=user_email).first()
            if user: # Existing user, link their Google account
                user.google_id = user_google_id
                db.session.commit()
            else: # New user
                # We don't have a roll number, so we need to ask for it.
                session['google_new_user_info'] = user_info
                return redirect(url_for('google_auth.complete_profile'))
        
        login_user(user)
        flash('Logged in successfully with Google!', 'success')
        return redirect(url_for('dashboard.dashboard'))

    # --- Handle Student Body Login/Registration ---
    elif user_type == 'body':
        body = StudentBody.query.filter_by(google_id=user_google_id).first()
        if not body:
            body = StudentBody.query.filter_by(email=user_email).first()
            if body: # Existing body, link Google account
                body.google_id = user_google_id
            else: # New student body
                body = StudentBody(
                    name=user_name,
                    email=user_email,
                    google_id=user_google_id,
                    logo=user_picture
                )
                db.session.add(body)
            db.session.commit()
        
        login_user(body)
        flash('Student Body logged in successfully with Google!', 'success')
        return redirect(url_for('studentbody.body_dashboard')) # Or wherever bodies go

    return redirect(url_for('auth.login'))

@google_auth_bp.route('/complete-profile', methods=['GET', 'POST'])
def complete_profile():
    if 'google_new_user_info' not in session:
        return redirect(url_for('auth.register'))

    form = CompleteProfileForm()
    user_info = session['google_new_user_info']
    
    if form.validate_on_submit():
        roll_number = form.roll_number.data
        if User.query.get(roll_number):
            flash('This Roll Number is already registered. Please log in.', 'danger')
            return redirect(url_for('auth.login'))

        new_user = User(
            id=roll_number,
            name=user_info['name'],
            email=user_info['email'],
            google_id=user_info['id'],
            profile_pic=user_info.get('picture')
        )
        db.session.add(new_user)
        db.session.commit()

        session.pop('google_new_user_info', None) # Clean up session
        login_user(new_user)
        flash('Registration complete! Welcome.', 'success')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('complete_profile.html', form=form, user_name=user_info['name'])