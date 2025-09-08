from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash
from models import StudentBody
from forms import BodyLoginForm
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

studentbody_auth_bp = Blueprint("studentbody_auth", __name__)

@studentbody_auth_bp.route("/body/login", methods=["GET", "POST"])
def body_login():
    form = BodyLoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data

        body = StudentBody.query.filter_by(email=email).first()

        if body and bcrypt.check_password_hash(body.password, password):
            login_user(body)
            flash("Logged in successfully as Student Body!", "success")
            return redirect(url_for("studentbody.body_dashboard", body_id=body.id))
        else:
            flash("Invalid credentials", "danger")

    return render_template("body_login.html", form=form)
