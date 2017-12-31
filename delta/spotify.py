import spotipy
import json
import requests
import base64
import time, datetime

COMBO = '46434e19c27449fc95505df227e3ee0f:30ff59886cde42d58304cd82437a4c5b'
EXPIRY = 'static/token_expiry.txt'

encoded = base64.b64encode(bytes(COMBO))
data = {
    'grant_type':'client_credentials'
}
headers = {
    'Authorization': 'Basic ' + encoded
}

expiry_content = file(EXPIRY).read()
get_parts = expiry_content.split('$$$')

expiry_timestamp = get_parts[0]
expiry_token = get_parts[1]

prev_timestamp = float(expiry_timestamp)
print "previous token was fetched on: " + datetime.datetime.fromtimestamp(prev_timestamp).strftime('%Y-%m-%d %H:%M:%S')
curr_timestamp = time.time()
if round((3600-(curr_timestamp-prev_timestamp))/60.0, 2) >= 0:
    print "token expires in: " + str(round((3600-(curr_timestamp-prev_timestamp))/60.0, 2))+ " minutes"

if curr_timestamp - prev_timestamp >= 3600:
    print "an hour has passed since last fetch - token has expired..."
    print "getting new token..."

    get = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
    parsed = json.loads(get.content)

    access_token = parsed['access_token']

    print "new token acquired - writing: " + str(curr_timestamp) + '$$$' + access_token

    expiry_file_handle = open(EXPIRY,'w')
    expiry_file_handle.write(str(curr_timestamp)+'-'+access_token)
    expiry_file_handle.close()

else:
    print "the token is still valid - using: " + expiry_token
    access_token = expiry_token


sp = spotipy.Spotify(auth=access_token)
user_query = raw_input("Spotify search: ")
result = sp.album("0U6ldwLBEMkwgfQRY4V6D2")
parsed =  dict(result)
print json.dumps(parsed, indent=4, sort_keys=True)