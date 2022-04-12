# Imports :
from flask import Blueprint, render_template

#Creating the views blueprint
views = Blueprint("views", __name__)


# Creating the navbar ressources (url, title, icon)
navigation = {
            "/artists": ("Artists", "bi bi-person-fill"),
            "/tracks": ("Tracks", "bi bi-disc-fill"),
            "/albums": ("Albums", "bi bi-journal-album"),
            "/playlists": ("Playlists", "bi bi-music-note-list")}

#Routes :
@views.route("/artists")
def artists():
    return render_template("artists.html", nav=navigation)


@views.route("/tracks")
def tracks():
    return render_template("tracks.html", nav=navigation)


@views.route("/albums")
def albums():
    return render_template("albums.html", nav=navigation)


@views.route("/playlists")
def playlists():
    return render_template("playlists.html", nav=navigation)