import requests

from random import randint

def get_random_giphy(api_key, tag='Waifu', rating='r'):
    path = 'https://api.giphy.com/v1/gifs/random?api_key='

    tag = "Waifu"
    rating = "r"
    rqs = path + api_key + '&tag=' + tag + '&rating=' + rating
    resp = requests.get(rqs).json()

    return resp['data']['images']['downsized']['url']

def get_random_giphy_search(api_key, q='Dominatrix', limit=10,offset=0,rating='r',lang='en'):
    path = 'https://api.giphy.com/v1/gifs/search?api_key='

    if offset == 0:
        offset = randint(0, 10)
    
    rqs = path + api_key + '&q=' + str(q) + '&limit=' + str(limit) + '&offset=' + str(offset) + '&rating=' + rating + '&lang=' + lang
    resp = requests.get(rqs).json()

    limit = len(resp['data']) - 1
    if limit < 1: # if could no find 
        return get_random_giphy(api_key, tag='crying'), False
    
    return resp['data'][randint(0, limit)]['images']['downsized']['url'], True