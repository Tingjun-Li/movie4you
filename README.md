# movie4you

## Prerequisite:
1. [flask](https://flask.palletsprojects.com/en/2.2.x/): `pip3 install flask`
2. [requests](https://requests.readthedocs.io/en/latest/): `pip3 install requests`
3. [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): `pip3 install bs4`

If you don't need to update interact with the movie API, you can skip the following step. Otherwise:

4. Please go to [The Movie Database API](https://developers.themoviedb.org/3/getting-started/introduction) and register for an API key. Put this key into a file `movie_api_secrets.py` in the root folder and name it as `API_KEY=<YOUR_API_KEY>`.

## Run the program:
1. Download the code: `git clone https://github.com/Tingjun-Li/movie4you.git`
2. Go to the root folder: `cd movie4you` 
3. check `params.py` file and change params as you want
4. run `python3 movie4you.py` and click the link in the terminal (e.g. http://127.0.0.1:5000)

## Tree data structure:
1. One can run `python3 movie_tree.py` to print out the tree in the terminal. The tree structure follows the following pattern:
![Tree structure that stores my data](./images/507ProjTree.png)
