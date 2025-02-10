from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from implicit.als import AlternatingLeastSquares
import pandas as pd
import numpy as np


def sliding_window_cos_similarity(matrix, sliding_amount):
    n = matrix.shape[0]
    cos_similarity = np.zeros((n,n))
    for start in range(0, n, sliding_amount):
        end = min(start + sliding_amount, n)
        cos_similarity[start:end] = cosine_similarity(matrix[start:end], matrix)

    return cos_similarity

def content_based_recommendation(data, track_name , artist_name , number_of_recommendations):

    print('Starting the function\n')
    test_data = (data['Track Name'] + ' ' + data['Artist Name'])
    print('Data has been combined\n')
    test_data = test_data.dropna()

    # Calculating the Term Frequency
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(test_data)
    print('TF-IDF Matrix has been calculated')

    # Convert the sparse matrix to a dense DataFrame for readability
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(),
        columns=vectorizer.get_feature_names_out()
    )

    #print(tfidf_df)

    # Calculating the cosine similarity
    cos_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
    print('Calculated the cosine similarity')

    song_index = data[(data['Track Name'].str.lower() == track_name.lower()) |
                      (data['Artist Name'].str.lower() == artist_name.lower())].index

    # Handle case where song is not found
    if song_index.empty:
        print(f"Error: The track '{track_name}' was not found in the dataset.")
        return pd.DataFrame(columns=['Track Name', 'Artist Name'])

    song_index = song_index[0]  # Extract integer index

    similarity_score = cos_similarity[song_index].flatten()  # Convert row to 1D array
    similarity_score = list(enumerate(similarity_score))

    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)[1:]

    # Get recommendations
    unique_songs = []
    seen_tracks = set()

    for idx, score in similarity_score:
        track, artist = data.iloc[idx][['Track Name', 'Artist Name']]

        if (track, artist) not in seen_tracks:
            seen_tracks.add((track, artist))
            unique_songs.append((idx, score))

        if len(unique_songs) >= number_of_recommendations:
            break


    song_indices = [i[0] for i in unique_songs]
    return data.iloc[song_indices][['Track Name', 'Artist Name']]


def collaborative_recommendation(data, playlist_id):


    # Encoding since the track ids are urls
    data['Playlist ID'] = data['Playlist ID'].astype('category').cat.codes
    data['Track ID'] = data['Track Url'].astype('category').cat.codes

    # Creating the sparse matrix
    playlist_matrix = csr_matrix((np.ones(len(data)), (data["Playlist ID"], data["Track ID"])))

    # Group by "Track Url", keeping the first track name and joining artist names
    data_grouped = data.groupby("Track Url").agg({
        "Track Name": "first",  # Take the first track name
        "Artist Name": lambda x: ", ".join(set(x))  # Combine artist names
    }).reset_index()

    # Create the mapping
    track_info_mapping = data_grouped.set_index("Track Url")[["Track Name", "Artist Name"]].to_dict(orient="index")

    print(f"Matrix shape: {playlist_matrix.shape}")

    # ALS Model
    model = AlternatingLeastSquares(factors=50, iterations=20)
    model.fit(playlist_matrix)

    recommendations = model.recommend(playlist_id, playlist_matrix[playlist_id])
    # print(recommendations)

    track_ids = recommendations[0]

    track_mapping = dict(enumerate(data["Track Url"].astype("category").cat.categories))
    recommended_urls = [track_mapping[track_id] for track_id in track_ids]

    recommended_tracks = [(track_info_mapping[url]['Track Name'], track_info_mapping[url]['Artist Name']) for url in recommended_urls if url in track_info_mapping]

    print(f"Recommended Tracks: {recommended_tracks}")


def main():

    df = pd.read_csv('../Data Analysis/mini_data.csv')
    # suggestions = content_based_recommendation(df, 'On the Floor', 'Jennifer Lopez' , 10)
    # print(f'Your recommended songs are: \n{suggestions}')
    collaborative_recommendation(df, 15)


if __name__ == '__main__':
    main()