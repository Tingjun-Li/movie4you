from bs4 import BeautifulSoup
import requests
from params import BASE_URL
from movie_api_secrets import API_KEY

response = requests.get('https://www.rottentomatoes.com/m/rrr')
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())
score_board = soup.find('score-board')
print(score_board["audiencescore"])
print(score_board["tomatometerscore"])

response = requests.get(
            BASE_URL+str(241),
            # headers={"Authorization" : "<api_key_here>"},
            params={
                "api_key": API_KEY,
            }
        )
movie = response.json()
movie["vote_average"] = 100
print(movie)