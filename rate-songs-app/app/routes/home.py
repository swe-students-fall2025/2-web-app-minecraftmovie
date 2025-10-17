# app/routes/home.py

# import
from flask import Blueprint, render_template, request, current_app, session

# bp
home_bp = Blueprint("home", __name__)

# route
@home_bp.get("/", endpoint="home")
def home_view():
    # query
    q = (request.args.get("q") or "").strip()
    y1 = (request.args.get("y1") or "").strip()
    y2 = (request.args.get("y2") or "").strip()

    # history
    if q:
        hist = session.get("history", [])
        if q not in hist:
            hist = ([q] + hist)[:6]
        session["history"] = hist
    history = session.get("history", [])

    # filter
    filt = {}
    if q:
        rx = {"$regex": q, "$options": "i"}
        ors = [{"title": rx}, {"artist": rx}, {"genre": rx}]
        if q.isdigit():
            ors.append({"year": int(q)})
        filt["$or"] = ors
    yr = {}
    if y1.isdigit():
        yr["$gte"] = int(y1)
    if y2.isdigit():
        yr["$lte"] = int(y2)
    if yr:
        filt["year"] = yr if "year" not in filt else {**filt["year"], **yr}

    # find
    songs = list(current_app.db.songs.find(filt).sort("title", 1).limit(100))

    # genres
    try:
        genres = [g for g in current_app.db.songs.distinct("genre") if g][:6]
    except Exception:
        genres = []

    # render
    return render_template(
        "home.html",
        page_title_text="Rate Songs",
        songs=songs,
        q=q,
        y1=y1,
        y2=y2,
        history=history,
        genres=genres,
    )
