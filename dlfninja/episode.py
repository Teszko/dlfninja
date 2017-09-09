class Episode:
    name = None
    date = None
    url = None
    id = None
    length = None
    author = None
    available_until = None
    program = None

    def __init__(self, name=None, id=None):
        if name is not None:
            self.name = name
        self.id = id

    def __str__(self):
        return "<name=\"%s\" date=\"%s\" url=\"%s\">" % (self.name, self.date, self.url)

    def set_name(self, name):
        self.name = name

    def set_url(self, url):
        self.url = url

    def set_date(self, date):
        self.date = date
