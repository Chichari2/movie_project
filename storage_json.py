import json
import requests
import time
from istorage import IStorage

API_KEY = "babd21fe"
MOVIE_FILE_PATH = "data.json"


class StorageJson(IStorage):
  def __init__(self, file_path=MOVIE_FILE_PATH):
    self.file_path = file_path

  def list_movies(self):
    try:
      with open(self.file_path, "r") as fileobj:
        return json.load(fileobj)
    except FileNotFoundError:
      return {}

  def add_movie(self, title, year, rating, poster):
    movies = self.list_movies()
    movies[title] = {"year": year, "rating": rating, "poster": poster}
    self.save_movies(movies)

  def delete_movie(self, title):
    movies = self.list_movies()
    if title in movies:
      del movies[title]
      self.save_movies(movies)

  def update_movie(self, title, rating):
    movies = self.list_movies()
    if title in movies:
      movies[title]["rating"] = rating
      self.save_movies(movies)

  def save_movies(self, movies):
    with open(self.file_path, "w") as fileobj:
      json.dump(movies, fileobj, indent=4)

  def fetch_movie_details(self, title, retries=3, backoff_factor=0.3):
    url = f"https://www.omdbapi.com/?apikey={API_KEY}&t={title}"
    for retry in range(retries):
      try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['Response'] == 'True':
          return {
            'Title': data.get('Title', 'N/A'),
            'Year': data.get('Year', 'N/A'),
            'Rating': data.get('imdbRating', 'N/A'),
            'Poster': data.get('Poster', 'https://via.placeholder.com/128x193.png?text=No+Image')
          }
        else:
          print(f"Error: {data['Error']}")
          return None
      except requests.exceptions.RequestException as e:
        print(f"Attempt {retry + 1} failed with error: {e}")
        if retry < retries - 1:
          time.sleep(backoff_factor * (2 ** retry))
        else:
          print("All attempts to fetch movie details failed.")
          return None
