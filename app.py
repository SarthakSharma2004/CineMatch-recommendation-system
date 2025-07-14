import streamlit as st
import pandas as pd
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data on first run
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Preprocessing utilities
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) 
             for word, tag in nltk.pos_tag(words) if word not in stop_words]
    return ' '.join(words)

# Caching to avoid recomputation
@st.cache_data(show_spinner=True)
def load_and_process():
    df = pd.read_csv('data/cleaned_data.csv')
    df['tags'] = df['tags'].fillna('').apply(preprocess)
    bow = CountVectorizer(max_features=3000, stop_words='english')
    vectors = bow.fit_transform(df['tags']).toarray()
    similarity = cosine_similarity(vectors)
    return df, similarity

df, similarity = load_and_process()

# Recommendation function
def recommend_top_5(movie_name):
    movie_name = movie_name.lower()
    if movie_name not in df['title'].str.lower().values:
        return "Movie not found", []

    index = df[df['title'].str.lower() == movie_name].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    recommended_movies = [df.iloc[i[0]]['title'] for i in movies_list]
    return "Success", recommended_movies

# Streamlit UI
st.title("🎬 CineMatch: Movie Recommendation System")
st.write("Discover movies similar to your favorites instantly.")

movie_list = df['title'].values
selected_movie = st.selectbox("Search for a movie:", sorted(movie_list))

if st.button("Recommend"):
    status, recommendations = recommend_top_5(selected_movie)
    if status == "Success":
        st.subheader("Top 5 Similar Movies:")
        for idx, movie in enumerate(recommendations, 1):
            st.write(f"{idx}. {movie}")
    else:
        st.error("Movie not found. Please try another title.")

       
