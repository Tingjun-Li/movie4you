# Author: Tingjun Li

# This file contains all the parameters used in the program

# The name of the file containing all the movie ids
MOVIE_LIST_FILENAME = "cache/movie_ids_12_05_2022.json"
# The name of the file containing the qualified movie ids
CACHE_FILENAME = "cache/cache_with_score.json"
# The base url for the API
BASE_URL = "https://api.themoviedb.org/3/movie/"
# URL to Rotten Tomatoes
ROTTEN_TOMATO_URL = "https://www.rottentomatoes.com/m/"
# The Movie API url
MOVIE_API_URL = "https://api.themoviedb.org/"

# The name of the file containing the tree with categorized movie indices
TREE_FILE = "cache/tree_with_score.txt"

# If True, retrieve data from the API and update it to the cache
RETRIEVE_DATA = False
# If True, reset the tree with new data and update the cache
RESET_TREE = False
# If True, run the program in terminal only:
RUN_IN_TERMINAL = False