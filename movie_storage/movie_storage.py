import json

FILENAME = '../data/data.json'


def get_movies():
    """
       Returns a dictionary of dictionaries that
       contains the movies information in the database.

       The function loads the information from the JSON
       file and returns the data.

       For example, the function may return:
       {
         "Titanic": {
           "rating": 9,
           "year": 1999
         },
         "..." {
           ...
         },
       }
       """

    try:
        with open(FILENAME, 'r') as movies_details:
            return json.load(movies_details)
    except FileNotFoundError:
        return {}


def save_movies(movies):
    """
        Gets all your movies as an argument and saves them to the JSON file.
        """
    with open(FILENAME, 'w') as f:
        json.dump(movies, f, indent=4)


def list_movies():
    """Return all movies as a dict {title: {rating, year}}."""
    return get_movies()


def add_movie(title, rating, year):
    """
      Adds a movie to the movies database.
      Loads the information from the JSON file, add the movie,
      and saves it. The function doesn't need to validate the input.
      """
    movies = get_movies()
    title = title.title()
    if title in movies:
        return False
    movies[title] = {'rating': rating, 'year': year}
    save_movies(movies)
    return True


def delete_movie(title):
    """
       Deletes a movie from the movies database.
       Loads the information from the JSON file, deletes the movie,
       and saves it. The function doesn't need to validate the input.
       """
    movies = get_movies()
    title = title.title()
    if title in movies:
        movies.pop(title, None)
        save_movies(movies)
        return True
    return False


def update_movie(title, rating):
    """
       Updates a movie from the movies database.
       Loads the information from the JSON file, updates the movie,
       and saves it. The function doesn't need to validate the input.
       """
    movies = get_movies()
    title = title.title()
    if title in movies:
        movies[title]['rating'] = rating
        save_movies(movies)
        return True
    return False





