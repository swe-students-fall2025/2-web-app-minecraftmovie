# app/routes/other_user_profile.py

from flask import Blueprint, render_template, current_app, abort
from bson import ObjectId

other_user_profile_bp = Blueprint("other_user_profile", __name__)

@other_user_profile_bp.route("/user/<username>")
def other_user_profile(username: str):
    db = current_app.db

    # user
    user = db.users.find_one({"username": username})
    if not user:
        abort(404)

    # (now includes genre/year)
    proj = {
        "title": 1,
        "artist": 1,
        "rating": 1,
        "review": 1,
        "genre": 1,
        "year": 1,
    }

    # favorites (latest first)
    favorite_songs = list(
        db.songs.find({"user_id": user["_id"], "favorite": True}, proj)
        .sort("_id", -1)
        .limit(50)
    )

    # recent (latest first)
    recent_songs = list(
        db.songs.find({"user_id": user["_id"]}, proj)
        .sort("_id", -1)
        .limit(50)
    )

    # stats
    total = db.songs.count_documents({"user_id": user["_id"]})
    stats = {
        "total": total,
        "five_star": db.songs.count_documents({"user_id": user["_id"], "rating": 5}),
        "four_star": db.songs.count_documents({"user_id": user["_id"], "rating": 4}),
        "three_star": db.songs.count_documents({"user_id": user["_id"], "rating": 3}),
        "two_star": db.songs.count_documents({"user_id": user["_id"], "rating": 2}),
        "one_star": db.songs.count_documents({"user_id": user["_id"], "rating": 1}),
    } if total else None

    return render_template(
        "other_user_profile.html",
        user=user,
        favorite_songs=favorite_songs,
        recent_songs=recent_songs,
        stats=stats,
    )
