# Imports :
import re
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
import deezer


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


# Creating the client object
client = deezer.Client()


#Routes :
@views.route("/artists", methods=["POST", "GET"])
def artists():
    if request.method == "POST":
        input = request.form.get("artist")
        print(input, input.isdigit())
        if not input.isdigit():
            list_result = search_artist(client, input)
            single_result = None
            return render_template("artists.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, l_result=list_result, s_result=single_result)
        else:
            list_result = None
            single_result = client.get_artist(int(input))
            return render_template("artists.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, l_result=list_result, s_result=single_result)
    else:
        list_result = None
        single_result = None
        return render_template("artists.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user, l_result=list_result, s_result=single_result)


@views.route("/tracks")
def tracks():
    return render_template("tracks.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)


@views.route("/albums")
def albums():
    return render_template("albums.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)


@views.route("/playlists")
@login_required
def playlists():
    return render_template("playlists.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)