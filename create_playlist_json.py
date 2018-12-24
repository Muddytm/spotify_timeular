import config
import spotipy
import spotipy.util as util
import time


with open("playlists.txt") as f:
    pls = [line.strip() for line in f]

scope = "user-read-playback-state"

token = util.prompt_for_user_token(config.username, scope, config.spotify_id, config.spotify_secret, "http://localhost:8888/callback")

if token:
    sp = spotipy.Spotify(auth=token)

    playlists = sp.user_playlists(username)

    playlist_info = {}

    for playlist in playlists["items"]:
        if playlist["name"] in pls:
            playlist_info[playlist["name"]] = "spotify:user:{}:playlist:{}".format(username, playlist["id"])

    print (playlist_info)
else:
    print ("Can't get token for" + username)
