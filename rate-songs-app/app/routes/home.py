# app/routes/home.py

from flask import Blueprint, render_template, request, session, current_app
import re

home_bp = Blueprint("home", __name__)

def _loose_regex(s: str) -> str:
    """
    ignores punctuation/spacing between characters.
    """
    tokens = re.sub(r"[^A-Za-z0-9]+", " ", s, flags=re.I).strip()
    if not tokens:
        return re.escape(s)
    return r"[^A-Za-z0-9]*".join(map(re.escape, tokens))

@home_bp.route("/")
def home():
    # query
    q = request.args.get("q", "").strip()

    # history (store last 5)
    hist = session.get("profile_history", [])
    if q:
        hist = [v for v in [q] + hist if v][:5]
        session["profile_history"] = hist

    # build filter
    filt = {}
    if q:
        rx = {"$regex": _loose_regex(q), "$options": "i"}

        # direct user-field match
        user_or = [{"name": rx}, {"email": rx}, {"username": rx}]

        # song-field match 
        song_or = [{"title": rx}, {"artist": rx}, {"genre": rx}]
        if q.isdigit():
            song_or.append({"year": int(q)})
            song_or.append({"year": q})

        # collect user ids from both user_id and owner_id in songs
        try:
            ids = set()
            ids.update(current_app.db.songs.distinct("user_id", {"$or": song_or}))
            ids.update(current_app.db.songs.distinct("owner_id", {"$or": song_or}))
            ids = [i for i in ids if i]
            if ids:
                user_or.append({"_id": {"$in": ids}})
        except Exception:
            pass

        filt = {"$or": user_or}

    # fetch users 
    users = list(
        current_app.db.users
        .find(filt, {"name": 1, "email": 1, "username": 1})
        .sort("name", 1)
        .limit(100)
    )

    # browse-by-taste 
    try:
        genres = [g for g in current_app.db.songs.distinct("genre") if g][:18]
    except Exception:
        genres = []

    return render_template(
        "home.html",
        q=q,
        history=hist,
        users=users,
        genres=genres,
    )
