class Program:
    name = 'unknown'
    url = None
    date = None
    details = None
    id = None
    episodes = []
    disabled = False

    def __init__(self, name=None, id=None):
        if name is not None:
            self.name = name
        self.id = id

    def __str__(self):
        return "<id=\"%d\" name=\"%s\" date=\"%s\" url=\"%s\">" % (self.id, self.name, self.date, self.url)

    def set_name(self, name):
        self.name = name

    def set_url(self, url):
        self.url = url

    def set_date(self, date):
        self.date = date

    def set_details(self, details):
        self.details = details

    def add_episode(self, episode):
        self.episodes.append(episode)

    def clear_episodes(self):
        del self.episodes[:]

    def print_episodes(self):
        for episode in self.episodes:
            print(episode)

    def set_disabled(self):
        self.disabled = True
