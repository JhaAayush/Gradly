from app import app, db, bcrypt  # Import your app, db, and bcrypt from your app.py
from models import User         # Import the User model

def create_admin_users():
    """
    Creates admin users if they don't already exist.
    """
    
    # 1. Hash the password
    # IMPORTANT: We store the HASH, not the plain-text password.
    hashed_password = bcrypt.generate_password_hash("password").decode('utf-8')

    # 2. Define the admin users' data
    admins_to_add = [
        {
            "id": "MBABA04019",
            "name": "Prateek Guha",
            "email": "prateekg.mbaba04@iimamritsar.ac.in",
        },
        {
            "id": "MBABA04002",
            "name": "Aayush Jha",
            "email": "aayushj.mbaba04@iimamritsar.ac.in",
        },
         {
            "id": "MBABA04020",
            "name": "Preksha Jha",
            "email": "prekshaj.mbaba04@iimamritsar.ac.in",
        },
    ]

    # 3. Use the app context to interact with the database
    with app.app_context():
        print("Checking for and adding admin users...")
        for admin_data in admins_to_add:
            
            # Check if user already exists by ID
            existing_user = User.query.get(admin_data["id"])
            
            if existing_user:
                # If they exist, just make sure they are an admin
                existing_user.is_admin = True
                print(f"User {existing_user.name} ({existing_user.id}) already exists. Updating to admin.")
            else:
                # If they don't exist, create a new user
                new_admin = User(
                    id=admin_data["id"],
                    name=admin_data["name"],
                    email=admin_data["email"],
                    password=hashed_password,
                    is_admin=True  # <-- Set them as admin
                )
                db.session.add(new_admin)
                print(f"Creating new admin user: {new_admin.name} ({new_admin.id})")

        # 4. Commit the changes to the database
        try:
            db.session.commit()
            print("Admin users created/updated successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_admin_users()