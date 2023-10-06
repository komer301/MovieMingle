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
    final = []
    if 'results' in data and data['results']:
        for result in data['results']:
            id = result.get('id',0)
            if 'name' in result:
                title = truncate_movie_title(result.get('name'))
            else:
                title = truncate_movie_title(result.get('title'))
            if 'genre_ids' in result:
                genres = result.get('genre_ids')
            else:
                genres = []
            media_type = result.get('media_type')
            for x in range(len(genres)):
                genres[x] =  genreTranslator(genres[x],media_type)
            rating = result.get('vote_average',0)
            poster_path = result.get('poster_path')
            if poster_path:
                poster_path = 'https://image.tmdb.org/t/p/w500' + poster_path
                final.append([id,title,genres,rating,poster_path])
    final = sorted(final, key=lambda x: x[3], reverse=True)
    return final

def truncate_movie_title(title, max_chars_per_line=14, max_lines=2):
    words = title.split()
    truncated_title = ""
    line_length = 0
    line_count = 0

    for word in words:
        if line_count >= max_lines:
            break

        if line_length + len(word) + 1 <= max_chars_per_line:
            if truncated_title:
                truncated_title += " "
                line_length += 1
            truncated_title += word
            line_length += len(word)
        else:
            # Add the word to the current line even if it exceeds max_chars_per_line
            if truncated_title:
                truncated_title += " "
                line_length += 1
            truncated_title += word
            line_length += len(word)
            break  # Stop adding words to this line

        if line_length >= max_chars_per_line:
            line_count += 1
            line_length = 0

    if truncated_title != title:
        if truncated_title.endswith(" "):
            truncated_title = truncated_title.rstrip() + "..."
        else:
            truncated_title = truncated_title + "..."

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
                    print(genreTranslator(genres[x],"movie"))
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

def asteroidCollision(asteroids):
    stack = [] 
    for i in range(len(asteroids)):
        isAlive = True
        while len(stack) != 0 and stack[-1] * asteroids[i] < 0:
            print("first",stack[-1])
            print(asteroids[i], end='\n')
            if abs(asteroids[i]) < abs(stack[-1]):
                isAlive = False
                break
            elif abs(asteroids[i]) > abs(stack[-1]):
                stack.pop()
                isAlive = False
            else:
                stack.pop()
                isAlive = False
                break
        if isAlive:
            stack.append(asteroids[i])
    return stack

print(asteroidCollision([-2,-1,1,2]))