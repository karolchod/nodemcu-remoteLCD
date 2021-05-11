import time
import simpleLCD
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#Please enter your Spotify app parameters - refer to Spotipy documentation
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="aaa",
                                               client_secret="aaa",
                                               redirect_uri="https://www.google.com/",
                                               scope="user-read-currently-playing"))

LCD = simpleLCD.SimpleLCD()
resultPrev=None
time.sleep(1)
while True:
    try:
        time.sleep(1)
        track = sp.currently_playing()
        if track is None or track['currently_playing_type']!= 'track' or track['is_playing']==False:
            result = (' ', ' ')
            if result != resultPrev:
                print("Nothing")
                LCD.clear()
                resultPrev = (' ', ' ')
        else:
            result=(track['item']['artists'][0]['name'], track['item']['name'])
            if resultPrev != result and track['is_playing']==True:
                print(result)
                LCD.clear()
                if len(result[0].encode()) <= len(result[1].encode()):
                    LCD.send(0,result[0])
                    LCD.scroll(1, result[1])
                elif len(result[0].encode()) > len(result[1].encode()):
                    LCD.send(1, result[1])
                    LCD.scroll(0, result[0])
                resultPrev = result
    except KeyboardInterrupt:
        LCD.clear()
        # LCD.clock()
        del LCD
        time.sleep(2)
        break
