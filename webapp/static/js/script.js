function hideTracks() {
    const hide = "hidden"
    const disable = "disabled"
    const albums = document.getElementById("top-albums")
    const tracks = document.getElementById("top-tracks")
    const btn_albums = document.getElementById("btn-top-albums")
    const btn_tracks = document.getElementById("btn-top-tracks")

    if (albums.classList.value.split(" ").includes(hide)){
        tracks.classList.add(hide)
        albums.classList.remove(hide)
        btn_tracks.classList.remove(disable)
        btn_albums.classList.add(disable)
    }
}
function hideAlbums() {
    const hide = "hidden"
    const disable = "disabled"
    const albums = document.getElementById("top-albums")
    const tracks = document.getElementById("top-tracks")
    const btn_albums = document.getElementById("btn-top-albums")
    const btn_tracks = document.getElementById("btn-top-tracks")

    if (tracks.classList.value.split(" ").includes(hide)){
        tracks.classList.remove(hide)
        albums.classList.add(hide)
        btn_tracks.classList.add(disable)
        btn_albums.classList.remove(disable)
    }
}

function like(btn, track_id, user_id, artist_id){
    const liked = "bi-heart-fill"
    const unliked = "bi-heart"
    if (artist_id){
        const url = "/artists?id="+artist_id
    } else {
        const url = "/track?id="+track_id
    }
    if (user_id){
        if (btn.classList.value.split(" ").includes(unliked)){
            btn.classList.remove(unliked)
            btn.classList.add(liked)
            fetch("/like-song", {
                method: "POST",
                body: JSON.stringify({ track_id: track_id})
            }).then((_res) => {
                window.location.href = url;
            });
        }else{
            btn.classList.remove(liked)
            btn.classList.add(unliked)
            fetch("/unlike-song", {
                method: "POST",
                body: JSON.stringify({ track_id: track_id})
            }).then((_res) => {
                window.location.href = url;
            });

        }
    }
}
function addToPlaylist(btn, track_id, user_id, artist_id){
    const added = "bi-check-circle-fill"
    const not_added = "bi-plus-circle"
    if (artist_id){
        const url = "/artists?id="+artist_id
    } else {
        const url = "/tracks?id="+track_id
    }
    const form_wraper = document.getElementById("playlist-form")
    const track_input = document.getElementById("track-id")

    if (user_id){
        if (btn.classList.value.split(" ").includes(not_added)){
            btn.classList.remove(not_added)
            btn.classList.add(added)
            form_wraper.classList.remove("hidden")
            track_input.value = track_id
        }else{
            btn.classList.remove(added)
            btn.classList.add(not_added)
            fetch("/remove-song", {
                method: "POST",
                body: JSON.stringify({track_id: track_id})
            }).then((_res) => {
                window.location.href = url;
            })
        }
    }
}

function play(btn, track_id){
    const audio_player = document.getElementById(track_id)
    const hide = "hidden"
    const play_btn = "bi-circle-play"
    const stop_btn = "bi-stop-circle"

    if (audio_player.classList.value.split(" ").includes(hide)){
        audio_player.classList.remove(hide)
        btn.classList.remove(play_btn)
        btn.classList.add(stop_btn)
        
    }
    else {
        audio_player.classList.add(hide)
        btn.classList.remove(stop_btn)
        btn.classList.add(play_btn)
    }
}