from threading import Thread, Lock
from news import News
import time
import csv
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
        self.lock = lock
        self.processor = Processor(self.lock)
        Thread.__init__(self)
    def run(self):
        while True:
            self.processor.calculate()
            time.sleep(1000)

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
        self.news_sub_key = '305dc95e236544168d39b8d0549a8725'
        self.text_sub_key = '7b20e9c1ffa8470cab2e3b6245148cf6'
        self.lock = lock
        self.code_to_countries = self.getCountriesFromFile()
        self.code_to_coords = self.getCoordsFromFile()
        self.codecity_to_coords = self.getCityCoordsFromFile()

        self.countryList = [
                'us',
                'cn',
                'in',
                'au',
                'de',
                'ru',
                'ph',
                'jp'
        ]
        self.cityList = [
            {'city': 'New York', 'code': 'us'},
            {'city': 'Toronto', 'code': 'ca'},
            {'city': 'Beijing', 'code': 'cn'},
            {'city': 'Berlin', 'code': 'de'},
            {'city': 'Montreal', 'code': 'ca'},
            {'city': 'Vancouver', 'code': 'ca'},
            {'city': 'Winnipeg', 'code': 'ca'},
            {'city': 'San Francisco', 'code': 'us'},
            {'city': 'Miami', 'code': 'us'},
            {'city': 'Seattle', 'code': 'us'},
            {'city': 'Mexicanos', 'code': 'mx'},
            {'city': 'Panama City', 'code': 'pa'},
            {'city': 'Buenos Aires', 'code': 'ar'},
            {'city': 'Santiago', 'code': 'cl'},
            {'city': 'London', 'code': 'gb'},
            {'city': 'Madrid', 'code': 'es'},
            {'city': 'Tripoli', 'code': 'ly'},
            {'city': 'Cape Town', 'code': 'za'},
            {'city': 'Cairo', 'code': 'eg'},
            {'city': 'Dubai', 'code': 'ae'},
            {'city': 'Ankara', 'code': 'tr'},
            {'city': 'Istanbul', 'code': 'tr'},
            {'city': 'Helsinki', 'code': 'fi'},
            {'city': 'Moscow', 'code': 'ru'},
            {'city': 'Mumbai', 'code': 'in'},
            {'city': 'Kathmandu', 'code': 'np'},
            {'city': 'Bangkok', 'code': 'th'},
            {'city': 'Jakarta', 'code': 'id'},
            {'city': 'Melbourne', 'code': 'au'},
            {'city': 'Xianggaang', 'code': 'cn'}#,
            #{'city': 'Shanghai', 'code': 'cn'},
            #{'city': 'Ulaanbaator', 'code': 'mn'},
            #{'city': 'Irkutsk', 'code': 'ru'},
            #{'city': 'Tokyo', 'code': 'jp'},
            #{'city': 'Sydney', 'code': 'au'},
            #{'city': 'Christchurch', 'code': 'nz'}
        ]

    def getNewsCountryCity(self, city, country_code):
        (lat, long) = self.getCoords(country_code, city)
        ''' returns a list of news articles '''
        headers = { 'Ocp-Apim-Subscription-Key': self.news_sub_key }
        params = { 'q': city, 'count': 5 }
        r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/news/search',
            headers=headers,
            params=params)
        if r.status_code != 200:
            print "error calling news: {}".format(r.status_code)
            return
        json_news = r.json()['value']
        news_list = [News(j['name'], j['url'], j['description'], j['datePublished'], location=city, lat=lat, long=long) for j in json_news]
        return news_list

    def getNewsCountry(self, country_code):
        country = self.getCountry(country_code)
        (lat, long) = self.getCoordsCountry(country_code)
        ''' returns a list of news articles '''
        headers = { 'Ocp-Apim-Subscription-Key': self.news_sub_key }
        params = { 'q': country }
        r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/news/search',
            headers=headers,
            params=params)
        if r.status_code != 200:
            print "error calling news: {}".format(r.status_code)
            return
        json_news = r.json()['value']
        news_list = [News(j['name'], j['url'], j['description'], j['datePublished'], location=country, lat=lat, long=long) for j in json_news]
        return news_list

    def addSentiments(self, news):
        ''' adds sentiment scores to news '''
        news = news[:1000]
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

    def writeToFile(self, news):
        with self.lock:
            open('events_write.txt', 'w').close()
            with open('events_write.txt', 'w') as f:
                for n in news:
                    json.dump(n.__dict__, f)
                    f.write('\n')
        return

    def getCountriesFromFile(self):
        code_to_countries = {}
        with open('countryinfo.txt') as tsv:
            for line in csv.reader(tsv, delimiter='\t'):
                code = line[0].lower().strip()
                country = line[4].strip()
                code_to_countries[code] = country
        return code_to_countries

    def getCityCoordsFromFile(self):
        coords = {}
        with open('worldcitiespop.txt') as tsv:
            for line in csv.reader(tsv, delimiter=','):
                code = line[0].strip()
                city = line[2].strip()
                lat = line[5]
                long = line[6]
                coords[(code, city)] = (line[5], line[6])
        return coords

    def getCoordsFromFile(self):
        code_to_coords = {}
        with open('worldcitiespop.txt') as tsv:
            for line in csv.reader(tsv, delimiter=','):
                code = line[0].strip()
                lat = line[5]
                long = line[6]
                code_to_coords[code] = (lat, long)
        return code_to_coords

    def getCountry(self, code):
        '''Return the country corresponding to the ISO 2-letter country code'''
        if code not in self.code_to_countries:
            print 'no such country'
            return
        return self.code_to_countries[code]

    def getCoordsCountry(self, code):
        '''Returns (latitude, longitude) within the given country'''
        return self.code_to_coords[code]

    def getCoords(self, code, city):
        '''Returns (latitude, longitude) within the given country'''
        return self.codecity_to_coords[(code, city)]

    def calculate(self):
        news = []
        for obj in self.cityList:
            news += self.getNewsCountryCity(obj['city'], obj['code'])
            print "got news for {}".format(obj['city'])
        self.addSentiments(news)
        # magical clustering
        self.writeToFile(news)
