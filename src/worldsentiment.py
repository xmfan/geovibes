from news import News
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

def getCities():
    cityList = []
    i = 0
    for key, val in codecity_to_coords.iteritems():
        if i == 3000:
            obj = {}
            obj['city'] = val
            obj['code'] = key
            cityList.append(obj)
            i = 0
        i+=1
    print len(cityList)

def getNewsCountryCity(city, country_code):
    (lat, long) = getCoords(country_code, city)
    ''' returns a list of news articles '''
    headers = { 'Ocp-Apim-Subscription-Key': news_sub_key }
    params = { 'q': city, 'count': 10 }
    r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/news/search',
        headers=headers,
        params=params)
    if r.status_code != 200:
        print "error calling news: {}".format(r.status_code)
        return
    json_news = r.json()['value']
    news_list = [News(j['name'], j['url'], j['description'], j['datePublished'], location=city, lat=lat, long=long) for j in json_news]
    return news_list


def addSentiments(news):
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
    return news

def writeToFile(news):
    i = 0
    with open('location_sentiment.txt', 'w') as f:
        for n in news:
            if i == 0:
                i += 1
            else:
                f.write(', ')
            json.dump(n.__dict__, f)

def getCountriesFromFile():
    code_to_countries = {}
    with open('countryinfo.txt') as tsv:
        for line in csv.reader(tsv, delimiter='\t'):
            code = line[0].lower().strip()
            country = line[4].strip()
            code_to_countries[code] = country
    return code_to_countries

def getCityCoordsFromFile():
    coords = {}
    with open('worldcitiespop.txt') as tsv:
        for line in csv.reader(tsv, delimiter=','):
            code = line[0].strip()
            city = line[2].strip()
            lat = line[5]
            long = line[6]
            coords[(code, city)] = (line[5], line[6])
    return coords

def getCoordsFromFile():
    code_to_coords = {}
    with open('worldcitiespop.txt') as tsv:
        for line in csv.reader(tsv, delimiter=','):
            code = line[0].strip()
            lat = line[5]
            long = line[6]
            code_to_coords[code] = (lat, long)
    return code_to_coords

def getCountry(code):
    '''Return the country corresponding to the ISO 2-letter country code'''
    if code not in code_to_countries:
        print 'no such country'
        return
    return code_to_countries[code]

def getCoordsCountry(code):
    '''Returns (latitude, longitude) within the given country'''
    return code_to_coords[code]

def getCoords(code, city):
    '''Returns (latitude, longitude) within the given country'''
    return codecity_to_coords[(code, city)]

def calculate(cities):
    news = []
    ind = 0
    locsents = []
    for obj in cities:
        news = getNewsCountryCity(obj['city'], obj['code'])
        addSentiments(news)
        sentiments = [x.sentiment for x in news]
        avg = sum(sentiments) / len(sentiments)
        ls = LocationSentiment(news.lat, news.long, news.location, avg)
        locsents.append(ls)
    writeToFile(locsents)

class LocationSentiment(object):
    def __init__(self, lat, long, city, sentiment):
        self.lat = lat
        self.long = long
        self.city = city
        self.sentiment = sentiment

news_sub_key = '305dc95e236544168d39b8d0549a8725'
text_sub_key = '7b20e9c1ffa8470cab2e3b6245148cf6'
code_to_countries = getCountriesFromFile()
codecity_to_coords = getCityCoordsFromFile()

cityList = [{}]

c = getCities()
calculatel(c)
