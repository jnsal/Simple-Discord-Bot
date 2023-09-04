import requests
from bs4 import BeautifulSoup as bs
# Num sei se vale o trampo de pegar o wiki
def getRandomWiki():
    #url = requests.get("https://pt.wikipedia.org/wiki/Special:Random")
    # = requests.get("https://pt.wikipedia.org/wiki/Kangaroo_(jogo_eletrônico)")
    url = requests.get("https://pt.wikipedia.org/wiki/M%C4%83dulari")
    ret = bs(url.content, "html.parser")
    print(ret.find_all(class_="mw-parser-output"))

getRandomWiki()