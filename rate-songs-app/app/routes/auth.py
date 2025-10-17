from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import UserDoc

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("profile.view_profile"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not email or not password:
            flash("Please provide both email and password.", "error")
            return render_template("login.html")

        user = current_app.db.users.find_one({"email": email})

        if user is None:
            # Sign-up on first use
            user = {
                "email": email,
                "username": email.split("@")[0],
                "password_hash": generate_password_hash(password),
                "favorite_song_id": None,
            }
            current_app.db.users.insert_one(user)
            user = current_app.db.users.find_one({"email": email})
            login_user(UserDoc(user))
            flash("Account created and logged in.", "success")
            return redirect(url_for("home.home"))

        if not check_password_hash(user.get("password_hash", ""), password):
            flash("Incorrect password. Try again.", "error")
            return render_template("login.html")

        login_user(UserDoc(user))
        flash("Logged in successfully.", "success")
        return redirect(url_for("home.home"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Logged out.", "info")
    return redirect(url_for("home.home"))
