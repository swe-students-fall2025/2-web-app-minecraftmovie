from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)

@home_bp.get("/")
def home_view():
    page_title_text = "Rate Songs"
    return render_template("home.html", page_title_text=page_title_text)
