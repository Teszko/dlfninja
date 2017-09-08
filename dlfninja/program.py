class Program:
    name = 'unknown'
    url = None
    date = None
    nachhoeren_url = None
    details = None

    def __init__(self, name=None):
        if name is not None:
            self.name = name

    def __str__(self):
        return "<name=\"%s\" date=\"%s\" url=\"%s\">" % (self.name, self.date, self.url)

    def set_name(self, name):
        self.name = name

    def set_url(self, url):
        self.url = url

    def set_date(self, date):
        self.date = date

    def set_nachhoeren_url(self, nachhoeren_url):
        self.nachhoeren_url = nachhoeren_url

    def set_details(self, details):
        self.details = details

