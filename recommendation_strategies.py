import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.neighbors import NearestNeighbors
import random

class RecommendationStrategies:
    """Collection of different recommendation strategies for A/B testing"""
    
    def __init__(self, df, audio_features):
        self.df = df
        self.audio_features = audio_features
        self.scaler = StandardScaler()
        self.feature_data = self.scaler.fit_transform(df[audio_features])
        
    def strategy_1_cosine_similarity(self, preferences, top_n=10):
        """Original cosine similarity strategy"""
        scaled_pref = self.scaler.transform([preferences])
        sims = cosine_similarity(scaled_pref, self.feature_data)[0]
        top_indices = np.argsort(sims)[::-1][:top_n]
        results = self.df.iloc[top_indices][['track_name', 'track_artist', 'playlist_genre']].copy()
        results['similarity'] = sims[top_indices]
        results['strategy'] = 'Cosine Similarity'
        return results
    
    def strategy_2_euclidean_distance(self, preferences, top_n=10):
        """Euclidean distance-based strategy"""
        scaled_pref = self.scaler.transform([preferences])
        distances = euclidean_distances(scaled_pref, self.feature_data)[0]
        top_indices = np.argsort(distances)[:top_n]  # Lower distance = better
        results = self.df.iloc[top_indices][['track_name', 'track_artist', 'playlist_genre']].copy()
        results['similarity'] = 1 / (1 + distances[top_indices])  # Convert to similarity score
        results['strategy'] = 'Euclidean Distance'
        return results
    
    def strategy_3_weighted_features(self, preferences, top_n=10):
        """Weighted feature strategy - emphasizes energy and danceability"""
        weights = np.array([1.5, 1.5, 0.8, 0.8, 0.8, 0.8, 1.0, 1.0, 0.8, 1.2, 1.0, 0.8])
        weighted_pref = np.array(preferences) * weights
        weighted_data = self.feature_data * weights
        
        scaled_pref = self.scaler.transform([weighted_pref])
        sims = cosine_similarity(scaled_pref, weighted_data)[0]
        top_indices = np.argsort(sims)[::-1][:top_n]
        results = self.df.iloc[top_indices][['track_name', 'track_artist', 'playlist_genre']].copy()
        results['similarity'] = sims[top_indices]
        results['strategy'] = 'Weighted Features'
        return results
    
    def strategy_4_popularity_boost(self, preferences, top_n=10):
        """Combines similarity with popularity boost"""
        scaled_pref = self.scaler.transform([preferences])
        sims = cosine_similarity(scaled_pref, self.feature_data)[0]
        
        # Normalize popularity to 0-1 range
        popularity_norm = (self.df['track_popularity'] - self.df['track_popularity'].min()) / \
                         (self.df['track_popularity'].max() - self.df['track_popularity'].min())
        
        # Combine similarity (70%) with popularity (30%)
        combined_score = 0.7 * sims + 0.3 * popularity_norm
        top_indices = np.argsort(combined_score)[::-1][:top_n]
        
        results = self.df.iloc[top_indices][['track_name', 'track_artist', 'playlist_genre']].copy()
        results['similarity'] = combined_score[top_indices]
        results['strategy'] = 'Popularity Boost'
        return results
    
    def strategy_5_genre_aware(self, preferences, top_n=10):
        """Genre-aware strategy that considers genre diversity"""
        scaled_pref = self.scaler.transform([preferences])
        sims = cosine_similarity(scaled_pref, self.feature_data)[0]
        
        # Get top candidates
        top_candidates = np.argsort(sims)[::-1][:top_n*3]  # Get more candidates
        
        # Select diverse genres
        selected_indices = []
        genres_seen = set()
        
        for idx in top_candidates:
            genre = self.df.iloc[idx]['playlist_genre']
            if len(selected_indices) < top_n and (genre not in genres_seen or len(genres_seen) >= 3):
                selected_indices.append(idx)
                genres_seen.add(genre)
        
        # Fill remaining slots with best similarity
        for idx in top_candidates:
            if len(selected_indices) < top_n and idx not in selected_indices:
                selected_indices.append(idx)
        
        results = self.df.iloc[selected_indices][['track_name', 'track_artist', 'playlist_genre']].copy()
        results['similarity'] = sims[selected_indices]
        results['strategy'] = 'Genre Aware'
        return results
    
    def strategy_6_knn_based(self, preferences, top_n=10):
        """K-Nearest Neighbors based strategy"""
        nn = NearestNeighbors(n_neighbors=top_n, metric='cosine')
        nn.fit(self.feature_data)
        
        scaled_pref = self.scaler.transform([preferences])
        distances, indices = nn.kneighbors(scaled_pref)
        
        results = self.df.iloc[indices[0]][['track_name', 'track_artist', 'playlist_genre']].copy()
        results['similarity'] = 1 - distances[0]  # Convert distance to similarity
        results['strategy'] = 'KNN Based'
        return results
    
    def strategy_7_random_baseline(self, preferences, top_n=10):
        """Random baseline for comparison"""
        random_indices = random.sample(range(len(self.df)), top_n)
        results = self.df.iloc[random_indices][['track_name', 'track_artist', 'playlist_genre']].copy()
        results['similarity'] = np.random.random(top_n)
        results['strategy'] = 'Random Baseline'
        return results

class SongRecommendationStrategies:
    """Strategies for song-based recommendations"""
    
    def __init__(self, df, audio_features):
        self.df = df
        self.audio_features = audio_features
        self.scaler = StandardScaler()
        self.feature_data = self.scaler.fit_transform(df[audio_features])
    
    def strategy_1_cosine_similarity(self, song_name, top_n=10):
        """Original cosine similarity for song-based recommendations"""
        matches = self.df[self.df['track_name'].str.contains(song_name, case=False, na=False)]
        if matches.empty:
            return None, None
        
        song_index = matches.index[0]
        song_vector = self.feature_data[song_index].reshape(1, -1)
        
        sims = cosine_similarity(song_vector, self.feature_data)[0]
        sorted_indices = np.argsort(sims)[::-1][1:top_n+1]
        
        recs = self.df.iloc[sorted_indices][['track_name', 'track_artist', 'playlist_genre']].copy()
        recs['similarity'] = sims[sorted_indices]
        recs['strategy'] = 'Cosine Similarity'
        
        return self.df.loc[song_index, 'track_name'], recs
    
    def strategy_2_artist_boost(self, song_name, top_n=10):
        """Boosts recommendations from the same artist"""
        matches = self.df[self.df['track_name'].str.contains(song_name, case=False, na=False)]
        if matches.empty:
            return None, None
        
        song_index = matches.index[0]
        song_vector = self.feature_data[song_index].reshape(1, -1)
        original_artist = self.df.loc[song_index, 'track_artist']
        
        sims = cosine_similarity(song_vector, self.feature_data)[0]
        
        # Boost same artist songs
        artist_mask = self.df['track_artist'] == original_artist
        sims[artist_mask] *= 1.3  # 30% boost for same artist
        
        sorted_indices = np.argsort(sims)[::-1][1:top_n+1]
        
        recs = self.df.iloc[sorted_indices][['track_name', 'track_artist', 'playlist_genre']].copy()
        recs['similarity'] = sims[sorted_indices]
        recs['strategy'] = 'Artist Boost'
        
        return self.df.loc[song_index, 'track_name'], recs
    
    def strategy_3_genre_similarity(self, song_name, top_n=10):
        """Prioritizes same genre recommendations"""
        matches = self.df[self.df['track_name'].str.contains(song_name, case=False, na=False)]
        if matches.empty:
            return None, None
        
        song_index = matches.index[0]
        song_vector = self.feature_data[song_index].reshape(1, -1)
        original_genre = self.df.loc[song_index, 'playlist_genre']
        
        sims = cosine_similarity(song_vector, self.feature_data)[0]
        
        # Boost same genre songs
        genre_mask = self.df['playlist_genre'] == original_genre
        sims[genre_mask] *= 1.2  # 20% boost for same genre
        
        sorted_indices = np.argsort(sims)[::-1][1:top_n+1]
        
        recs = self.df.iloc[sorted_indices][['track_name', 'track_artist', 'playlist_genre']].copy()
        recs['similarity'] = sims[sorted_indices]
        recs['strategy'] = 'Genre Similarity'
        
        return self.df.loc[song_index, 'track_name'], recs