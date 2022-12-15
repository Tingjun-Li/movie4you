#
# Name: Tingjun Li
#

from movie import Movie
import random
import params

EMPTY_MOVIE_TREE = (
    "Do you want some movies which has English as its original language?",
    ("Do you want some movies with high budget?", 
        ("Do you want some movies that are longer than 100 minutes?", 
            ("Do you want some action movies?", 
                ([], None, None), ([], None, None),
            ), 
            ("Do you want some action movies?", 
                ([], None, None), ([], None, None),
            ),
        ),
        ("Do you want some movies that are longer than 100 minutes?", 
            ("Do you want some action movies?", 
                ([], None, None), ([], None, None),
            ), 
            ("Do you want some action movies?", 
                ([], None, None), ([], None, None),
            ),
        ),
    ),
    
    ("Do you want some movies with high budget?", 
        ("Do you want some movies that are longer than 100 minutes?", 
            ("Do you want some action movies?", 
                ([], None, None), ([], None, None),
            ), 
            ("Do you want some action movies?", 
                ([], None, None), ([], None, None),
            ),
        ),
        ("Do you want some movies that are longer than 100 minutes?", 
            ("Do you want some action movies?", 
                ([], None, None), ([], None, None),
            ), 
            ("Do you want some action movies?", 
                ([], None, None), ([], None, None),
            ),
        ),
    ),
)
    

def main():
    """
    The main function. It can printout the cached tree
    --------------------
    Parameters:
    None
    --------------------
    Return:
    None
    """
    tree_file_handle = open(params.TREE_FILE, "r")
    tree = loadTree(tree_file_handle)
    printTree(tree)

def buildTree(movies, tree=None):
    """
    Build a tree.
    --------------------
    Parameters:
    None
    --------------------
    Return:
    tree: a tree
    """
    if tree is None:
        tree = (None, None, None)

    for idx, movie_json in enumerate(movies):
        movie = Movie(movie_json)
        movie_answers = []
        if (movie.original_language == "en"):
            movie_answers.append("Yes")
        else:
            movie_answers.append("No")
        
        if (movie.budget > 50000000):
            movie_answers.append("Yes")
        else:
            movie_answers.append("No")
        
        if (movie.runtime > 100):
            movie_answers.append("Yes")
        else:
            movie_answers.append("No")

        if (movie.is_action() == True):
            movie_answers.append("Yes")
        else:
            movie_answers.append("No")
        
        movie.list_index = idx
        movie.answers = movie_answers
        insertMovie(tree, movie)
    return tree

def insertMovie(tree, movie, question_number = 0):
    """
    Insert a movie into the tree.
    --------------------
    Parameters:
    tree: a tree
    movie: a movie
    --------------------
    Return:
    tree: an updated tree
    """
    if type(tree[0]) is list:
        tree[0].append(movie.list_index)
        return tree
    
    if movie.answers[question_number] == "Yes":
        insertMovie(tree[1], movie, question_number + 1)
    
    if movie.answers[question_number] == "No":
        insertMovie(tree[2], movie, question_number + 1)


def saveTree(tree, tree_file_handle):
    """
    Save the tree to the file treeFile.
    --------------------
    Parameters:
    tree: a tree
    tree_file_handle: a file handle
    --------------------
    Return:
    None
    """
    if tree[1] is not None and tree[2] is not None:
        tree_file_handle.write("Internal Node\n")
        tree_file_handle.write(tree[0] + "\n")
        saveTree(tree[1], tree_file_handle)
        saveTree(tree[2], tree_file_handle)

    else:
        tree_file_handle.write("Leaf Node\n")
        tree_file_handle.write(','.join(str(idx) for idx in tree[0]) + "\n")


def loadTree(treeFile):
    """
    Load the tree from the file treeFile and return the tree.
    --------------------
    Parameters:
    treeFile: a file handle
    --------------------
    Return:
    tree: a tree
    """
    line = treeFile.readline()
    if line == "Internal Node\n":
        question = treeFile.readline().rstrip('\n')
        yes_answer = loadTree(treeFile)
        no_answer = loadTree(treeFile)
        return (question, yes_answer, no_answer)
    elif line == "Leaf Node\n":
        object = treeFile.readline().rstrip('\n')
        return ([int(idx) for idx in object.split(",")], None, None)

def findMovies(tree, movies, random_size = 5):
    """
    Find movie with the tree.
    --------------------
    Parameters:
    tree: a tree
    movies_file_handle: a handle to the movies cache file
    random_size: the number of movies to return
    --------------------
    Return:
    None
    """
    if type(tree[0]) is list:
        print("Here are some movies you may like:")
        for idx in random.sample(tree[0], min(random_size, len(tree[0]))):
            movie = Movie(movies[idx])
            print(movie.title)
        return
    
    answer = input(tree[0] + " (Yes/No): ")
    if answer == "Yes":
        findMovies(tree[1], movies)
    elif answer == "No":
        findMovies(tree[2], movies)

def findMovieByQuestionnaire(tree, movies, number_of_movies, answers):
    """
    Find movie with given tree and questionnaire answers.
    --------------------
    Parameters:
    tree: a tree
    movies_file_handle: a handle to the movies cache file
    number_of_movies: the number of movies to return
    answers: a list of answers
    --------------------
    Return:
    None
    """
    result = []
    if type(tree[0]) is list:
        print("Here are some movies you may like:")
        for idx in random.sample(tree[0], min(number_of_movies, len(tree[0]))):
            movie = Movie(movies[idx])
            result.append(movie)
            print(movie.title)
        return result
    
    answer = answers.pop(0)
    if answer == "Yes":
        result = findMovieByQuestionnaire(tree[1], movies, number_of_movies, answers)
    elif answer == "No":
        result = findMovieByQuestionnaire(tree[2], movies, number_of_movies, answers)

    return result

def printTree(tree, prefix = '', bend = '', answer = ''):
    """Recursively print a tree in a human-friendly form.
       TREE is the tree (or subtree) to be printed.
       PREFIX holds characters to be prepended to each printed line.
       BEND is a character string used to print the "corner" of a tree branch.
       ANSWER is a string giving "Yes" or "No" for the current branch."""
    text, left, right = tree
    if left is None  and  right is None:
        print(f'{prefix}{bend}{answer}{text}')
    else:
        print(f'{prefix}{bend}{answer}{text}')
        if bend == '+-':
            prefix = prefix + '| '
        elif bend == '`-':
            prefix = prefix + '  '
        printTree(left, prefix, '+-', "Yes: ")
        printTree(right, prefix, '`-', "No:  ")


if __name__ == "__main__":
    main()