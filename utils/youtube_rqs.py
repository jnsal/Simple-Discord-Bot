import requests

def get_video(api_key, query):
    baseURL = "https://youtube.googleapis.com/youtube/v3/search?part=snippet&"

    info = requests.get(f"{baseURL}&q={query}&maxResults=1&key={api_key}").json()

    return {'webpage_url': f"https://www.youtube.com/watch?v={info['items'][0]['id']['videoId']}", 
            'title': info['items'][0]['snippet']['title'], 
            'thumbnail': info['items'][0]['snippet']['thumbnails']['high']['url']
    }