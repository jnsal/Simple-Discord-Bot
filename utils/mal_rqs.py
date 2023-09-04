import requests

def get_anime(api_key, query):
    return get_anime_list(api_key, query, 1)[0]

def get_anime_by_id(api_key, id, nsfw = True):
    default_url = f'https://api.myanimelist.net/v0.2/anime/{id}?fields=id,main_picture,alternative_titles,pictures,title,genres,synopsis,rank,mean&nsfw={nsfw}&code={api_key}'
    val = requests.get(default_url).json()

    if 'rank' in val:
        return {'id': val['id'], 'title': val['title'], 'main_picture': val['main_picture'],'genres': val['genres'], 'pictures': val['pictures'], 'synopsis': val['synopsis'], 'mean': val['mean'], 'rank': val['rank']}
    else:
        return {'id': val['id'], 'title': val['title'], 'main_picture': val['main_picture'],'genres': val['genres'], 'pictures': val['pictures'], 'synopsis': val['synopsis'], 'mean': val['mean'], 'rank': 'N/A'}

def get_anime_list(api_key, query, limit = 4, nsfw = True): # return a list of animes based on a query
    default_url = 'https://api.myanimelist.net/v0.2/anime?'
    url = f"{default_url}q={query}&limit={limit}&nsfw={nsfw}&code={api_key}"
    ret = requests.get(url).json()
    val = []
    for i in range(0, len(ret['data'])):
        val.append(get_anime_by_id(api_key,ret['data'][i]['node']['id']))
    
    return val