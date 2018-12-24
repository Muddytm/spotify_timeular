import config
import spotipy
import spotipy.util as util
import time

scope = "user-read-playback-state"

token = util.prompt_for_user_token(config.username, scope, config.spotify_id, config.spotify_secret, "http://localhost:8888/callback")

if token:
    sp = spotipy.Spotify(auth=token)

    print (sp.devices())
else:
    print ("Can't get token for" + username)
