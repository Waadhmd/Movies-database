import requests
import os
from dotenv import load_dotenv
from requests.exceptions import RequestException

load_dotenv()
OMDB_URL ='http://www.omdbapi.com/'
API_KEY = os.getenv('API_KEY')

def fetch_movie(title:str):
    """fetch movie by title from omdb api """
    params = {'t':title,'apikey':API_KEY}
    try:
        response = requests.get(OMDB_URL, params)
        data = response.json()
        if data.get('Response') == 'False':
            print(f"Movie '{title}' not found in the OMDB API.")
            return None
        return {'title': data['Title'],
                'year': int(data['Year']),
                'rating': float(data['imdbRating'] if data['imdbRating'] != 'N/A' else None),
                'poster': data['Poster']}
    except RequestException as e:
        print(f"API request has failed {e}.")
    except ValueError:
        print('Failed to parse API response as json.')



print(fetch_movie('inception'))