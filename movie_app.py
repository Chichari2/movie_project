import requests
import time
from films_web_generator import update_html_file


class MovieApp:
  def __init__(self, storage):
    self._storage = storage
    self.API_KEY = "babd21fe"

  def _fetch_movie_details(self, title, retries=3, backoff_factor=0.3):
    url = f"https://www.omdbapi.com/?apikey={self.API_KEY}&t={title}"
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

  def _command_add_movie(self):
    title = input("Enter new movie name: ")
    movie_details = self._fetch_movie_details(title)
    if movie_details:
      self._storage.add_movie(
        title=title,
        year=movie_details['Year'],
        rating=movie_details['Rating'],
        poster=movie_details['Poster']
      )
    else:
      print(f"Failed to add movie '{title}'.")

  def _command_list_movies(self):
    movies = self._storage.list_movies()
    if not movies:
      print("No movies found.")
    else:
      for title, details in movies.items():
        print(f"{title} ({details['year']}) - {details['rating']}★")

  def _command_delete_movie(self):
    title = input("Enter the movie name to delete: ")
    self._storage.delete_movie(title)

  def _command_update_movie(self):
    title = input("Enter the movie name to update: ")
    rating = input("Enter the new rating: ")
    self._storage.update_movie(title, rating)

  def _generate_website(self):
    movies = self._storage.list_movies()
    update_html_file(movies)
    print("Website generated successfully.")

  def run(self):
    while True:
      print("Menu:")
      print("0. Exit")
      print("1. List movies")
      print("2. Add movie")
      print("3. Delete movie")
      print("4. Update movie")
      print("5. Generate website")
      choice = input("Enter choice (0-5): ")
      if choice == '0':
        print("Bye!")
        break
      elif choice == '1':
        self._command_list_movies()
      elif choice == '2':
        self._command_add_movie()
      elif choice == '3':
        self._command_delete_movie()
      elif choice == '4':
        self._command_update_movie()
      elif choice == '5':
        self._generate_website()
      else:
        print("Invalid choice. Please try again.")
