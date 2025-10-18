from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_required, current_user

# name = 'edit', so endpoint names become 'edit.edit_song'
edit_bp = Blueprint("edit", __name__, url_prefix="/songs")

@edit_bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_song(id):
    db = current_app.db
    songs_col = db.songs
    uid = current_user.get_id()

    song = songs_col.find_one({"_id": ObjectId(id), "owner_id": uid})
    if not song:
        return "Song not found or access denied", 404

    if request.method == "POST":
        new_title = request.form.get("title", "").strip()
        new_artist = request.form.get("artist", "").strip()
        new_rating = int(request.form.get("rating", song.get("rating", 0)))
        new_review = request.form.get("review", "").strip()
        new_favorite = "favorite" in request.form  # True if checkbox checked

        songs_col.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "title": new_title,
                    "artist": new_artist,
                    "rating": new_rating,
                    "review": new_review,
                    "favorite": new_favorite,
                }
            },
        )
        return redirect(url_for("songs.all_songs"))

    return render_template("edit_song.html", song=song)