#  Music Recommendation System

Welcome to my **Music Recommendation System**, an exciting journey into **recommender system development** using real-world data from the **Spotify Million Playlist Dataset** (~33GB). This project explores **content-based filtering, collaborative filtering (ALS, k-NN), and hybrid approaches** to enhance recommendation accuracy. 

## Features

- **Content-Based Filtering**: Utilizes **TF-IDF and cosine similarity** to recommend tracks based on song features.
- **Collaborative Filtering (ALS)**: Implements **Alternating Least Squares (ALS)** matrix factorization to recommend tracks based on user interactions.
- **Hybrid Approach (WIP)**: Combining content-based and collaborative filtering to optimize recommendations.
- **Efficient Data Processing**: Handles large-scale data efficiently with **pyspark** and optimized transformations.

##  Implementation Details:

### **1) Data Processing**
- **Cleaning & Preprocessing**: Transforming raw playlist data into a structured format.
- **Sparse Matrix Construction**: Representing user-playlist interactions for collaborative filtering.
- Converts categorical **track IDs and playlist IDs** into numerical representations.  
- Preprocesses song metadata for **TF-IDF vectorization**.  

### **2) Recommendation Models**
#### **Content-Based Filtering (TF-IDF + Cosine Similarity)**
- Extracts song features (e.g., track name, artist, genre).
- Uses **TF-IDF vectorization** to represent text-based features.
- Measures similarity between tracks using **cosine similarity**.

#### **Collaborative Filtering (ALS & k-NN)**
- Encodes playlists and tracks into a **sparse matrix representation**.  
- Trains an **ALS model** from the implicit library to predict song preferences.  

#### **Hybrid Approach (WIP)**
- **Merges content-based & collaborative filtering results** to provide balanced recommendations.  
- Uses **weighted scoring** to combine similarity rankings.

##  Learnings & Challenges
- **Efficient processing of large-scale music data** (~33GB).  
- **Sparse matrix construction & optimization** for collaborative filtering.  
- **Combining multiple recommendation techniques** to enhance accuracy.  