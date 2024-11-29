import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the cleaned dataset
data_standardized = pd.read_csv("audio_features_cleaned.csv")
features = ['danceability', 'energy', 'valence', 'popularity']

# Recommendation function
def recommend_songs(input_track, input_artist, data, features, num_recommendations=3):
    """
    Recommend songs based on the input track and artist.
    """
    input_data = data[
        (data['track_name'] == input_track) & 
        (data['artist_name'] == input_artist)
    ]
    if input_data.empty:
        return None
    input_features = input_data[features].values
    similarity_scores = cosine_similarity(input_features, data[features])
    data['similarity'] = similarity_scores[0]
    recommendations = data[
        (data['track_name'] != input_track) | 
        (data['artist_name'] != input_artist)
    ].sort_values(by='similarity', ascending=False).head(num_recommendations)
    return recommendations[['track_name', 'artist_name', 'similarity']]

# Initialize session state
if "artist_workflow" not in st.session_state:
    st.session_state.artist_workflow = False
if "song_workflow" not in st.session_state:
    st.session_state.song_workflow = False

# App Layout and Theme
st.image("header.png", use_column_width=True)
st.title("🎵 Song Recommender")
st.write("Get personalized song recommendations!")

# Instructions
with st.expander("ℹ️ How to use this app"):
    st.write("""
    - Click on "Choose Based on Artist" or "Choose Based on Song".
    - Follow the steps to select your preferences.
    - Get personalized recommendations instantly!
    """)

# Quick Stats
col1, col2, col3 = st.columns(3)
col1.metric(label="Total Songs", value=data_standardized.shape[0])
col2.metric(label="Unique Artists", value=data_standardized['artist_name'].nunique())
col3.metric(label="Unique Tracks", value=data_standardized['track_name'].nunique())

# Workflow Selection
if st.button("Choose Based on Artist", key="artist_button"):
    st.session_state.artist_workflow = True
    st.session_state.song_workflow = False

if st.button("Choose Based on Song", key="song_button"):
    st.session_state.artist_workflow = False
    st.session_state.song_workflow = True

# --- Workflow 1: Choose Based on Artist ---
if st.session_state.artist_workflow:
    st.write("🎤 **Choose Based on Artist**")
    selected_artist = st.selectbox("Select an artist:", [""] + list(data_standardized['artist_name'].unique()), key="artist_select")
    if selected_artist:
        filtered_tracks = data_standardized[data_standardized['artist_name'] == selected_artist]['track_name'].unique()
        input_track = st.selectbox("Select a song by this artist:", [""] + list(filtered_tracks), key="track_select_artist")
        if input_track:
            if st.button("Get Recommendations", key="recommend_artist"):
                recommendations = recommend_songs(input_track, selected_artist, data_standardized, features)
                if recommendations is not None and not recommendations.empty:
                    st.write(f"### Recommendations for: **{input_track}** by **{selected_artist}**")
                    for idx, row in recommendations.iterrows():
                        st.write(f"- **{row['track_name']}** by {row['artist_name']}")
                else:
                    st.warning("No recommendations found.")

# --- Workflow 2: Choose Based on Song ---
if st.session_state.song_workflow:
    st.write("🎵 **Choose Based on Song**")
    selected_track = st.selectbox("Select a song:", [""] + list(data_standardized['track_name'].unique()), key="track_select")
    if selected_track:
        artists_for_track = data_standardized[data_standardized['track_name'] == selected_track]['artist_name'].unique()
        input_artist = st.selectbox("Select the artist:", [""] + list(artists_for_track), key="artist_select_song")
        if input_artist:
            if st.button("Get Recommendations", key="recommend_song"):
                recommendations = recommend_songs(selected_track, input_artist, data_standardized, features)
                if recommendations is not None and not recommendations.empty:
                    st.write(f"### Recommendations for: **{selected_track}** by **{input_artist}**")
                    for idx, row in recommendations.iterrows():
                        st.write(f"- **{row['track_name']}** by {row['artist_name']}")
                else:
                    st.warning("No recommendations found.")

# Footer
st.markdown("""
    <footer style="text-align: center;">
    Made with ❤️ by <a href="https://github.com/tiaratc" target="_blank">Tiara Cahyadi</a>
    </footer>
""", unsafe_allow_html=True)
