import pickle
import streamlit as st
import requests

st.header("Movie Recommendation System")

# # def fetch_poster(movie_id):
# #     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=59db3a5daf52a55f9f194ad064f1fa11language=en-US"
# #     data = requests.get(url)
# #     data = data.json()
# #     poster_path = data['poster_path']
# #     # full_path = 'https://image.tmdb.org/t/p/w500/' + poster_path
# #     full_path = 'https://www.themoviedb.org/t/p/w500_and_h900_bestv2/' + poster_path
# #     # full_path = 'http://image.tmdb.org/t/p/w500/' + poster_path
# #     return full_path

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=59db3a5daf52a55f9f194ad064f1fa11&language=en-US"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure no HTTP error
        data = response.json()
        
        poster_path = data.get('poster_path')  # Get poster_path safely
        
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"  # TMDb image base URL
        else:
            return "https://via.placeholder.com/500x750?text=No+Image+Available"  # Default image if missing

    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Image"  # Placeholder for API errors

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movies_names = []
        recommended_movies_posters = []
        
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id  # Ensure movie_id exists
            if not movie_id:
                print(f"Skipping movie with missing ID at index {i[0]}")
                continue  # Skip missing movie IDs
            
            recommended_movies_names.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        
        return recommended_movies_names, recommended_movies_posters

    except Exception as e:
        print(f"Error in recommend function: {e}")
        return [], []

# Load movie data
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie", movie_list)

# Show recommendations when button is clicked
if st.button("Recommend"):
    recommended_movies_names, recommended_movies_posters = recommend(selected_movie)

    if recommended_movies_names:
        cols = st.columns(5)  # Create 5 columns for movie recommendations
        for i in range(len(recommended_movies_names)):
            with cols[i]:
                st.text(recommended_movies_names[i])
                st.image(recommended_movies_posters[i])
    else:
        st.error("No recommendations available. Please try another movie.")

# if st.button("Recommend"):
#     recommended_movies_names, recommended_movies_posters = recommend(selected_movie)
#     col1, col2, col3, col4, col5 =st.columns(5)
#     with col1:
#         st.text(recommended_movies_names[0])
#         st.image(recommended_movies_posters[0])
#     with col2:
#         st.text(recommended_movies_names[1])
#         st.image(recommended_movies_posters[1])
#     with col3:
#         st.text(recommended_movies_names[2])
#         st.image(recommended_movies_posters[2])
#     with col4:
#         st.text(recommended_movies_names[3])
#         st.image(recommended_movies_posters[3])
#     with col5:
#         st.text(recommended_movies_names[4])
#         st.image(recommended_movies_posters[4])        
