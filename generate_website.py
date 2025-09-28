import movie_storage_sql as storage

TEMPLATE_FILE_BATH = '_static/index_template.html'
OUTPUT_HTML_FILE = '_static/index.html'

def save_file(file_path, content):
    """Save rendered content to a file."""
    with open(file_path, 'w',encoding='utf-8') as file:
        file.write(content)

def load_html(file_path):
    with open(file_path, 'r',encoding='utf-8') as template:
        return template.read()

def serialize_movie(title: str, movie_info: dict):

    """Return HTML block for a single movie using semantic tags."""
    return f"""
        <article class="movie-card">
            <img src="{movie_info['poster']}" alt="Poster of {title}" class="movie-poster"/>
            <h2 class="movie-title">{title}</h2>
            <p class="movie-year">{movie_info['year']}</p>
        </article>
        """

def generate_website():
    """Generate website index.html from template and movie storage."""
    html_template = load_html(TEMPLATE_FILE_BATH)
    movies = storage.list_movies()
    movie_grid = ''.join(serialize_movie(title, info) for title, info in movies.items())
    rendered_html = html_template.replace('__TEMPLATE_TITLE__','__Movie database__')
    rendered_html = rendered_html.replace(' __TEMPLATE_MOVIE_GRID__',movie_grid)

    save_file(OUTPUT_HTML_FILE,rendered_html)
    print("Website was generated successfully.")


generate_website()

