from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from models import db, User, Task, StudentBody
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.tasks import tasks_bp
from routes.events import events_bp
import os
from werkzeug.utils import secure_filename
from routes.profile import profile_bp
from routes.studentbody import studentbody_bp
from routes.studentbody_auth import studentbody_auth_bp

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Config
app.config['SECRET_KEY'] = 'yoursecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gradly.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    if user_id.startswith("U_"):
        roll = user_id.split("_", 1)[1]   # keep string as-is
        return User.query.get(roll)
    elif user_id.startswith("B_"):
        body_id = user_id.split("_", 1)[1]
        return StudentBody.query.get(int(body_id))
    return None



@app.before_request
def create_tables():
    db.create_all()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(events_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(studentbody_bp)
app.register_blueprint(studentbody_auth_bp)

# Home route stays here
@app.route('/')
def home():
    closest_task = None
    if current_user.is_authenticated:
        closest_task = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date).first()
        print(current_user)
    return render_template('home.html', closest_task=closest_task)

if __name__ == '__main__':
    app.run(debug=True)
