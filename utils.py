import json
from params import BASE_URL
from movie_api_secrets import API_KEY
import requests

def open_cache(cache_filename):
    """opens the cache file if it exists and loads the JSON into
    the FIB_CACHE dictionary.

    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    cache_filename: str
        The filename for the cache

    Returns
    -------
    The opened cache
    """
    try:
        cache_file = open(cache_filename, "r")
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict, cache_filename="cache/cache.json"):
    """saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    """
    dumped_json_cache = json.dumps(cache_dict, sort_keys=True, indent=2)
    fw = open(cache_filename, "w")
    fw.write(dumped_json_cache)
    fw.close()

def load_movie_ids(file_name):
    """
    Load the movie ids from a file
    Parameters
    ----------
    file_name: str
        The name of the file containing the movie ids
    
    Returns
    -------
    json_file handle
    """
    f = open(file_name)
    json_file = json.load(f)
    f.close()
    
    return json_file
    
def retrieve_and_save_movie_data(file_name, popularity_threshold=20, save_every=10000, print_every=1000):
    """
    Retrieve the movie data from the API
    Parameters
    ----------
    file_name: str
        The name of the file containing the movie ids
    popularity_threshold: int
        The minimum popularity of the movie to retrieve
    save_every: int
        The number of movies to retrieve before saving the cache
    print_every: int
        The number of movies to retrieve before printing the status

    Returns
    -------
    None
    """
    print(f"Retrieving data from {file_name} and saving every {save_every} movies. Printing shows progress every {print_every} movies.")
    movie_ids = load_movie_ids(file_name)
    print(f"There are {len(movie_ids['movies'])} movies in the file")
    movie_cache = []
    i = 0
    for idx, movie in enumerate(movie_ids["movies"]):
        if (idx % print_every == 0):
            print(f"Now starting to retrieve data for: {idx+1}th movie")

        if movie["popularity"] < popularity_threshold:
            continue

        response = requests.get(
            BASE_URL+str(movie["id"]),
            # headers={"Authorization" : "<api_key_here>"},
            params={
                "api_key": API_KEY,
            }
        )
        movie_cache.append(response.json())

        # There are 
        if len(movie_cache) % save_every == 0:
            i += 1
            print(f"Saving the {i}th file, which contains {len(movie_cache)} movies")
            save_cache({"movie_details": movie_cache}, f"cache/cache_{i}.json") 
            movie_cache = []

    i += 1
    print(f"Saving the {i}th file, which contains {len(movie_cache)} movies")
    save_cache({"movie_details": movie_cache}, f"cache/cache_{i}.json")