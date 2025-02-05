import requests

# TODO: add a whole playlist to queue
def get_video(api_key, query):
    baseURL = "https://youtube.googleapis.com/youtube/v3/search?type=video&part=snippet&"

    info = requests.get(f"{baseURL}&q={query}&maxResults=6&safeSearch=none&key={api_key}").json()
    ret = []
    for i in range(0, min(4, len(info['items']))):
        ret.append({'webpage_url': f"https://www.youtube.com/watch?v={info['items'][i]['id']['videoId']}", 
            'title': info['items'][i]['snippet']['title'], 
            'thumbnail': info['items'][i]['snippet']['thumbnails']['high']['url']
        })

    return ret
