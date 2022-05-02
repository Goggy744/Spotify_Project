# Imports :
from threading import currentThread
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .static import deezer
import json
from . import db
from .models import LikedSong, Playlist, Track

# Functions :
def search_artist(client, input):
    """
    Function that return 5 artists.
    :param client: The deezer API Client 
    :param input: the artist name
    :return: a list of 5 artists sorted by their fames
    """
    # Create the request
    request = tuple(client.search_artists(input))
    # Creating a dictonnary that will take the number of fans as key and artist'name as value
    dict = {}
    # Creating a list that will take the number of fans of each artist
    nb_fans_liste = []
    # Creating a list that will take the result
    resultat = []
    # Looping inside the request => updating the dictionnary + append the number of fans in the list
    for artist in request:
        dict.update({artist.nb_fan:artist})
        nb_fans_liste.append(artist.nb_fan)

    # Sorting the list with the reverse parameters switch on
    nb_fans_liste.sort(reverse=True)
    # Append the 3 most famous artists in the result's list
    resultat.append(dict[nb_fans_liste[0]])
    i = 1
    while i < len(nb_fans_liste):
        value = dict[nb_fans_liste[i]]
        i += 1
        if resultat[0].name not in value.name:
            resultat.append(value)
        
    return resultat[:3]




#MAIN PROGRAM#


#Creating the views blueprint
views = Blueprint("views", __name__)


# Creating the navbar ressources (url, title, icon)
nav_guest = {
            "/artists": ("Artists", "bi bi-person-fill"),
            "/tracks": ("Tracks", "bi bi-disc-fill"),
            "/albums": ("Albums", "bi bi-journal-album")
}
nav_user = {
            "/artists": ("Artists", "bi bi-person-fill"),
            "/tracks": ("Tracks", "bi bi-disc-fill"),
            "/albums": ("Albums", "bi bi-journal-album"),
            "/playlists": ("Playlists", "bi bi-music-note-list"),
            "/logout": ("Logout", "bi bi-box-arrow-left")}


#Routes :
@views.route("/artists", methods=["POST", "GET"])
@login_required
def artists():
    client = deezer.Client()
    userLikedSong = []
    userPlaylistTrack = []
    for like in LikedSong.query.filter_by(account_id=current_user.id).all():
        userLikedSong.append(int(like.track_id))
    for playlist in Playlist.query.filter_by(account_id=current_user.id).all():
        for track in Track.query.filter_by(playlist_id=playlist.id).all():
            userPlaylistTrack.append(int(track.track_id)) 
    if request.args:
        arg = tuple(request.args.keys())[0]
        if arg == "artist":
            input = request.args.get(arg)
            if input == "":
                flash("Input field must not be empty", category="error")
                return render_template("artists.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, result=None)
            else:
                result = search_artist(client, input)
                return render_template("artists.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, result=result)
        elif arg == "id":
            input = request.args.get(arg)
            result = client.get_artist(int(input))
            return render_template("artists.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, result=result, client=client, likedSong=userLikedSong, userPlaylistTrack=userPlaylistTrack)
    else:
        return render_template("artists.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, result=None)


@views.route("/tracks")
@login_required
def tracks():
    userLikedSong = []
    userPlaylistTrack = []
    for like in LikedSong.query.filter_by(account_id=current_user.id).all():
        userLikedSong.append(int(like.track_id))
    for playlist in Playlist.query.filter_by(account_id=current_user.id).all():
        for track in Track.query.filter_by(playlist_id=playlist.id).all():
            userPlaylistTrack.append(int(track.track_id)) 
    client = deezer.Client()
    if request.args:
        arg = tuple(request.args.keys())[0]
        if arg == "track":
            input = request.args.get(arg)
            if input == "":
                flash("Input field must not be empty", category="error")
                return render_template("tracks.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, result=None)
            else:
                raw_result = client.search(input)
                dict = {}
                rank_list = []
                result = []
                for track in raw_result:
                    dict.update({track.rank: track})
                    rank_list.append(track.rank)
                if len(rank_list) == 0:
                    flash("Sorry but no tracks matches your research", category="error")
                    return render_template("tracks.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, result=None)
                else:
                    rank_list.sort(reverse=True)
                    for i in range(3):
                        result.append(dict[rank_list[i]])
                    return render_template("tracks.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, result=result)
        else:
            input = request.args.get(arg)
            result = client.get_track(int(input))
            return render_template("tracks.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, result=result, likedSong=userLikedSong, userPlaylistTrack=userPlaylistTrack)

    else:
        return render_template("tracks.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, result=None)


@views.route("/albums")
@login_required
def albums():
    client = deezer.Client()
    if request.args:
        arg = tuple(request.args.keys())[0]
        if arg == "album":
            input = request.args.get(arg)
            if input == "":
                flash("Input shoud not be empty !", category="error")
                return render_template("albums.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
            else:
                raw_result = tuple(client.search(album=input))
                dict = {}
                rank_list = []
                for track in raw_result:
                    dict.update({track.rank: track})
                    rank_list.append(track.rank)
                if len(rank_list) == 0:
                    flash("Sorry but no albums matches your research", category="error")
                    return render_template("albums.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
                else:
                    rank_list.sort(reverse=True)
                    result = dict[rank_list[0]].get_album()
                    return render_template("albums.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, result=result)
    else:
        return render_template("albums.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)


@views.route("/playlists")
@login_required
def playlists():
    playlists = Playlist.query.filter_by(account_id=current_user.id).all()
    return render_template("playlists.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, playlists=playlists, playlist=None)


@views.route("/playlists/<playlist_name>")
@login_required
def playlist(playlist_name):
    client = deezer.Client()
    playlists = Playlist.query.filter_by(account_id=current_user.id).all()
    playlist = Playlist.query.filter_by(account_id=current_user.id, name=playlist_name).first()
    tracks = Track.query.filter_by(playlist_id=playlist.id).all()
    if playlist:
        return render_template("playlists.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, playlists=playlists, tracks=tracks, client=client)


@views.route("/like-song", methods=["POST"])
@login_required
def like_song():
    data = json.loads(request.data)
    track_id = data['track_id']
    new_like = LikedSong(track_id=track_id, account_id=current_user.id)
    db.session.add(new_like)
    db.session.commit()
    return jsonify({})


@views.route("/unlike-song", methods=["POST"])
@login_required
def unlike_song():
    data = json.loads(request.data)
    track_id = data['track_id']
    for like in LikedSong.query.filter_by(account_id=current_user.id).all():
        if like.track_id == track_id:
            db.session.delete(like)
            db.session.commit()
            return jsonify({})


@views.route("/add-song", methods=["POST"])
@login_required
def add_song():
    track_id = request.form.get("track")
    playlist_name = request.form.get("playlist-title")
    user_id = int(request.form.get("user"))
    artist_url = request.form.get("artist_url")
    track_url = request.form.get("track_url")
    
    if artist_url == "":
        url = f"/tracks?id={int(track_url)}"
    else:
        url = f"/artists?id={int(artist_url)}"
    
    if user_id == current_user.id:
        existing_playlist = Playlist.query.filter_by(account_id=current_user.id, name=playlist_name).first()
        if existing_playlist:
            new_track = Track(track_id=track_id, playlist_id=existing_playlist.id)
            db.session.add(new_track)
            db.session.commit()
            return redirect(url)
        else:
            new_playlist = Playlist(name=playlist_name, account_id=user_id)
            db.session.add(new_playlist)
            db.session.commit()
            playlist = Playlist.query.filter_by(name=playlist_name).first()
            new_track = Track(track_id=track_id, playlist_id=playlist.id)
            db.session.add(new_track)
            db.session.commit()
            return redirect(url)
    else:
        return redirect(url)

@views.route("/remove-song", methods=["POST"])
@login_required
def remove_song():
    data = json.loads(request.data)
    track_id = data["track_id"]

    for playlist in Playlist.query.filter_by(account_id=current_user.id).all():
        for track in Track.query.filter_by(playlist_id=playlist.id).all():
            if track.track_id == track_id:
                db.session.delete(track)
                db.session.commit()
                return jsonify({})
        

@views.route("/privacy")
def privacy():
    return render_template("privacy.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)


@views.route("/donates", methods=["POST", "GET"])
@login_required
def donates():
    if request.method == "POST":
        lname = request.form.get("lname")
        fname = request.form.get("fname")
        email = request.form.get("email")
        city = request.form.get("city")
        creditCard = request.form.get("credit-card")
        zip = request.form.get("zip")
        donation = request.form.get("donation")
        checked = request.form.get("checkbox")

        if lname == "":
            flash("You must provide a last name", category="error")
            return render_template("donates.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
        if fname == "":
                    flash("You must provide a first name", category="error")
                    return render_template("donates.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
        if email == "":
                    flash("You must provide an email", category="error")
                    return render_template("donates.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
        if city == "":
                    flash("You must provide a city", category="error")
                    return render_template("donates.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
        if creditCard == "":
                    flash("You must provide a creditCard", category="error")
                    return render_template("donates.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
        if zip == "":
                    flash("You must provide a zip", category="error")
                    return render_template("donates.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)

        if donation == "":
                    flash("You must provide an amount of money", category="error")
                    return render_template("donates.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
        if checked == "":
                    flash("You must check the agreement", category="error")
                    return render_template("donates.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
        flash("Your donation has been well received", category="success")
        return redirect(url_for("auth.home"))
    else:
        return render_template("donates.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)


@views.route("/contacts")
def contacts():
    return render_template("contacts.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
