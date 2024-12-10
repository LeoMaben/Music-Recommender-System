"""
@Author: Leonardo Maben
@Date: 1/12/24

"""
import os

import numpy
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA


def aggregate_data(folder_path):
    '''
    Function to concatenate the metadata and save it into one file

    :param folder_path: path to the original metadata
    '''

    aggregated_data = []

    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        data = pd.read_csv(path)
        aggregated_data.append(data)

    ad_csv = pd.concat(aggregated_data, ignore_index=True)
    print(ad_csv.head())

    ad_csv.to_csv('aggregated_data.csv', index=False)


def top_songs(dataframe):
    '''
    Plot the top 10 songs
    :param dataframe: Dataframe containing the playlist metadata
    '''
    song_count = dataframe['Track Name'].value_counts().head(10)
    sns.barplot(x=song_count.values, y=song_count.index)
    plt.title('The top 10 most popular songs in playlists are: ')
    plt.show()


def top_artists(dataframe):
    '''
    Plots the top 10 artists
    :param dataframe: Dataframe containing the playlist metadata
    '''
    artist_count = dataframe['Artist Name'].value_counts().head(10)
    sns.barplot(x=artist_count.values, y=artist_count.index)
    plt.title('The top 10 most popular artist in the playlists are:')
    plt.show()

def main():
    # folder_path = '../metadata/'
    playlist_df = pd.read_csv('aggregated_data.csv')

    #top_songs(playlist_df)
    top_artists(playlist_df)

    # aggregate_data(folder_path)


if __name__ == '__main__':
    main()
