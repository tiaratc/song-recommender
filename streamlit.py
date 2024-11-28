import streamlit as st
import pandas as pd
import pickle

# Load the dataset
combined_df = pd.read_csv("spotify_combined_data.csv")

# Load precomputed recommendations
with open("precomputed_recommendations.pkl", "rb") as f:
    precomputed_recommendations = pickle.load(f)

# Streamlit UI
st.title("Precomputed Song Recommendation System")
st.write("Recommendations based on precomputed predictions using SVD.")

# Select a user/playlist
user_id = st.selectbox("Choose a User ID:", combined_df['user_id'].unique())

if user_id:
    st.write(f"Recommendations for User ID: {user_id}")
    
    # Get precomputed recommendations for the selected user
    recommendations = precomputed_recommendations.get(user_id, [])
    
    # Display top recommendations
    if recommendations:
        st.write("### Top 5 Recommendations:")
        for track_id, score in recommendations:
            track_info = combined_df[combined_df['track_id'] == track_id].iloc[0]
            st.write(f"**{track_info['track_name']}** by {track_info['artist_name']} (Predicted Score: {score:.2f})")
    else:
        st.write("No recommendations available for this user.")
