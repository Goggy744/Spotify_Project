from . import db
from flask_login import UserMixin

class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True)
    password = db.Column(db.String(24), unique=False)
    Likes = db.relationship("LikedSong")
    Playlists = db.relationship("Playlist")


class LikedSong (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, unique=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    tracks = db.relationship("Track")


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, unique=False)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.id"))