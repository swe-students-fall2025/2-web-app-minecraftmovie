# app/routes/home.py

from flask import Blueprint, render_template, request, session, current_app
from bson import ObjectId
import re

home_bp = Blueprint("home", __name__)

def _loose_rx(q: str) -> dict:
    """Case-insensitive"""
    tokens = re.sub(r"[^A-Za-z0-9]+", " ", q, flags=re.I).strip()
    if not tokens:
        return {"$regex": re.escape(q), "$options": "i"}
    pat = r"[^A-Za-z0-9]*".join(map(re.escape, tokens))
    return {"$regex": pat, "$options": "i"}

def _coerce_object_ids(values):
    """Return a list of ObjectId"""
    out = []
    for v in values:
        if isinstance(v, ObjectId):
            out.append(v)
        elif isinstance(v, str) and re.fullmatch(r"[0-9a-fA-F]{24}", v):
            try:
                out.append(ObjectId(v))
            except Exception:
                pass
    return out

@home_bp.route("/")
def home():
    q = request.args.get("q", "").strip()

    # simple history (last 5)
    history = session.get("profile_history", [])
    if q:
        history = [v for v in [q] + history if v][:5]
        session["profile_history"] = history

    # -------- build user filter --------
    filt = {}
    if q:
        rx = _loose_rx(q)

        # direct match on user fields
        user_or = [{"name": rx}, {"username": rx}, {"email": rx}]

        # match songs by title or artist 
        song_or = [{"title": rx}, {"artist": rx}]

        try:
            # collect user ids from both fields present in songs
            ids_raw = set()
            ids_raw.update(current_app.db.songs.distinct("user_id", {"$or": song_or}))
            ids_raw.update(current_app.db.songs.distinct("owner_id", {"$or": song_or}))

            # normalize to ObjectId 
            ids = _coerce_object_ids([i for i in ids_raw if i])

            if ids:
                user_or.append({"_id": {"$in": ids}})
        except Exception:
            # ignore lookup errors
            pass

        filt = {"$or": user_or}

    # fetch users
    users = list(
        current_app.db.users
        .find(filt, {"name": 1, "username": 1, "email": 1})
        .sort("name", 1)
        .limit(100)
    )

    # we removed "browse by taste", so pass nothing for genres
    return render_template(
        "home.html",
        q=q,
        history=history,
        users=users,
        genres=[],
    )
