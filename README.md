# Gradly

Gradly is a web application designed to facilitate communication and engagement within a student community, potentially for a college or university. It provides features for student bodies to manage events and posts, and for individual students to create profiles, interact through messaging, and stay updated with campus activities.

## Features

- **User Authentication:** Secure login and registration for students and student bodies, including Google OAuth integration.
- **Profiles:** Personalized profiles for students and student bodies.
- **Posts & Feed:** Student bodies can create and manage posts, which are displayed on a central feed for students.
- **Events Management:** Student bodies can create, edit, and publish events.
- **Messaging:** Direct messaging functionality between users.
- **Resources:** A section for sharing resources.
- **Task Management:** Functionality for managing tasks.

## Technologies Used

- **Backend:** Python (Flask)
- **Database:** SQLAlchemy (ORM) with Alembic for migrations
- **Frontend:** HTML, CSS, JavaScript (Jinja2 templating)
- **Authentication:** Flask-Login, Google OAuth
- **File Storage:** Local uploads for profile pictures, event images, and post media.

## Setup Instructions

To get Gradly up and running on your local machine, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd Gradly
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python3 -m venv .gradly
    source .gradly/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database:**

    ```bash
    flask db upgrade
    ```

5.  **Run the application:**

    ```bash
    flask run
    ```

    The application should now be running on `http://127.0.0.1:5000/`.

## Usage

-   **Register/Login:** Access the registration or login pages to create an account or sign in.
-   **Dashboard:** After logging in, navigate to your personalized dashboard.
-   **Student Body Features:** If you are a student body, you can create posts, manage events, and update your profile.
-   **Student Features:** As a student, you can view the feed, check out events, message other users, and manage your profile.
