"""
@Author:    Leonardo Maben
@Date:      26/10/2024
"""
import pandas as pd
import csv
import SpotifyCredentials as sc
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id= '67d8b05550974151bed3f3593a3526ff',
                                                      client_secret='a213356e2e714bd3aa64a255ac372f96')
# # Manually fetch the token
# try:
#     token = client_credentials_manager.get_access_token(as_dict=False)
#     print("Access Token:", token)
# except Exception as e:
#     print("Error generating token:", e)

# sp = spotipy.Spotify(auth=token)

token = client_credentials_manager.get_access_token(as_dict=False)
print("Access token: ", token)

# Initialize Spotipy with fresh token
sp = spotipy.Spotify(auth=token)

# Request audio features again
track = '03kCR9HZpX5muU7D8xYPOL'
audio_features = sp.audio_features([track])

# Print the audio features
print(audio_features)

csv_filename = "../metadata/audiofeatures.csv"
fieldnames = [
    "acousticness",
    "danceability",
    "energy",
    "instrumentalness",
    "key",
    "liveness",
    "loudness",
    "mode",
    "speechiness",
    "tempo",
    "valence",
]

#file = pd.read_csv('../processed_files/#boostyourrun.csv')
#tracks = file['track_uri']

#track_ids = [uri.split(":")[-1] for uri in tracks]
audio_features_list = sp.audio_features(track)

with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for features in audio_features_list:
        if features:  # Avoid None entries
            writer.writerow({field: features[field] for field in fieldnames})

print(f"Audio features for all tracks saved to {csv_filename}")