# Author: Tingjun Li

# This file contains all the parameters used in the program

# The name of the file containing all the movie ids
MOVIE_LIST_FILENAME = "cache/movie_ids_12_05_2022.json"
# The name of the file containing the qualified movie ids
CACHE_FILENAME = "cache/cache_final.json"
# The base url for the API
BASE_URL = "https://api.themoviedb.org/3/movie/"

# The name of the file containing the tree with categorized movie indices
TREE_FILE = "cache/tree_final.txt"

# If True, retrieve data from the API and update it to the cache
RETRIEVE_DATA = False
# If True, reset the tree with new data and update the cache
RESET_TREE = False