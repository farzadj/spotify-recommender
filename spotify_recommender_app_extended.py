import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from recommendation_strategies import RecommendationStrategies, SongRecommendationStrategies
from ab_testing import ABTestingFramework

# Load dataset
df = pd.read_csv("spotify_songs.csv")

# Select audio feature columns
audio_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                  'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']

# Initialize recommendation strategies
pref_strategies = RecommendationStrategies(df, audio_features)
song_strategies = SongRecommendationStrategies(df, audio_features)

# Initialize A/B testing framework
ab_framework = ABTestingFramework()

# Title
st.title("🎧 Spotify Song Recommender")
st.markdown("Use **audio preferences** or search by **song name** to get personalized recommendations.")

# Add A/B testing info
with st.expander("🔬 A/B Testing Active"):
    st.info("""
    This app is running A/B tests with different recommendation strategies! 
    You'll be randomly assigned a strategy, and we'll track which ones work best.
    
    **Current Strategies:**
    - Cosine Similarity (original)
    - Euclidean Distance
    - Weighted Features
    - Popularity Boost
    - Genre Aware
    - KNN Based
    - Random Baseline
    """)

# Tabs for mode selection
mode = st.radio("Select Recommendation Mode:", ["By Audio Preferences", "By Song Name", "A/B Test Results"])

if mode == "By Audio Preferences":
    # Sidebar sliders
    st.subheader("🎛️ Set Your Preferences")

    danceability = st.slider('Danceability', 0.0, 1.0, 0.5)
    energy = st.slider('Energy', 0.0, 1.0, 0.5)
    key = st.slider('Key', 0, 11, 5)
    loudness = st.slider('Loudness (dB)', -60.0, 0.0, -5.0)
    mode_val = st.selectbox('Mode', [0, 1], format_func=lambda x: 'Minor' if x == 0 else 'Major')
    speechiness = st.slider('Speechiness', 0.0, 1.0, 0.1)
    acousticness = st.slider('Acousticness', 0.0, 1.0, 0.1)
    instrumentalness = st.slider('Instrumentalness', 0.0, 1.0, 0.0)
    liveness = st.slider('Liveness', 0.0, 1.0, 0.1)
    valence = st.slider('Valence', 0.0, 1.0, 0.5)
    tempo = st.slider('Tempo (BPM)', 50.0, 200.0, 120.0)
    duration = st.slider('Duration (ms)', 60000, 400000, 200000)

    preferences = [danceability, energy, key, loudness, mode_val, speechiness,
                   acousticness, instrumentalness, liveness, valence, tempo, duration]

    # Get assigned strategy for this session
    assigned_strategy = ab_framework.assign_strategy("preferences")
    strategy_name = ab_framework.preference_strategies[assigned_strategy]
    
    st.info(f"🎯 You're testing: **{strategy_name}** strategy")

    if st.button("🎵 Recommend by Preferences"):
        with st.spinner("Finding your perfect songs..."):
            # Call the appropriate strategy method
            if assigned_strategy == 'strategy_1_cosine_similarity':
                results = pref_strategies.strategy_1_cosine_similarity(preferences)
            elif assigned_strategy == 'strategy_2_euclidean_distance':
                results = pref_strategies.strategy_2_euclidean_distance(preferences)
            elif assigned_strategy == 'strategy_3_weighted_features':
                results = pref_strategies.strategy_3_weighted_features(preferences)
            elif assigned_strategy == 'strategy_4_popularity_boost':
                results = pref_strategies.strategy_4_popularity_boost(preferences)
            elif assigned_strategy == 'strategy_5_genre_aware':
                results = pref_strategies.strategy_5_genre_aware(preferences)
            elif assigned_strategy == 'strategy_6_knn_based':
                results = pref_strategies.strategy_6_knn_based(preferences)
            elif assigned_strategy == 'strategy_7_random_baseline':
                results = pref_strategies.strategy_7_random_baseline(preferences)
            
            # Record the recommendation
            ab_framework.record_recommendation(assigned_strategy, results, preferences)
            
            st.success(f"Top recommendations using {strategy_name}:")
            st.dataframe(results.reset_index(drop=True))
            
            # Add feedback collection
            st.subheader("📝 How were these recommendations?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Good recommendations!"):
                    ab_framework.collect_feedback(assigned_strategy, "positive")
                    st.success("Thanks for your feedback!")
            with col2:
                if st.button("👎 Not what I was looking for"):
                    ab_framework.collect_feedback(assigned_strategy, "negative")
                    st.error("We'll improve! Thanks for your feedback.")

elif mode == "By Song Name":
    st.subheader("🔍 Recommend Songs Based on a Song Name")
    input_song = st.text_input("Enter a part of a song name:")

    # Get assigned strategy for song-based recommendations
    assigned_strategy = ab_framework.assign_strategy("song")
    strategy_name = ab_framework.song_strategies[assigned_strategy]
    
    st.info(f"🎯 You're testing: **{strategy_name}** strategy")

    if st.button("🎧 Recommend by Song"):
        if input_song.strip():
            with st.spinner("Finding similar songs..."):
                # Call the appropriate strategy method
                if assigned_strategy == 'strategy_1_cosine_similarity':
                    song_used, recs = song_strategies.strategy_1_cosine_similarity(input_song)
                elif assigned_strategy == 'strategy_2_artist_boost':
                    song_used, recs = song_strategies.strategy_2_artist_boost(input_song)
                elif assigned_strategy == 'strategy_3_genre_similarity':
                    song_used, recs = song_strategies.strategy_3_genre_similarity(input_song)
                
                if recs is not None:
                    # Record the recommendation
                    ab_framework.record_recommendation(assigned_strategy, recs, input_song)
                    
                    st.success(f"Top songs similar to '{song_used}' using {strategy_name}:")
                    st.dataframe(recs.reset_index(drop=True))
                    
                    # Add feedback collection
                    st.subheader("📝 How were these recommendations?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("👍 Good recommendations!", key="song_positive"):
                            ab_framework.collect_feedback(assigned_strategy, "positive")
                            st.success("Thanks for your feedback!")
                    with col2:
                        if st.button("👎 Not what I was looking for", key="song_negative"):
                            ab_framework.collect_feedback(assigned_strategy, "negative")
                            st.error("We'll improve! Thanks for your feedback.")
                else:
                    st.error("No matching song found.")
        else:
            st.warning("Please enter a song name.")

elif mode == "A/B Test Results":
    # Display A/B test results
    ab_framework.display_ab_test_results()
    
    # Add admin controls
    with st.expander("🔧 Admin Controls"):
        if st.button("Reset A/B Test Data"):
            ab_framework.reset_test_data()
        
        # Show raw data
        if st.checkbox("Show Raw Test Data"):
            st.json(ab_framework.test_data)

# Add session info in sidebar
with st.sidebar:
    st.subheader("🔬 A/B Testing Info")
    if 'session_id' in st.session_state:
        st.write(f"**Session ID:** {st.session_state.session_id[:8]}...")
        st.write(f"**Current Strategy:** {strategy_name}")
    
    st.subheader("📊 Quick Stats")
    performance = ab_framework.get_strategy_performance()
    if performance:
        best_strategy = max(performance.items(), key=lambda x: x[1]['satisfaction_rate'])
        st.write(f"**Best performing:** {best_strategy[0]}")
        st.write(f"**Satisfaction rate:** {best_strategy[1]['satisfaction_rate']:.2%}")
    else:
        st.write("No data yet")
