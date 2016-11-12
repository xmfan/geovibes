class News(object):
    def __init__(self, name, url, description, mentions, datePublished, location=None, sentiment=None):
        self.name = name
        self.url = url
        self.description = description
        self.mentions = mentions
        self.datePublished = datePublished
        self.location = location
        self.sentiment = sentiment

