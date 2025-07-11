# 🎧 Spotify Song Recommender App

This Streamlit web app recommends songs from a curated Spotify dataset based on:
- 🎛️ User-defined **audio preferences** (e.g., energy, danceability, valence)
- 🔍 **Similar song recommendations** based on a selected track

It uses content-based filtering with audio features and cosine similarity to suggest music you might enjoy.

## 🚀 Live Demo

Try the app here: [🎧 Spotify Song Recommender on Streamlit]

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://spotify-recommender-thfaveuzqnp4jqulgfqlzh.streamlit.app/)


---
## 🚀 Features

- 🔥 Interactive sliders for selecting:
  - Danceability, Energy, Valence, Tempo, Loudness, etc.
- 🎵 Song-based recommendation:
  - Enter any song name and get similar tracks.
- 📈 Audio feature standardization and similarity matching using `scikit-learn`.
- 🎨 Built with [Streamlit](https://streamlit.io) — deploys in seconds.

---
## 📁 Dataset

The dataset includes:
- 32,000+ songs from popular Spotify playlists.
- Audio features like `danceability`, `energy`, `acousticness`, etc.
- Metadata including `track_name`, `artist`, `album`, `popularity`, and `genre`.

Source: [Kaggle]

---
## 🛠 How to Run Locally

1. Clone the repo
   git clone https://github.com/farzadj/spotify-recommender.git
   
   cd spotify-recommender
3. Install dependencies:

   pip install -r requirements.txt   
4. Run the app:
   
   streamlit run spotify_recommender_app_extended.py   
5. Open in browser at http://localhost:8501

---
## 🌐 Deploy on Streamlit Cloud

You can deploy this app for free via Streamlit Community Cloud:

1. Push this repo to GitHub.

2. Go to Streamlit Cloud → "New app"

3. Select the repository and spotify_recommender_app_extended.py as the entry point.

---
## 📦 Dependencies
streamlit, pandas, scikit-learn, numpy

---
## 🙋‍♂️ Author
Farzad Jafarinia

Data Scientist | Machine Learning Scientist
