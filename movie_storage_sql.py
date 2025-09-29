from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

def init_db():
    """Initialize the database and create the movies table if it does not exist."""
    # Create the movies table if it does not exist
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster TEXT NOT NULL
            )
        """))
        connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
            movies = result.fetchall()
            if not movies:
                print('No movies found in database')
                return {}
        return {
            row.title: {
                "year": row.year,
                "rating": row.rating,
                "poster": row.poster,
            }
            for row in movies

        }
    except SQLAlchemyError as e:
        print(f"Database error {e}")
        return {}



def add_movie(title:str, year:int, rating:float,poster:str):
    """Add a new movie to the database."""
    title = title.strip()            # remove leading/trailing spaces
    title = title.casefold().title() # normalize casing
    poster = None if poster == "N/A" else poster  # handle missing posters
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating,:poster)"),
                                   {"title": title, "year": year, "rating": rating,"poster":poster})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
            return True
        except IntegrityError:
            print(f" Movie '{title}' already exists.")
            return False
        except SQLAlchemyError as e:
            print(f" Error adding movie: {e}")
            return False


def delete_movie(title:str):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            result =connection.execute(
                text("DELETE FROM movies WHERE lower(trim(title)) = lower(:title)"),{"title":title})
            connection.commit()
            if result.rowcount == 0:
                print(f"Movie '{title}' not found.")
                return False
            print(f"Movie '{title}' deleted successfully. ")
            return True
        except SQLAlchemyError as e:
            print(f"Error deleting movie: {e}")
            return False


def update_movie(title:str, rating:float):
    """Update a movie's rating in the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title "),
                                        {'rating': rating, 'title': title})
            connection.commit()
            if result.rowcount == 0:
                print(f"Movie 'title' not found")
                return False
            print(f"Movie '{title}' updated successfully.")
            return True

    except SQLAlchemyError as e :
        print(f"Error updating movie {e}")
        return False

# Initialize the database when module is imported
init_db()
