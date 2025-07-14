import streamlit as st

# Your imports
import pandas as pd
import pickle

# Load your saved model artifacts
# Ensure these are prepared and paths updated
df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# CineMatch App
st.set_page_config(page_title="CineMatch", page_icon="🎬")

# Colorful title
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎬 Welcome to CineMatch 🎬</h1>", unsafe_allow_html=True)
st.markdown("##")

# Dropdown to select a movie
movie_list = df['title'].values
selected_movie = st.selectbox("Select a movie you like:", movie_list)

# Function to recommend top 5 movies
def recommend_top_5(movie_title):
    if movie_title not in df['title'].values:
        return "Movie not found", []
    idx = df[df['title'] == movie_title].index[0]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    recommended = []
    for i in sim_scores[1:6]:
        recommended.append((i[0], df.iloc[i[0]].title))
    return "Success", recommended

# Recommend button
if st.button("Show Recommendations"):
    status, recommendations = recommend_top_5(selected_movie)

    if status == "Movie not found":
        st.error("Movie not found in dataset.")
    else:
        st.markdown("## Recommended Movies:")
        for idx, movie in recommendations:
            st.write(f"🎥 {movie}")
