import requests
import json

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxY2QxMTM2MGQyNmQ1MzlhOTFmYjI2YjllNWViODlkNCIsInN1YiI6IjY1MGU0YWY1ZTFmYWVkMDBlM2Y1MWY3MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JcBTbOQwPdpT4MCfmbYH14f9fqWXfIXPFomUp5OyuHE"
    }   

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

def trendingInfo(time_window):
    url = f"https://api.themoviedb.org/3/trending/movie/{time_window}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxY2QxMTM2MGQyNmQ1MzlhOTFmYjI2YjllNWViODlkNCIsInN1YiI6IjY1MGU0YWY1ZTFmYWVkMDBlM2Y1MWY3MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JcBTbOQwPdpT4MCfmbYH14f9fqWXfIXPFomUp5OyuHE"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    if 'results' in data and data['results']:
        for result in data['results']:
            id = result.get('id',0)
            title = result.get('title', 'None')
            rating = result.get('vote_average',0)
            poster_path = 'https://image.tmdb.org/t/p/w500' + result.get('poster_path','None')
            print([id,title,rating,poster_path])


trendingInfo("week")

