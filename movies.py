import random
import re

import movie_storage
from utils import err_msg, user_prompt, display_menu
from datetime import datetime



def print_line(spaces=1):
    # Print blank lines for readability.
    for _ in range(spaces):
        print()


def prompt_user_to_choice():
    choice = int(user_prompt("Enter choice (0-8):"))
    print_line()
    return choice


# print total of movies in database , list all movies along with their rating
def list_movies_and_display_total():
    movies = movie_storage.list_movies()
    total_movies = len(movies)
    print(f"{total_movies} movies in total")
    for movie, info in movies.items():
        print(f"{movie} ({info['year']}): {info['rating']}")
    print_line()

def get_valid_input(prompt,validator,error_msg):
    while True:
        user_input = user_prompt(prompt)
        try:
            result = validator(user_input)
            if result is None:
                print(error_msg)
            elif result is not None:
                return result
        except ValueError:
            pass
            print(error_msg)

def validate_rating(rating):
    if rating.replace('.','',1).isdigit():
        r = float(rating)
        if  1<= r <= 10:
            return r
    return None


def validate_name(name):
    if not name.strip():
        return None
    title = name.strip().title()
    if not re.match(r"^[a-zA-Z0-9\s:'\-!?.,]+$",title):
        return None
    return title


def add_movie():
    movies = movie_storage.list_movies()
    current_year = datetime.now().year
    movie_name = get_valid_input('Enter new movie name:',validate_name,'Please enter a valid, non-empty movie name that is not already in the list')
    movie_year = get_valid_input('Enter a new movie year:',lambda year :int(year) if year.isdigit() and 1888 <= int(year) <= current_year else None,f"Year must be a number between 1888 and {current_year}.")
    movie_rating = get_valid_input('Enter a new movie rating:', validate_rating,"Rating must be a number between 1 and 10." )
    if movie_storage.add_movie(movie_name,movie_rating,movie_year):
        print('Movie added successfully!')
    else:
        err_msg('Movie already exist!')



def delete_movie():
    movie_name = get_valid_input('please enter the name of the movie you want to delete:', validate_name,
                                 'Please enter a valid, non-empty movie name')
    if movie_storage.delete_movie(movie_name):
        print(f"Movie {movie_name} successfully deleted")
    else:
        err_msg("Movie doesn't exist!")
        print_line()



# update a movie
def update_movie():
    movie_name = get_valid_input('please enter the name of the movie you want to update:', validate_name,
                                 'Please enter a valid, non-empty movie name')
    #movie_name = user_prompt("please enter the name of the movie you want to update:")
    movie_rating = get_valid_input('Enter a new movie rating:',validate_rating,"Rating must be a number between 1 and 10.")
    if movie_storage.update_movie(movie_name,movie_rating):
        print('Movie updated successfully!')
    else:
        err_msg("Movie doesn't exist!")
        print_line()


def get_median(ratings):
    sorted_ratings = sorted(ratings)
    count_of_ratings = len(sorted_ratings)
    if count_of_ratings == 0:
        return None
    if count_of_ratings % 2 == 1:  # odd case
        rating_median = sorted_ratings[count_of_ratings // 2]
    else:
        rating_median = (sorted_ratings[count_of_ratings // 2 - 1] + sorted_ratings[count_of_ratings // 2]) / 2
    return rating_median


def print_top_movies(movies):
    ratings = [details['rating'] for details in movies.values()]
    max_rating = max(ratings)
    top_movies = [name for name, details in movies.items() if details['rating'] == max_rating]
    if len(top_movies) > 1:
        names = ', '.join(top_movies)
        print(f"Best movies:  ({names}),{max_rating}")
    else:
        print(f"Best movie: {top_movies[0]}, {max_rating}")


def print_worst_rating_movies(movies):
    ratings = [details['rating'] for details in movies.values()]
    min_rating = min(ratings)
    worst_movies = [name for name, details in movies.items() if details['rating'] == min_rating]
    if len(worst_movies) > 1:
        names = ', '.join(worst_movies)
        print(f"Worst movies: ({names}),{min_rating}")
    else:
        print(f"Worst movie: {worst_movies[0]},{min_rating}")


# print statistics about the movies in database
def print_stats():
    movies = movie_storage.list_movies()
    # average ratings
    ratings = [details['rating'] for details in movies.values() ]
    total_rating = sum(ratings)
    average_rating = total_rating / len(ratings)
    rating_median = get_median(ratings)
    print(f"Average rating: {average_rating:.2f}")
    print(f"Median rating: {rating_median:.2f}")
    # The best and worst movies
    print_top_movies(movies)
    print_worst_rating_movies(movies)
    print_line()


def print_random_movie():
    movies = movie_storage.get_movies()
    #functions like random.choice() need an indexable sequence (like a list or tuple),dict_keys is not indexable.
    random_movie_name = random.choice(list(movies.keys()))
    print(f"Your movie for tonight {random_movie_name} , it'S rated {movies[random_movie_name]['rating']}")
    print_line()


def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j]) + 1
    return dp[m][n]


def search_movie():
    movies = movie_storage.list_movies()
    user_search_query = user_prompt('Enter part of movie name: ')

    results = [(movie , details['rating']) for movie , details in movies.items() if user_search_query.lower() in movie.lower()]
    if results:
        for movie, rating in results:
            print(f"{movie}, {rating}")
            print_line()
    else:
        matching_movies = []
        for movie in movies:
            if min_distance(movie, user_search_query) <= 5:
                matching_movies.append(movie)
        if matching_movies:
            print(f"The movie {user_search_query} does not exist.Did you mean:")
            for movie in matching_movies:
                print(movie)
                print_line()
        else:
            err_msg("No movies found matching your search.")
            print_line()


def print_sorted_movies_by_ratings():
    movies = movie_storage.list_movies()
    sorted_by_ratings = sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=True)
    for movie, details in sorted_by_ratings:
        print(f"{movie}, {details['rating']}")
    print_line()


def main():
    menu = ["Exit", "List movies", "Add movie", "Delete movie", "Update movie", "Stats", "Random movie", "Search movie",
            "Movies sorted by rating"]
    menu_commands = {
        0 :'EXit',
        1 : list_movies_and_display_total,
        2 : add_movie,
        3:delete_movie,
        4:update_movie,
        5:print_stats,
        6:print_random_movie,
        7:search_movie,
        8:print_sorted_movies_by_ratings
    }

    print("********** My Movies Database **********")
    print_line()

    while True:
        display_menu(menu)
        try:
            user_choice = prompt_user_to_choice()
            if user_choice == 0:
                print('Bye!')
                break
            elif user_choice in menu_commands:
                menu_commands[user_choice]()
            else:
                err_msg('Not on the Menu!')
        except ValueError:
            print('Please enter a valid input')


        input("Press Enter to continue")
        print_line()


if __name__ == "__main__":
    main()

