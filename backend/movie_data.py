import requests
import json

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxY2QxMTM2MGQyNmQ1MzlhOTFmYjI2YjllNWViODlkNCIsInN1YiI6IjY1MGU0YWY1ZTFmYWVkMDBlM2Y1MWY3MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JcBTbOQwPdpT4MCfmbYH14f9fqWXfIXPFomUp5OyuHE"
    }   

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
    for show in data['results']:
        print(show['id'])
    # json_formatted = json.dumps(data['results'], indent=2)
    json_formatted2 = json.dumps(data['total_results'], indent=2)
    # print(json_formatted)
    print(json_formatted2)

def truncate_movie_title(title, max_chars=28):
    if len(title) > max_chars:
        truncated_title = title[:max_chars - 3] + "..."
    else:
        truncated_title = title
    return truncated_title

def trendingInfo(time_window):
    url = f"https://api.themoviedb.org/3/trending/movie/{time_window}?language=en-US"
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    if 'results' in data and data['results']:
        for result in data['results']:
            id = result.get('id',0)
            title = truncate_movie_title(result.get('title'))
            genres = result.get('genre_ids')
            for x in range(len(genres)):
                genres[x] = genreTranslator(genres[x],"movie")
            rating = result.get('vote_average',0)
            poster_path = 'https://image.tmdb.org/t/p/w500' + result.get('poster_path','None')
            print([id,title,genres,rating,poster_path])


trendingInfo("week")

# 38 CHARACTERS MAX


# Example usage:
# movie_title1 = "Creation of the Gods I: Kingdom..."
# movie_title2 = "Teenage Mutant Ninja Turtles: Mutant Mayhem"
# truncated_title1 = truncate_movie_title(movie_title1)
# truncated_title2 = truncate_movie_title(movie_title2)
# print(truncated_title1)  # Output: "Creation of the Gods I: Kingdom..."
# print(truncated_title2)  # Output: "The Wonderful Story of Henry..."

# print(genreTranslator(18,"movie"))


