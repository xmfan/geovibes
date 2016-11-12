from threading import Thread, Lock
from news import News
import time
import json
import requests

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

class CalcThread(Thread):
    def __init__(self, lock):
        Thread.__init__(self)
        self.lock = lock
        self.processor = Processor(self.lock)
    def run(self):
        while True:
            self.processor.calculate()
            time.sleep(10)

class Processor(object):
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
    def __init__(self, lock):
        self.news_sub_key = '782e68122d8742c091f6dee73fc2d270'
        self.text_sub_key = '7b20e9c1ffa8470cab2e3b6245148cf6'
        self.cities = set()
        self.lock = lock
        self.cities = self.getCitiesFromFile()

        self.news_json_read = {}
        self.news_json_write = {}

    def getNews(self):
        ''' returns a list of news articles '''
        headers = {'Ocp-Apim-Subscription-Key': self.news_sub_key }
        r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/news/',
            headers=headers)
        if r.status_code != 200:
            print "error calling news"
            return
        json_news = r.json()['value']
        news_list = [News(j['name'], j['url'], j['description'], j['datePublished']) for j in json_news]
        return news_list

    def addSentiments(self, news):
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
            'Ocp-Apim-Subscription-Key': self.text_sub_key,
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
        return news

    def addLocations(self, news):
        headers = {
            'Ocp-Apim-Subscription-Key': self.text_sub_key,
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
                if k in self.cities:
                    location = k
                    continue
            if location is None:
                news.remove(document)
            else:
                document.location = location
        return news

    def getCitiesFromFile(self):
        cities = set()
        with open('../scripts/cities.txt', 'r') as f:
            for line in f:
                cities.add(line.strip())
        return cities
    
    

    def writeToFile(self, news):
        with self.lock:
            with open('events_write.txt', 'w') as f:
                for n in news:
                    json.dump(n.__dict__, f)
        return

    def calculate(self):
        news = self.getNews()
        self.addSentiments(news)
        self.addLocations(news)
        # magical clustering
        self.writeToFile(news)


