# app/routes/home.py

# imports
from flask import Blueprint, render_template, request, session, current_app

# blueprint
home_bp = Blueprint("home", __name__)

# route
@home_bp.route("/")
def home():
    # query
    q = request.args.get("q", "").strip()

    # history
    hist = session.get("profile_history", [])
    if q:
        hist = [v for v in [q] + hist if v][:5]
        session["profile_history"] = hist

    # filter
    filt = {}
    if q:
        rx = {"$regex": q, "$options": "i"}
        filt = {"$or": [{"name": rx}, {"email": rx}]}

    # users
    users = list(
        current_app.db.users
        .find(filt, {"password": 0})
        .sort("name", 1)
        .limit(100)
    )

    # genres
    try:
        genres = [g for g in current_app.db.songs.distinct("genre") if g][:18]
    except Exception:
        genres = []

    # render
    return render_template(
        "home.html",
        q=q,
        history=hist,
        users=users,
        genres=genres,
    )
