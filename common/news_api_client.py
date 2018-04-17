import requests
import json

# NEWS
NEWS_API = "https://newsapi.org/v2/"
NEWS_API_ENDPOINT = "top-headlines"
# Differnt User has Differnt Keys
NEWS_API_KEY = '570814d418c6481396bbb639b37774a6'

# Params
DEFAULT_SOURCES = "cnn"
COUNTRY = 'us'

def buildUrl(news_api = NEWS_API, news_endpoint = NEWS_API_ENDPOINT):
    return news_api + news_endpoint

'''
    Output : List[articals]
    {"source": {"id": "cnn", "name": "CNN"},
    "author":
    "title":
    "description":
    "url":
    "urlToImage":
    "publishedAt": }
'''
def getNewsFromSource(sources = DEFAULT_SOURCES):
    articals = []
    payload = { 'apiKey' : NEWS_API_KEY,
               'sources' : sources,}
    response = requests.get(buildUrl(),
                            params = payload)
    res_json = json.loads(response.content)

    # Extract Info from json
    if (res_json is not None and
        res_json['status'] == 'ok' ):
        articals.extend(res_json['articles'])
    return articals

if __name__ == '__main__':
    print getNewsFromSource()
