from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app.forms import HostLoginForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("events.events_list"))

    form = HostLoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.is_host and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("events.events_list"))

        flash("Invalid username or password, or you are not a host.")

    return render_template("login.html", form=form, title="Host Login")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.home"))
