from bson import ObjectId
from flask import Blueprint, redirect, url_for, current_app
from flask_login import login_required, current_user

delete_bp = Blueprint("delete", __name__, url_prefix="/songs")

@delete_bp.route("/delete/<id>", methods=["POST"])
@login_required
def delete_song(id):
    db = current_app.db
    songs_col = db.songs
    uid = current_user.get_id()

    song = songs_col.find_one({"_id": ObjectId(id), "owner_id": uid})
    if not song:
        return "Song not found or access denied", 404

    songs_col.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("songs.all_songs"))