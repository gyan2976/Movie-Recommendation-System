import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast
import nltk
import re, sys, os
# nltk.download('stopwords')
# from nltk.corpus import stopwards
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
ps = PorterStemmer()


credits = pd.read_csv('data/tmdb_5000_credits.csv')
movies = pd.read_csv('data/tmdb_5000_movies.csv')

# print(credits.head())
# print(movies.head())

# print(credits.shape, movies.shape)
# print(credits.column)
# print(movies.columns)

movies = movies.merge(credits, on='title')
# print(movies.shape)
# print(movies.columns)

movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# movies.isnull().sum()
movies.dropna(inplace=True)

# movies.duplicated().sum()
# print(movies.iloc[0]['geners'])
# print(movies.iloc[0]['keywords'])

def convert(text):
    l = []
    for i in ast.literal_eval(text):
        l.append(i['name'])
    return l

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

# print(movies.iloc[0]['cast'])

# def convert_cast(text):
#     l = []
#     counter = 0
#     for i in ast.literal_eval(text):
#         if counter < 3:
#             l.append(i['name'])
#             counter += 1
#     return l

def convert_cast(text):
    l = []
    
    # Ensure text is a string before using ast.literal_eval
    if isinstance(text, str):
        try:
            data = ast.literal_eval(text)  # Convert string to list/dict
        except (ValueError, SyntaxError):
            return []  # Return an empty list if conversion fails
    else:
        data = text  # If already a list/dict, use as is
    
    # Extract top 3 cast members
    for i in data[:3]:  # Ensuring only top 3 members
        if isinstance(i, dict) and 'name' in i:
            l.append(i['name'])
    
    return l


movies['cast'] = movies['cast'].apply(convert_cast)

# print(movies.iloc[0]['crew'])

# def fetch_director(text):
#     l = []
#     for i in ast.literal_eval(text):
#         if i['job'] == 'Director':
#             l.append(i['name'])
#             break
#     return l

# def fetch_director(text):
#     l = []
    
#     # Ensure text is a string before using ast.literal_eval
#     if isinstance(text, str):
#         try:
#             data = ast.literal_eval(text)  # Convert string to list/dict
#         except (ValueError, SyntaxError):
#             return []  # Return an empty list if conversion fails
#     else:
#         data = text  # If already a list/dict, use as is
    
#     # Extract the director's name
#     for i in data:
#         if isinstance(i, dict) and i.get('job') == 'Director':
#             l.append(i.get('name'))
#             break  # Stop after finding the first director
    
#     return l

def fetch_director(text):
    if isinstance(text, str):
        try:
            data = ast.literal_eval(text)  # Convert string to list/dict
        except (ValueError, SyntaxError):
            return []  # Return an empty list if conversion fails
    else:
        data = text  # If already a list/dict, use as is
    
    for i in data:
        if isinstance(i, dict) and i.get('job') == 'Director':
            return [i.get('name')]  # Return list with the director's name
    
    return []

movies['crew'] = movies['crew'].apply(fetch_director)

# print(movies.iloc[0]['overview'])
movies['overview'] = movies['overview'].apply(lambda x: x.split())

def remove_space(word):
    l = []
    for i in word:
        l.append(i.replace(' ', ''))
    return l

movies['cast'] = movies['cast'].apply(remove_space)
movies['crew'] = movies['crew'].apply(convert_cast)
movies['genres'] = movies['genres'].apply(convert_cast)
movies['keywords'] = movies['keywords'].apply(convert_cast)

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# print(movies.iloc[0]['tags'])

new_df = movies[['movie_id', 'title', 'tags']]

# print(new_df.head())

new_df['tags'] = new_df['tags'].apply(lambda x: ' '.join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

def stems(text):
    l = []
    for i in text.split():
        l.append(ps.stem(i))
    return " ".join(l)

new_df['tags'] = new_df['tags'].apply(stems)
# print(movies.iloc[0]['tags'])

cv = CountVectorizer(max_features=5000, stop_words='english')

vectors = cv.fit_transform(new_df['tags']).toarray()
# print(vectors.shape)

similarity = cosine_similarity(vectors)
# print(similarity.shape)

# print(new_df[new_df['tags'] == 'avatar'].index[0])

def recommend(movie):
    index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:6]:
        print(new_df.iloc[i[0]].title)

# print(recommend('Avatar'))        

pickle.dump(new_df, open('artifacts/movie_list.pkl', 'wb'))
pickle.dump(similarity, open('artifacts/similarity.pkl', 'wb'))
