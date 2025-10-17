from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from bson import ObjectId

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_song():
    if request.method == "POST":
        rating_str = request.form.get("rating", "0")
        try:
            rating = int(rating_str)
        except ValueError:
            rating = 0

        song_data = {
            "title": request.form.get("title") or "Untitled",
            "artist": request.form.get("artist") or "Unknown",
            "rating": rating,
            "review": request.form.get("review") or "",
            "favorite": bool(request.form.get("favorite")),
            "user_id": ObjectId(current_user.doc["_id"])
        }

        current_app.db.songs.insert_one(song_data)

        return redirect(url_for("profile.view_profile"))

    return render_template("upload.html")




