import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

cid = '4a07e98721c84fcab2458d5813965796'
secret = '9fc833bbc4a647c8b56ddb3e952d04b4'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


result = sp.search('monster', limit=5, market='KR')
pprint.pprint(result)