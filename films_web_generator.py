import json


def load_data(file_path):
  with open(file_path, "r") as handle:
    return json.load(handle)


def serialize_movie(movie_obj):
  poster = movie_obj.get('poster', 'https://via.placeholder.com/128x193.png?text=No+Image')
  title = movie_obj.get('title', 'Unknown Title')
  year = movie_obj.get('year', 'Unknown Year')

  output = f'<li><div class="movie"><img class="movie-poster" src="{poster}">'
  output += f'<div class="movie-title">{title}</div>'
  output += f'<div class="movie-year">{year}</div></div></li>'

  return output


def update_html_file(movies):
  with open("index_template.html", "r") as fileobj:
    data = fileobj.read()

  movie_entries = ""
  for movie_title, movie_details in movies.items():
    movie_obj = {
      "title": movie_title,
      "poster": movie_details.get("poster", 'https://via.placeholder.com/128x193.png?text=No+Image'),
      "year": movie_details.get("year", 'Unknown Year')
    }
    movie_entries += serialize_movie(movie_obj) + "\n"

  updated_html = data.replace("__TEMPLATE_TITLE__", "My Movie App").replace("__TEMPLATE_MOVIE_GRID__", movie_entries)

  with open("index.html", "w") as fileobj:
    fileobj.write(updated_html)
