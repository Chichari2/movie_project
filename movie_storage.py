import json
import requests
from films_web_generator import update_html_file
import time

API_KEY = "babd21fe"  #API key
MOVIE_FILE_PATH = "data.json"


def get_movies():
  try:
    with open(MOVIE_FILE_PATH, "r") as fileobj:
      movie_data = json.load(fileobj)
      return movie_data
  except FileNotFoundError:
    return {}


def save_movies(movies):
  with open(MOVIE_FILE_PATH, "w") as fileobj:
    json.dump(movies, fileobj, indent=4)


def fetch_movie_details(title, retries=3, backoff_factor=0.3):
  url = f"https://www.omdbapi.com/?apikey={API_KEY}&t={title}"

  for retry in range(retries):
    try:
      response = requests.get(url)
      response.raise_for_status()  # Raise an HTTPError for bad responses
      data = response.json()
      if data['Response'] == 'True':
        movie_details = {
          'Title': data.get('Title', 'N/A'),
          'Year': data.get('Year', 'N/A'),
          'Rating': data.get('imdbRating', 'N/A'),
          'Poster': data.get('Poster', 'https://via.placeholder.com/128x193.png?text=No+Image')
        }
        return movie_details
      else:
        print(f"Error: {data['Error']}")
        return None
    except requests.exceptions.RequestException as e:
      print(f"Attempt {retry + 1} failed with error: {e}")
      if retry < retries - 1:
        time.sleep(backoff_factor * (2 ** retry))  # Exponential backoff
      else:
        print("All attempts to fetch movie details failed.")
        return None


def add_movie(title):
  movie_details = fetch_movie_details(title)
  if movie_details:
    movies = get_movies()
    movies[title] = {
      "rating": movie_details['Rating'],
      "year": movie_details['Year'],
      "poster": movie_details['Poster']
    }
    save_movies(movies)
    update_html_file(movies)  # Update the HTML file after adding a movie
    print(f"Movie '{title}' added successfully.")
  else:
    print(f"Failed to add movie '{title}'.")


def delete_movie(title):
  movies = get_movies()
  if title in movies:
    del movies[title]
    save_movies(movies)
    update_html_file(movies)  # Update the HTML file after deleting a movie
    print(f"'{title}' has been deleted!")
  else:
    print(f"Movie '{title}' not found in the database.")


def update_movie(title, rating):
  movies = get_movies()
  if title in movies:
    movies[title]["rating"] = rating
    save_movies(movies)
    update_html_file(movies)  # Update the HTML file after updating a movie
    print(f"Movie '{title}' rating updated to {rating}★")
  else:
    print(f"Movie '{title}' not found in the database.")
