import requests
from datetime import date
import json

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxY2QxMTM2MGQyNmQ1MzlhOTFmYjI2YjllNWViODlkNCIsInN1YiI6IjY1MGU0YWY1ZTFmYWVkMDBlM2Y1MWY3MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JcBTbOQwPdpT4MCfmbYH14f9fqWXfIXPFomUp5OyuHE"
    }   

def dateVerify(initialDate):
    year, month, day = map(int, initialDate.split('-'))
    today = date.today()
    input_date = date(year, month, day)
    return input_date > today

def genreTranslator(id,type):
    if type == "movie":
        url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        genres = data['genres']
        for item in genres:
            if item['id'] == id:
                return item['name']
    else:
        url = "https://api.themoviedb.org/3/genre/tv/list?language=en"
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        genres = data['genres']
        for item in genres:
            if item['id'] == id:
                return item['name']


def multiSearch(title):
    x = title.split()
    final = "%20".join(x)
    url = f"https://api.themoviedb.org/3/search/multi?query={final}&include_adult=true&language=en&page=1"
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    # for show in data['results']:
        # print(show['id'])
    # json_formatted = json.dumps(data['results'], indent=2)
    json_formatted2 = json.dumps(data['total_results'], indent=2)
    print(json_formatted2)

def truncate_movie_title(title, max_chars=28):
    if len(title) > max_chars:
        truncated_title = title[:max_chars - 3] + "..."
    else:
        truncated_title = title
    return truncated_title

def trendingInfo(type,time_window):
    url = f"https://api.themoviedb.org/3/trending/{type}/{time_window}?language=en-US"
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    final = []
    if 'results' in data and data['results']:
        for result in data['results']:
            id = result.get('id',0)
            title = truncate_movie_title(result.get('title'))
            genres = result.get('genre_ids')
            for x in range(len(genres)):
                genres[x] =  genreTranslator(genres[x],"movie")
            rating = result.get('vote_average',0)
            poster_path = 'https://image.tmdb.org/t/p/w500' + result.get('poster_path','None')
            final.append([id,title,genres,rating,poster_path])
    return final

def upcomingInfo(type):
    if type == "movie":
        url = f"https://api.themoviedb.org/3/{type}/upcoming?language=en-US&page=1"
    else:
        url = "https://api.themoviedb.org/3/tv/top_rated?language=en-US&page=1"
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    final = []
    if 'results' in data and data['results']:
        for result in data['results']:
            release = result.get('release_date')
            if dateVerify(release):
                id = result.get('id',0)
                title = truncate_movie_title(result.get('title'))
                genres = result.get('genre_ids')
                for x in range(len(genres)):
                    genres[x] = genreTranslator(genres[x],"movie")
                rating = result.get('vote_average',0)
                
                poster_path = 'https://image.tmdb.org/t/p/w500' + result.get('poster_path','None')
                final.append([id,title,genres,rating,poster_path])
    return final

def tvShowTrending():
    url = "https://api.themoviedb.org/3/tv/top_rated?language=en-US&page=1"
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    final = []
    if 'results' in data and data['results']:
        for result in data['results']:
            id = result.get('id',0)
            title = truncate_movie_title(result.get('name'))
            genres = result.get('genre_ids')
            for x in range(len(genres)):
                genres[x] = genreTranslator(genres[x],"tv")
            rating = result.get('vote_average',0)
            poster_path = 'https://image.tmdb.org/t/p/w500' + result.get('poster_path','None')
            final.append([id,title,genres,rating,poster_path])
    return final

multiSearch('the office')