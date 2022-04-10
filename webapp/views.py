from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("base.html")


@views.route("/artists")
def artists():
    pass


@views.route("/tracks")
def tracks():
    pass


@views.route("/albums")
def albums():
    pass


@views.route("/playlists")
def playlists():
    pass