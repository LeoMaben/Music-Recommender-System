#  Music Recommendation System

Welcome to my **Music Recommendation System**, an exciting journey into **recommender system development** using real-world data from the **Spotify Million Playlist Dataset** (~33GB). This project explores **content-based filtering, collaborative filtering (ALS, k-NN), and hybrid approaches** to enhance recommendation accuracy. 

## Features

- **Content-Based Filtering**: Utilizes **TF-IDF and cosine similarity** to recommend tracks based on song features.
- **Collaborative Filtering (ALS)**: Implements **Alternating Least Squares (ALS)** matrix factorization to recommend tracks based on user interactions.
- **k-NN Collaborative Filtering**: Applies **k-nearest neighbors (k-NN) with cosine similarity** for playlist similarity.
- **Hybrid Approach (WIP)**: Combining content-based and collaborative filtering to optimize recommendations.
- **Efficient Data Processing**: Handles large-scale data efficiently with optimized transformations.

##  Steps:

### **1) Data Processing**
- **Cleaning & Preprocessing**: Transforming raw playlist data into a structured format.
- **Sparse Matrix Construction**: Representing user-playlist interactions for collaborative filtering.
- **Feature Extraction**: Using **TF-IDF vectorization** for track metadata.

### **2) Recommendation Models**
#### ** Content-Based Filtering (TF-IDF + Cosine Similarity)**
- Extracts song features (e.g., track name, artist, genre).
- Uses **TF-IDF vectorization** to represent text-based features.
- Measures similarity between tracks using **cosine similarity**.

#### ** Collaborative Filtering (ALS & k-NN)**
- **ALS Matrix Factorization** to predict missing interactions.
- **k-NN (Cosine Similarity)** for playlist similarity-based recommendations.

#### ** Hybrid Approach (WIP)**
- Integrating both **content-based and collaborative filtering** for better accuracy.
- Experimenting with weighted scores to balance different recommendation strategies.


##  Next Steps
-  **Improve Model Performance**: Fine-tune ALS hyperparameters & TF-IDF weights.
-  **Implement Hybrid Model**: Combine collaborative & content-based filtering.
-  **Expand Feature Engineering**: Incorporate audio features (e.g., tempo, key, energy levels).
-  **Evaluation Metrics**: Implement precision@k, recall@k, and hit rate evaluation.

##  Learnings & Challenges
- Managing **large-scale datasets** efficiently.
- Handling **sparse matrices** for collaborative filtering.
- Experimenting with **different recommendation techniques** for better accuracy