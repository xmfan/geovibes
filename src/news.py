class News(object):
    def __init__(self, name, url, description, datePublished, location=None, lat=None, long=None, sentiment=None):
        self.name = name
        self.url = url
        self.description = description
        self.datePublished = datePublished
        self.location = location
        self.lat = lat
        self.long = long
        self.sentiment = sentiment
