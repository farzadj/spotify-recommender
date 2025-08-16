# Configuration file for Spotify Recommender A/B Testing

# Audio features used for recommendations
AUDIO_FEATURES = [
    'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms'
]

# A/B Testing Configuration
AB_TEST_CONFIG = {
    'data_file': 'ab_test_data.json',
    'session_timeout_hours': 24,  # How long to consider sessions active
    'min_sample_size': 10,  # Minimum samples needed for statistical significance
    'confidence_level': 0.95  # Confidence level for statistical tests
}

# Recommendation Strategy Weights (for weighted features strategy)
FEATURE_WEIGHTS = {
    'danceability': 1.5,
    'energy': 1.5,
    'key': 0.8,
    'loudness': 0.8,
    'mode': 0.8,
    'speechiness': 0.8,
    'acousticness': 1.0,
    'instrumentalness': 1.0,
    'liveness': 0.8,
    'valence': 1.2,
    'tempo': 1.0,
    'duration_ms': 0.8
}

# Popularity boost configuration
POPULARITY_CONFIG = {
    'similarity_weight': 0.7,
    'popularity_weight': 0.3
}

# Artist and genre boost factors
BOOST_FACTORS = {
    'artist_boost': 1.3,  # 30% boost for same artist
    'genre_boost': 1.2    # 20% boost for same genre
}

# Display settings
DISPLAY_CONFIG = {
    'default_recommendations': 10,
    'max_recommendations': 20,
    'show_similarity_scores': True,
    'show_strategy_info': True
}

# Dataset configuration
DATASET_CONFIG = {
    'file_path': 'spotify_songs.csv',
    'encoding': 'utf-8',
    'sample_size': None  # Set to a number to use only a sample of the data
}