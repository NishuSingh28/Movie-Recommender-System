import streamlit as st
import pickle
import requests

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = movies['title'].values


def fetch_poster(mve_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key'
                            '=c7b6a3b327ae4486eda03ad7de23e9c5&language=en-US&external_source=imdb_id'.format(mve_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_movies_posters = []
    for name in distances[1:6]:
        movie_id = movies.iloc[name[0]].movie_id
        # fetch poster
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[name[0]].title)
    return recommended_movies, recommended_movies_posters


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Which movie would you like to watch select from the dropdown ?',
    movies_list)


if st.button('RECOMMEND'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
