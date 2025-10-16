from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from bson import ObjectId

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile")
@login_required
def view_profile():
    user = current_user.doc
    user_id = ObjectId(user["_id"])

    favorite_songs_cursor = (
            current_app.db.songs
            .find({"user_id": user_id, "favorite": True})
            .sort("_id", -1)   # optional: newest first
            .limit(10)
        )
    favorite_songs = list(favorite_songs_cursor)

    recent_songs = list(
        current_app.db.songs.find({"user_id": user_id}).sort("_id", -1).limit(5)
    )

    for s in favorite_songs + recent_songs:
        s["_id"] = str(s["_id"])

    all_songs = list(current_app.db.songs.find({"user_id": user_id}))
    stats = {
        "total": len(all_songs),
        "five_star": sum(1 for s in all_songs if s.get("rating") == 5) or 0,
        "four_star": sum(1 for s in all_songs if s.get("rating") == 4) or 0,
        "three_star": sum(1 for s in all_songs if s.get("rating") == 3) or 0,
        "two_star": sum(1 for s in all_songs if s.get("rating") == 2) or 0,
        "one_star": sum(1 for s in all_songs if s.get("rating") == 1) or 0
    }



    return render_template(
        "profile.html",
        user=user,
        favorite_songs=favorite_songs,
        recent_songs=recent_songs,
        stats=stats,
    )
