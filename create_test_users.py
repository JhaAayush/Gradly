from app import app, db
from models import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

with app.app_context():
    db.create_all()

    # Create a test user
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    new_user = User(
        id='2023A7PS0001G',
        name='Test User',
        email='test@example.com',
        password=hashed_password
    )
    db.session.add(new_user)

    # Create another test user to view their profile
    hashed_password_2 = bcrypt.generate_password_hash('password2').decode('utf-8')
    new_user_2 = User(
        id='2023A7PS0002G',
        name='Test User 2',
        email='test2@example.com',
        password=hashed_password_2
    )
    db.session.add(new_user_2)

    db.session.commit()
