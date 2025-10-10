from flask import Blueprint, render_template
from flask import current_app
from bson import ObjectId

home_bp = Blueprint("home", __name__)

@home_bp.get("/")
def home_view():
    page_title_text = "Rate Songs"

    #read a few docs from MongoDB (safe even if collection is empty)
    songs_cursor = current_app.db.songs.find().limit(20)  # NEW
    songs = []  
    for s in songs_cursor:  
        # convert ObjectId to string so Jinja doesn’t choke if you print it  
        if isinstance(s.get("_id"), ObjectId): 
            s["_id"] = str(s["_id"])  
        songs.append(s)  

    return render_template("home.html", page_title_text=page_title_text, songs=songs)
