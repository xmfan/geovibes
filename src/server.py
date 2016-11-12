import json
import requests
from news import News
from flask import Flask, request
app = Flask(__name__)

'''
Batch job
1. Get news
2. send description to sentiment / get sentiment
3. cluster
4. write to file

file with:

event description
location
links
sentiment
time

'''

news_sub_key = '782e68122d8742c091f6dee73fc2d270'
text_sub_key = '7b20e9c1ffa8470cab2e3b6245148cf6'
cities = set()
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
def _getNews():
    ''' returns a list of news articles '''
    headers = {'Ocp-Apim-Subscription-Key': news_sub_key }
    r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/news/',
        headers=headers)
    if r.status_code != 200:
        print "error calling news"
        return
    json_news = r.json()['value']
    news_list = [News(j['name'], j['url'], j['description'], j['datePublished']) for j in json_news]
    return news_list

def addSentiments(news):
    ''' adds sentiment scores to news '''
    assert(len(news) < 100)
    index = 0
    payload = {}
    documents = [None] * len(news)
    ind_to_doc = {}
    for n in news:
        ind_to_doc[str(index)] = n
        documents[index] = {"language": "en",
                 "id": str(index),
                 "text": n.description
                }
        index += 1
    payload['documents'] = documents
    headers = {
        'Ocp-Apim-Subscription-Key': text_sub_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    r = requests.post(
        'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment',
        json = payload,
        headers=headers)
    if r.status_code != 200:
        print "error calling sentiments"
        return
    res = byteify(r.json())['documents']
    for r in res:
        ind_to_doc[r['id']].sentiment = r['score']
def addLocations(news):
    headers = {
        'Ocp-Apim-Subscription-Key': text_sub_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    ind_to_doc = {}
    index = 0
    payload = {}
    documents = [None] * len(news)
    for n in news:
        ind_to_doc[str(index)] = n
        documents[index] = {"language": "en",
                 "id": str(index),
                 "text": n.name + " " + n.description
                }
        index += 1
    payload['documents'] = documents
    r = requests.post(
        'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases',
        json=payload,
        headers=headers)
    if r.status_code != 200:
        print "error calling keyphrases"
        return
    results = byteify(r.json())['documents']
    for res in results:
        # res has keyPhrases (list), id (string)
        keyphrases = res['keyPhrases']
        id = res['id']
        document = ind_to_doc[id]
        location = None
        for k in keyphrases:
            if k in cities:
                location = k
                continue
        if location is not None:
            print location
       # if location is None:
       #     news.remove(document)
       # else:
       #     document.location = location

def getCitiesFromFile():
    with open('../scripts/cities.txt', 'r') as f:
        for line in f:
            cities.add(line.strip())
    print(str(len(cities)) + " cities loaded")

def _calculate():
    getCitiesFromFile()
    news = _getNews()
    addSentiments(news)
    addLocations(news)
   # for n in news:
   #     print n.name
   #     print n.sentiment
   #     print n.location
    # magical clustering
    # writeToFile(news)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/events", methods=['GET'])
def get_events():
    return "get events called"

if __name__ == "__main__":
    _calculate()
    app.run()
