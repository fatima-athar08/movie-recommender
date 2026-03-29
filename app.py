import streamlit as st
import pickle
import requests
def fetch_poster(movie_id):
   response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f3c107d7f91423722c136ffc4ff90003&language=en-US'.format(movie_id))
   data=response.json()
   return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

# #load data
# movies=pickle.load(open("movies.pkl","rb"))
# similarity = pickle.load(open("similarity.pkl","rb"))

movies = pickle.load(open("movies.pkl","rb"))

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

similarity = cosine_similarity(vectors)

st.title('Movie Recommender System')

selected_movie_name= st.selectbox(
    "Select a movie to recommend",
 movies['title'].values)
if st.button("Recommend"):
    names,posters=recommend(selected_movie_name)

    col1,col2,col3,col4,col5=st.columns(5)
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