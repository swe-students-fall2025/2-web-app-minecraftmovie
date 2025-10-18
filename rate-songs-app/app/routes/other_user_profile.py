from flask import Blueprint, render_template, current_app, abort
from bson import ObjectId

other_user_profile_bp = Blueprint("other_user_profile", __name__)

@other_user_profile_bp.route("/user/<username>")
def other_user_profile(username):
    user = current_app.db.users.find_one({"username": username})
    if not user:
        abort(404, description="User not found")

    user_id = ObjectId(user["_id"])

    favorite_songs = list(
        current_app.db.songs
        .find({"user_id": user_id, "favorite": True})
        .sort("_id", -1)
        .limit(10)
    )

    recent_songs = list(
        current_app.db.songs
        .find({"user_id": user_id})
        .sort("_id", -1)
        .limit(5)
    )

    for s in favorite_songs + recent_songs:
        s["_id"] = str(s["_id"])

    all_songs = list(current_app.db.songs.find({"user_id": user_id}))
    stats = {
        "total": len(all_songs),
        "five_star": sum(1 for s in all_songs if s.get("rating") == 5),
        "four_star": sum(1 for s in all_songs if s.get("rating") == 4),
        "three_star": sum(1 for s in all_songs if s.get("rating") == 3),
        "two_star": sum(1 for s in all_songs if s.get("rating") == 2),
        "one_star": sum(1 for s in all_songs if s.get("rating") == 1),
    }

    return render_template(
        "other_user_profile.html",
        user=user,
        favorite_songs=favorite_songs,
        recent_songs=recent_songs,
        stats=stats,
    )
