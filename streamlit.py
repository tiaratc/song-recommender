import streamlit as st
import pandas as pd
import pickle
# from surprise import SVD

# Load the combined dataset
combined_df = pd.read_csv("spotify_combined_data.csv")  # Replace with your dataset file

# Streamlit UI
st.title("Spotify Music Recommendation System")
st.write("Recommend songs for a specific user or playlist based on your data.")

# Select a user/playlist
user_id = st.text_input("Enter User/Playlist ID:")

if user_id:
    st.write(f"Recommendations for user/playlist ID: {user_id}")
    
    # Placeholder logic for recommendations
    st.write("### Top 5 Recommendations (Placeholder):")
    example_recommendations = combined_df[['track_name', 'artist_name']].sample(5)
    for _, row in example_recommendations.iterrows():
        st.write(f"**{row['track_name']}** by {row['artist_name']}")


# # Load the saved model
# with open("spotify_recommender_model.pkl", "rb") as f:
#     model = pickle.load(f)

# # Streamlit UI
# st.title("Spotify Music Recommendation System")
# st.write("Recommend songs for a specific user or playlist based on your data.")

# # Select a user/playlist
# user_id = st.text_input("Enter User/Playlist ID:")

# if user_id:
#     st.write(f"Recommendations for user/playlist ID: {user_id}")
    
#     # Get all unique track IDs
#     all_tracks = combined_df['track_id'].unique()

#     # Tracks already rated by the user
#     rated_tracks = combined_df[combined_df['user_id'] == user_id]['track_id'].values

#     # Find unrated tracks
#     unrated_tracks = [track for track in all_tracks if track not in rated_tracks]

#     # Predict ratings for unrated tracks
#     recommendations = []
#     for track_id in unrated_tracks:
#         prediction = model.predict(user_id, track_id)
#         recommendations.append((track_id, prediction.est))

#     # Sort recommendations by predicted rating
#     recommendations.sort(key=lambda x: x[1], reverse=True)

#     # Display top 5 recommendations
#     st.write("### Top 5 Recommendations:")
#     for track_id, score in recommendations[:5]:
#         track_info = combined_df[combined_df['track_id'] == track_id].iloc[0]
#         track_name = track_info['track_name']
#         artist_name = track_info['artist_name']
#         st.write(f"**{track_name}** by {artist_name} (Predicted Score: {score:.2f})")
