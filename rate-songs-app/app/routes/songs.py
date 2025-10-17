from flask import Blueprint, render_template, request, current_app

songs_bp = Blueprint("songs", __name__)

@songs_bp.route("/songs/all")
def all_songs():
    # Prefer the db handle attached in app/__init__.py
    db = getattr(current_app, "db", None)
    if db is None:
        # Fallback if someone imports mongo_db directly elsewhere
        from app import mongo_db as db

    coll = db.songs

    # pagination (15 per page)
    try:
        page = max(1, int(request.args.get("page", "1")))
    except ValueError:
        page = 1
    PER_PAGE = 15
    skip = (page - 1) * PER_PAGE

    items = list(coll.find().sort("title", 1).skip(skip).limit(PER_PAGE))
    has_next = coll.count_documents({}) > skip + len(items)

    # Stringify _id for safe templating/links
    for s in items:
        s["_id"] = str(s["_id"])

    return render_template(
        "all_songs_paginated.html",
        items=items,
        page=page,
        has_next=has_next,
    )

