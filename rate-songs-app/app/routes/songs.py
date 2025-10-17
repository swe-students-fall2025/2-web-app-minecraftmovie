from flask import Blueprint, render_template, request, current_app
from flask_login import login_required, current_user
from bson import ObjectId

songs_bp = Blueprint("songs", __name__)

@songs_bp.route("/songs/all")
@login_required
def all_songs():
    db = current_app.db
    coll_songs = db.songs
    coll_ratings = db.ratings

    uid = current_user.get_id()

    try:
        page = max(1, int(request.args.get("page", "1")))
    except ValueError:
        page = 1
    PER_PAGE = 15
    skip = (page - 1) * PER_PAGE

    #only songs attached to this user
    q = {"owner_id": uid}
    items = list(coll_songs.find(q).sort("title", 1).skip(skip).limit(PER_PAGE))
    total = coll_songs.count_documents(q)
    has_next = total > skip + len(items)

    #looks up this user's ratings for these songs
    ids_str = [str(doc["_id"]) for doc in items]
    user_ratings = {
        r["song_id"]: r["score"]
        for r in coll_ratings.find(
            {"user_id": uid, "song_id": {"$in": ids_str}},
            {"song_id": 1, "score": 1},
        )
    }

    for s in items:
        s["_id"] = str(s["_id"])

    return render_template(
        "all_songs_paginated.html",
        items=items,
        page=page,
        has_next=has_next,
        user_ratings=user_ratings,
    )
