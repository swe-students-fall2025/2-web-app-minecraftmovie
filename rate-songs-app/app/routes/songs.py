from flask import Blueprint, render_template, request, current_app
from flask_login import login_required, current_user

songs_bp = Blueprint("songs", __name__)

@songs_bp.route("/songs/all")
@login_required
def all_songs():
    db = current_app.db
    songs_col = db.songs
    uid = current_user.get_id()

    try:
        page = max(1, int(request.args.get("page", "1")))
    except ValueError:
        page = 1
    PER_PAGE = 15
    skip = (page - 1) * PER_PAGE

    #only this user's songs; rating is stored on the song doc itself
    q = {"owner_id": uid}
    items = list(songs_col.find(q).sort("title", 1).skip(skip).limit(PER_PAGE))
    total = songs_col.count_documents(q)
    has_next = total > skip + len(items)

    for s in items:
        s["_id"] = str(s["_id"])

    return render_template(
        "all_songs_paginated.html",
        items=items,
        page=page,
        has_next=has_next,
    )
