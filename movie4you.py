import requests
import webbrowser
import json

CACHE_FILENAME = "cache/cache_final.json"
MOVIE_LIST_FILENAME = "movie_ids_12_05_2022.json"
BASE_URL = "https://api.themoviedb.org/3/movie/"
API_KEY = "8e82d66faf368b0b37ec9ed221ab3ec7"
RETRIEVE_DATA = False

def main():
    # Retrieve the movie data from the API
    if RETRIEVE_DATA:
        retrieve_and_save_movie_data(MOVIE_LIST_FILENAME, popularity_threshold=20)

    cache_dict_final = open_cache(CACHE_FILENAME)
    movie_cache_final = cache_dict_final.get("movie_details", [])
    print(f"The cache has {len(movie_cache_final)} qualified movies")

class Movie:
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", rating="No Rating", movie_length=0, json=None):
        """Initialize a Movie object with a title, author, release year, url, rating, and movie length"""
        if json is None:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url
            self.rating = rating
            self.movie_length = movie_length
        else:
            self.title = json.get("trackName") or json.get("collectionName") or "No Title"
            self.author = json.get("artistName") or "No Author"
            self.release_year = json.get("releaseDate")[:4] or "No Release Year"
            self.url = json.get("trackViewUrl") or json.get("collectionViewUrl") or "No URL"
            self.rating = json.get("contentAdvisoryRating") or "No Rating"
            self.movie_length = json.get("trackTimeMillis") or 0

    def info(self):
        """Return a string of the format: TITLE by ARTIST (YEAR)[GENRE]"""
        return f"{self.title} by {self.author} ({self.release_year}) [{self.rating}]"

    def length(self):
        """Return the length of the song in seconds"""
        return round(self.movie_length / 1000)


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

def save_cache(cache_dict, cache_filename=CACHE_FILENAME):
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


if __name__ == "__main__":
    main()