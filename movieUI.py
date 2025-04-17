import pickle
import streamlit as st
import requests


# --- Styling Section ---
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }

    div.stButton > button:first-child {
        background-color: #e50914;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-size: 16px;
        font-weight: bold;
        transition: 0.3s;
        border: none;
    }

    div.stButton > button:first-child:hover {
        background-color: #b20710;
        transform: scale(1.05);
        cursor: pointer;
    }

    img {
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.4);
    }

    .movie-title {
        color: white;
        font-weight: bold;
        text-align: center;
        margin-top: 8px;
    }

    /* Make selectbox label white */
    label, .stSelectbox label {
        color: white !important;
        font-weight: 600;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2f920c90c47a8bbf9051cf6b60597ed4&language=en-US"
    try:
        data = requests.get(url, timeout=10)
        data.raise_for_status()
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('MovieMatch:Recommendation System')

# Load data
movies = pickle.load(open('movie.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Use st.columns instead of st.beta_columns
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"<h5 class='movie-title'>{recommended_movie_names[i]}</h5>", unsafe_allow_html=True)
            st.image(recommended_movie_posters[i])
