import os
import random
import requests

from lxml import html

GET_CNN_NEWS_XPATH = '''//p[@class="zn-body__paragraph"]//text() | //div[@class="zn-body__paragraph"]//text()'''

'''
    Load user agents, Avoid anti-scrape!
'''
USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []
with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])
random.shuffle(USER_AGENTS)

# Generate Headers
def getHeaders():
    ua = random.choice(USER_AGENTS)
    headers = {
        "Connection" : "close",
        "User-Agent" : ua
    }
    return headers

def extract_news(news_url):
    # Fetch html from news url
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=getHeaders())

    news = {}
    try:
        # Parse html
        tree = html.fromstring(response.content)
        # Extract information
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        news = ''.join(news)
    except Exception as e:
        print e
        return {}
    return news

if __name__ == '__main__':
    EXPECTED_STRING = "The storms were expected to move into Alabama Sunday evening and continue along a path extending to Michigan."
    CNN_NEWS_URL = "http://www.cnn.com/2017/04/30/us/severe-weather-tornadoes-flooding/index.html"
    news = extract_news(CNN_NEWS_URL)
    print news
    assert EXPECTED_STRING in news
    print 'test_basic passed!'
