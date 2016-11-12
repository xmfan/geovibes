class News(object):
    def __init__(self, name, url, description, datePublished, location=None, sentiment=None):
        self.name = name
        self.url = url
        self.description = description
        self.datePublished = datePublished
        self.location = location
        self.sentiment = sentiment
