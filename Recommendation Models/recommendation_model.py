from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from implicit.als import AlternatingLeastSquares
import pandas as pd
import numpy as np

def preprocess_text(text):
    text = text.lower()
    text = text.replace(',', '')
    return text

def content_based_recommendation(data, track_name , artist_name , number_of_recommendations):

    data['combined'] = (data['Track Name'] + ' ' + data['Artist Name']).apply(preprocess_text)
    data['combined'] = data['combined'].dropna()

    # test_data = (data['Track Name'] + ' ' + data['Artist Name'])
    # test_data = test_data.dropna()

    # Calculating the Term Frequency
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data['combined'])

    cos_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

    match = data[(data['Track Name'].str.lower() == track_name.lower()) &
                 (data['Artist Name'].str.lower() == artist_name.lower())]

    # Handle case where song is not found
    if match.empty:
        return "Track not found!"

    song_index = match.index[0]  # Extract integer index

    similarity_score = list(enumerate(cos_similarity[song_index]))
    # similarity_score = cos_similarity[song_index].flatten()  # Convert row to 1D array
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)[1:number_of_recommendations + 1]
    song_indices = [i[0] for i in similarity_score]

    return data.iloc[song_indices][['Track Name', 'Artist Name']]

def collaborative_recommendation(data, playlist_id, number_of_recommendations):

    # Encoding since the track ids are urls
    data['Playlist ID'] = data['Playlist ID'].astype('category').cat.codes
    data['Track ID'] = data['Track Url'].astype('category').cat.codes

    # Creating the sparse matrix
    playlist_matrix = csr_matrix((np.ones(len(data)), (data["Playlist ID"], data["Track ID"])))


    track_mapping = dict(enumerate(data["Track Url"].astype("category").cat.categories))
    track_info_mapping = data.groupby("Track Url").agg({"Track Name": "first", "Artist Name": lambda x: ", ".join(set(x))}).to_dict(orient="index")

    # ALS Model
    model = AlternatingLeastSquares(factors=50, iterations=20)
    model.fit(playlist_matrix)

    if playlist_id not in range(playlist_matrix.shape[0]):
        return "Playlist not found!"

    recommendations = model.recommend(playlist_id, playlist_matrix[playlist_id], N=number_of_recommendations)
    track_ids = [track_mapping.get(i, None) for i in recommendations[0]]
    track_ids = [tid for tid in track_ids if tid is not None]

    recommended_urls = [track_mapping[track_id] for track_id in recommendations[0]]

    return [(track_info_mapping[track]['Track Name'], track_info_mapping[track]['Artist Name']) for track in track_ids if track in track_info_mapping]

def hybrid_recommendation(data, track_name, artist_name, number_recommendations,
                          playlist_id, weight_cbf=0.5, weight_cf=0.5):

    cbf_result = content_based_recommendation(data, track_name, artist_name, number_recommendations)
    if isinstance(cbf_result, str):
        return "Track not found!"

    cf_result = collaborative_recommendation(data, playlist_id, number_recommendations)
    if isinstance(cf_result, str):
        return "Playlist not found!"

    cbf_scores = {row["Track Name"]: 1 - idx / len(cbf_result) for idx, row in cbf_result.iterrows()}
    cf_scores = {track[0]: 1 - idx / len(cf_result) for idx, track in enumerate(cf_result)}

    # Merge and weight scores
    combined_scores = {}
    for track in set(cbf_scores.keys()).union(cf_scores.keys()):
        combined_scores[track] = weight_cbf * cbf_scores.get(track, 0) + weight_cf * cf_scores.get(track, 0)

    # Sort and return top recommendations
    final_recommendations = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:number_recommendations]

    return final_recommendations

def main():

    df = pd.read_csv('../Data Analysis/mini_data.csv')
    # suggestions = content_based_recommendation(df, 'On the Floor', 'Jennifer Lopez' , 10)
    # print(f'Your recommended songs are: \n{suggestions}')
    # collaborative_recommendation(df, 15)
    recomendations = hybrid_recommendation(df, 'On the Floor', 'Jennifer Lopez', 10, 0)
    print(f"Recommendations based on the given choices are: \n")
    print(recomendations)


if __name__ == '__main__':
    main()