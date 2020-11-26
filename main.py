import spotipy
from spotipy.oauth2 import SpotifyOAuth
from os import environ
import json

# Needs to be removed lol
"""
SET SPOTIPY_CLIENT_ID='0395ebe9ec5f4eee9d86aad2edd60340'
SET SPOTIPY_CLIENT_SECRET='699fbeb75cb943759f6bf7485921e06b'
SET SPOTIPY_REDIRECT_URI='http://localhost'
"""

# Imported from enviroment
SPOTIPY_CLIENT_ID = environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = "http://localhost8080"

# Cache location for token
APPDATA = environ["APPDATA"]
CACHE = APPDATA + "\spotifyapp"

# oAuth process
scope = "user-read-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET ,redirect_uri=SPOTIPY_REDIRECT_URI,scope=scope, show_dialog=True, cache_path=CACHE))




# get current logged in available devices data
def get_device_data():
    device_data = sp.devices()
    device_list = device_data["devices"]

    # parses device data to readable
    print("Geräteübersicht:")
    print(json.dumps(device_list, indent=4, sort_keys=True))

    # Create a list of available devices
    counter = 0
    device_name_list = list()
    for device in device_list:
        device_name = device["name"]
        device_name_list.append(device_name)
    print(device_name_list)

# gets user information (use sp.me() for current)
def  get_user_id():
    user_data = sp.me()
    return user_data["id"]

# returns bpm
def get_song_bpm(song_id):
    song_data_packed = sp.audio_features(song_id)
    song_data = song_data_packed[0]
    return song_data["tempo"]



def main():
    user_id = get_user_id()
    get_device_data()


    # get list of playlist id
    user_playlists = sp.current_user_playlists(limit=50)
    item_list = user_playlists["items"]

    counter = 0
    playlist_id_list = list()
    for item in item_list:
        playlist_id = item["id"]
        playlist_id_list.append(playlist_id)


    # playlist selector
    print("Zu welcher playlist möchtest du infos?")

    counter = 1
    for item in item_list:
        print(f"{counter}. {item['name']}")
        counter += 1

    playlist_index = int(input("Gib eine Zahl ein:")) - 1
    selected_playlist_id = playlist_id_list[playlist_index]


    # retrieve list of song ids for specified playlist
    playlist_data = sp.playlist(selected_playlist_id)
    tracks = playlist_data["tracks"]
    items = tracks["items"]

    song_id_list = list()
    counter = 0
    for item in items:
        song_info = item["track"]
        song_id_list.append(song_info["id"])
        counter += 1

    # retrieve list of song names
    song_name_list = list()
    counter = 0
    for item in items:
        song_info = item["track"]
        song_name_list.append(song_info["name"])
        counter += 1


    # create an output dict
    output_dict = dict()
    counter = 0
    for song_id in song_id_list:
        bpm = get_song_bpm(song_id)
        song_name = song_name_list[counter]
        counter +=1

        output_dict[song_name] = bpm

    print(json.dumps(output_dict, indent=4))

    """audio_data = sp.audio_analysis(song_id)
    print(audio_data)
    print(json.dumps(audio_data, indent=4))"""





main()











