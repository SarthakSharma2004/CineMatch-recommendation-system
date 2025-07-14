import streamlit as st
import pandas as pd
import pickle

# Load preprocessed data and similarity matrix
df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommend function
def recommend_top_5(movie_name):
    movie_name = movie_name.lower()
    if movie_name not in df['title'].str.lower().values:
        return []

    index = df[df['title'].str.lower() == movie_name].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    recommended_movies = [df.iloc[i[0]]['title'] for i in movies_list]
    return recommended_movies

# Streamlit UI
st.title("🎬 CineMatch: Movie Recommendation System")

movie_list = df['title'].values
selected_movie = st.selectbox("Search for a movie to get recommendations", movie_list)

if st.button("Recommend"):
    recommendations = recommend_top_5(selected_movie)
    if recommendations:
        st.subheader("Top 5 Recommendations:")
        for idx, movie in enumerate(recommendations, 1):
            st.write(f"{idx}. {movie}")
    else:
        st.warning("Movie not found in the dataset. Please try another movie.")

       
