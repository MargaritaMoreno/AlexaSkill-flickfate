import requests
import random
from imdb import IMDb

## Get a random movie ##
ia = IMDb()
movies = ia.get_top250_movies()
random_movie = random.choice(movies)
title = random_movie['title']

print(random_movie['title'])

## Get the streaming service ##

url = "https://streaming-availability.p.rapidapi.com/v2/search/title"

querystring = {"title":title,"country":"mx","show_type":"movie","output_language":"en"}

headers = {
	"X-RapidAPI-Key": "da318c225cmshe652ecbca62d7eap1544aejsnc2850b6bac62",
	"X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data = response.json()
dict = data["result"][0]["streamingInfo"]["mx"]
first_key = next(iter(dict))
print(first_key) 

## Get random quote ##

url = "https://andruxnet-random-famous-quotes.p.rapidapi.com/"

querystring = {"cat":"movies","count":"1"}

headers = {
	"X-RapidAPI-Key": "da318c225cmshe652ecbca62d7eap1544aejsnc2850b6bac62",
	"X-RapidAPI-Host": "andruxnet-random-famous-quotes.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()
quote = data[0]["quote"]
movie = data[0]["author"]
print(f"{quote} from the movie {movie}")