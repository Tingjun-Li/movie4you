from flask import Flask, render_template, request

import movie_tree
import params
from utils import open_cache, retrieve_and_save_movie_data

app = Flask(__name__, template_folder='templates', static_folder='statics')

def main():
    """
    Main function can be used to play and test the code in terminal. It is not used when launching the web app version.
    """
    # Retrieve the movie data from the API
    if params.RETRIEVE_DATA:
        retrieve_and_save_movie_data(params.MOVIE_LIST_FILENAME, popularity_threshold=20)

    cache_dict_final = open_cache(params.CACHE_FILENAME)
    movie_cache_final = cache_dict_final.get("movie_details", [])
    print(f"The cache has {len(movie_cache_final)} qualified movies")

    # Load tree:
    if params.RESET_TREE:
        tree = movie_tree.buildTree(movie_cache_final, movie_tree.EMPTY_MOVIE_TREE)
        tree_file_handle = open(params.TREE_FILE, "w")
        movie_tree.saveTree(tree, tree_file_handle)
        tree_file_handle.close()
    else:
        tree_file_handle = open(params.TREE_FILE, "r")
        tree = movie_tree.loadTree(tree_file_handle)
        tree_file_handle.close()

    # Find movies with tree:
    movie_tree.findMovies(tree, movie_cache_final)

def get_movie_by_questionnaire(answers, number_of_movies):
    cache_dict_final = open_cache(params.CACHE_FILENAME)
    movie_cache_final = cache_dict_final.get("movie_details", [])
    print(f"The cache has {len(movie_cache_final)} qualified movies")

    tree_file_handle = open(params.TREE_FILE, "r")
    tree = movie_tree.loadTree(tree_file_handle)
    tree_file_handle.close()

    # Find movies with tree:
    movie_result = movie_tree.findMovieByQuestionnaire(tree, movie_cache_final, number_of_movies, answers)
    return movie_result

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        print("POST")
        answers = []
        answers.append(request.form.get("english"))
        answers.append(request.form.get("budget"))
        answers.append(request.form.get("runtime"))
        answers.append(request.form.get("action"))

        number_of_movies = int(request.form.get("number_of_movies"))
        print(f"Recievd answers: {answers}. Number of movies: {number_of_movies}")

        movie_result = get_movie_by_questionnaire(answers, number_of_movies)
        
        # Get reviewer score from rotten tomatoes:
        # for movie in movie_result:
        #     base_url = "https://www.rottentomatoes.com/m/"
        #     movie_name = movie.title.lower().replace(": ","_").replace(" ", "_")
        #     movie_url = base_url + movie_name
        #     response = requests.get(movie_url)
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     score_board = soup.find('score-board')
        #     if score_board:
        #         print("Movie: " + movie.title)
        #         print("Audience score: " + score_board["audiencescore"])
        #         print("Tomatometer score: " + score_board["tomatometerscore"])
        #         movie.audiencescore = score_board["audiencescore"]
        #         movie.tomatometerscore = score_board["tomatometerscore"]

        # Get imdb score (But I could not get the response from the website using requests.get()):
        # for movie in movie_result:
        #     base_url = "https://www.imdb.com/title/"
        #     response = requests.get(base_url + movie.imdb_id)
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     movie.imdb_score = soup.find('jGRxWM')
        #     movie.imdb_popularity = soup.find('gopMqI')

        return render_template("result.html", movies=movie_result)
    
    return render_template("index.html")


if __name__ == "__main__":
    if params.RUN_IN_TERMINAL:
        main()
    else:
        print("starting Flask app", app.name)
        app.run(debug=True)
