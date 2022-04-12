from . import db
from flask_login import UserMixin

class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True)
    password = db.Column(db.String(24), unique=False)
    playlists = db.relationship('Playlist')


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    musics = db.relationship('Music')


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False)
    artist = db.Column(db.String(50), unique=False)
    album = db.Column(db.String(50), unique=False)
    like = db.Column(db.Integer, unique=False)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))