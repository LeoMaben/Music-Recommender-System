"""
@Author:    Leonardo Maben
@Date:      26/10/2024
"""

import os
import pandas as pd
import json
import re


def check_playlist_name(playlist_name):
    """
    Helper function to check for special symbols in the playlist name and replace it with '_'
    This is to avoid errors while creating .csv files for the specific playlists while checking for music metadata

    :param   playlist_name:     String containing the name of the playlist
    :return: new_playlist_name: String containing the new name of the playlist
    """

    new_playlist_name = re.sub(r'[<>:"/\\|?*]', '_', playlist_name)
    return new_playlist_name


def read_json(file_path):
    """
    Function to read the json files and save them in the .csv format for extracting metadata on songs
    """

    try:
        file = open(file_path)
        data = json.load(file)
        folder_path = '../processed_files'

        playlists = data['playlists']
        i = 0

        for playlist in playlists:

            # print(i)
            # i += 1
            name = playlist['name']
            tracks = pd.DataFrame(playlist['tracks'])
            tracks = tracks.drop(columns='pos')
            name = check_playlist_name(name)
            file = name + '.csv'

            file_path = os.path.join(folder_path, file)
            if os.path.exists(file_path):
                tracks.to_csv(file_path, mode='a', index=False, header=False)
            else:
                # print(file_path) # Quick check to see if file paths already exist or not
                tracks.to_csv(file_path, index=False)

    except FileNotFoundError:
        print(f"{file_path} does not exist")
    except json.JSONDecodeError as e:
        print(f"Error with json file: {e}")
    except Exception as e:
        print(f"Following error got triggered: {e}")



def reconstruct_data(file_path, output_path):
    start = 0
    end = 1000


    while end != 11000:
        path = file_path + 'mpd.slice.' + str(start) + '-' + str(end - 1) + '.json'
        data = json.load(open(path))
        song_array = []
        for playlist in data['playlists']:
            pid = playlist['pid']
            for tracks in playlist['tracks']:

                artist_name = tracks['artist_name']
                track_uri = tracks['track_uri']
                track_name = tracks["track_name"]

                song_array.append([track_uri, track_name, artist_name, pid])

        song_playlist = pd.DataFrame(song_array, columns=['Track Url', 'Track Name', 'Artist Name', 'Playlist ID'])
        print("Dataframe loaded")
        song_playlist.to_csv(output_path + 'mpd.slice.' + str(start) + '-' + str(end - 1) + '.csv', index=False)
        print("CSV written")
        start += 1000
        end += 1000



def main():
    file_path = "../../SpotifyChallenge/million_dataset/data/"
    output_path = '../metadata/'
    # read_json(file_path)
    reconstruct_data(file_path, output_path)


if __name__ == '__main__':
    main()