class News(object):
    def __init__(self, name, url, description, datePublished, location=None, sentiment=None):
        self.name = name
        self.url = url
        self.description = description
        self.datePublished = datePublished
        self.location = location
        self.sentiment = sentiment
    #def __repr__(self):
        #return #u'name: ' + self.name#; +\
               #u'url: ' + utf(self.url) +\
               #u'description: ' + utf(self.description) +\
               #u'datePublished: ' + utf(self.datePublished) +\
               #u'location: ' + (self.location if self.location is not None else u'N/A' )+\
               #u'sentiment: ' + (self.sentiment if self.location is not None else u'N/A');

