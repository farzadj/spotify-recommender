import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("spotify_songs.csv")

# Select audio feature columns
audio_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                  'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
scaler = StandardScaler()
feature_data = scaler.fit_transform(df[audio_features])

# Compute similarity matrix
similarity_matrix = cosine_similarity(feature_data)

# Title
st.title("🎧 Spotify Song Recommender")
st.markdown("Use **audio preferences** or search by **song name** to get personalized recommendations.")

# Tabs for mode selection
mode = st.radio("Select Recommendation Mode:", ["By Audio Preferences", "By Song Name"])

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

    def recommend_by_preferences(preferences, top_n=10):
        scaled_pref = scaler.transform([preferences])
        sims = cosine_similarity(scaled_pref, feature_data)[0]
        top_indices = np.argsort(sims)[::-1][:top_n]
        results = df.iloc[top_indices][['track_name', 'track_artist', 'playlist_genre']]
        results['similarity'] = sims[top_indices]
        return results

    if st.button("🎵 Recommend by Preferences"):
        results = recommend_by_preferences(preferences)
        st.success("Top recommendations based on your preferences:")
        st.dataframe(results.reset_index(drop=True))

else:
    st.subheader("🔍 Recommend Songs Based on a Song Name")
    input_song = st.text_input("Enter a part of a song name:")

    def recommend_by_song(song_name, top_n=10):
        matches = df[df['track_name'].str.contains(song_name, case=False, na=False)]
        if matches.empty:
            return None, None
        song_index = matches.index[0]
        sims = list(enumerate(similarity_matrix[song_index]))
        sorted_songs = sorted(sims, key=lambda x: x[1], reverse=True)[1:top_n+1]
        recs = df.iloc[[idx for idx, _ in sorted_songs]][['track_name', 'track_artist', 'playlist_genre']]
        recs['similarity'] = [score for _, score in sorted_songs]
        return df.loc[song_index, 'track_name'], recs

    if st.button("🎧 Recommend by Song"):
        song_used, recs = recommend_by_song(input_song)
        if recs is not None:
            st.success(f"Top songs similar to: {song_used}")
            st.dataframe(recs.reset_index(drop=True))
        else:
            st.error("No matching song found.")
