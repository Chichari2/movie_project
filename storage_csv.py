import csv
from istorage import IStorage


class StorageCsv(IStorage):
  def __init__(self, file_path):
    self.file_path = file_path

  def list_movies(self):
    movies = {}
    try:
      with open(self.file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
          movies[row['title']] = {
            'rating': row['rating'],
            'year': row['year'],
            'poster': row.get('poster', 'https://via.placeholder.com/128x193.png?text=No+Image')
          }
    except FileNotFoundError:
      pass
    return movies

  def add_movie(self, title, year, rating, poster):
    movies = self.list_movies()
    if title in movies:
      print(f"Movie '{title}' already exists!")
      return

    movies[title] = {'rating': rating, 'year': year, 'poster': poster}
    self._save_movies(movies)
    print(f"Movie '{title}' added successfully.")

  def delete_movie(self, title):
    movies = self.list_movies()
    if title in movies:
      del movies[title]
      self._save_movies(movies)
      print(f"'{title}' has been deleted!")
    else:
      print(f"Movie '{title}' not found in the database.")

  def update_movie(self, title, rating):
    movies = self.list_movies()
    if title in movies:
      movies[title]['rating'] = rating
      self._save_movies(movies)
      print(f"Movie '{title}' rating updated to {rating}★")
    else:
      print(f"Movie '{title}' not found in the database.")

  def _save_movies(self, movies):
    with open(self.file_path, 'w', newline='', encoding='utf-8') as csvfile:
      fieldnames = ['title', 'rating', 'year', 'poster']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      for title, details in movies.items():
        row = {'title': title, 'rating': details['rating'], 'year': details['year'], 'poster': details['poster']}
        writer.writerow(row)
