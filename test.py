import base64
import config
import requests


#r = requests.get("https://accounts.spotify.com/authorize?client_id={}&response_type=code&redirect_uri=http://localhost:8888/callback".format(config.client_id))

#print (r.text)
#exit()

body = {"grant_type": "client_credentials"}

#encoded = (config.client_id + ":" + config.client_secret)
encoded = (base64.b64encode((config.client_id + ":" + config.client_secret).encode("utf-8")))

print(encoded)

headers = {"Authorization": "Basic" + encoded}

#print (body)
#print (headers)

r = requests.post("https://accounts.spotify.com/api/token",
                  headers=headers,
                  data=body)

print (r.text)
