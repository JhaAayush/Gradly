# import_student_bodies.py
import os
import pandas as pd
from flask_bcrypt import Bcrypt

# adjust import to match your app structure
from app import app, db
from models import StudentBody

EXCEL_PATH = "Student_bodies.xlsx"  # path you uploaded

def import_bodies(excel_path=EXCEL_PATH):
    bcrypt = Bcrypt(app)
    df = pd.read_excel(excel_path)  # requires openpyxl

    # expected columns: Name, Email_id, Body_Type, Description
    created = 0
    with app.app_context():
        for idx, row in df.iterrows():
            name = str(row.get('Name', '')).strip()
            email = str(row.get('Email_id', '')).strip()
            body_type = str(row.get('Body_Type', '')).strip()
            description = str(row.get('Description', '')).strip()

            if not email or not name:
                print(f"Skipping row {idx} missing name/email")
                continue

            # check existing
            existing = StudentBody.query.filter_by(email=email).first()
            if existing:
                print(f"Already exists: {email}")
                continue

            hashed = bcrypt.generate_password_hash("password").decode('utf-8')
            sb = StudentBody(
                name=name,
                email=email,
                body_type=body_type,
                description=description,
                password=hashed
            )
            db.session.add(sb)
            created += 1

        db.session.commit()
    print(f"Import finished. Created {created} student bodies.")

if __name__ == "__main__":
    import_bodies()
