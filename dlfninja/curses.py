import curses

BANNER = """
 ______   _____     ________    ____  _____  _____  ____  _____     _____     _      
|_   _ `.|_   _|   |_   __  |  |_   \|_   _||_   _||_   \|_   _|   |_   _|   / \     
  | | `. \ | |       | |_ \_|    |   \ | |    | |    |   \ | |       | |    / _ \    
  | |  | | | |   _   |  _|       | |\ \| |    | |    | |\ \| |   _   | |   / ___ \   
 _| |_.' /_| |__/ | _| |_       _| |_\   |_  _| |_  _| |_\   |_ | |__' | _/ /   \ \_ 
|______.'|________||_____|     |_____|\____||_____||_____|\____|`.____.'|____| |____|
                                                                               v0.1.0"""


class Banner:
    win = None

    def __init__(self):
        self.win = curses.newwin(10, 86, ((curses.LINES // 4) - 5), (curses.COLS - 86)//2 - 1)

    def draw(self):
        self.win.addstr(0, 0, BANNER, curses.color_pair(1))
        self.win.refresh()


class Entry:
    text = None
    text_right = None
    url = None

    def set_text(self, text):
        self.text = text

    def set_text_right(self, text):
        if text is not None:
            self.text_right = text.strip().rstrip('.')

    def set_url(self, url):
        self.url = url


class Menu:
    win = None
    entries = []
    selected = 0
    title = None
    subtext = None
    width = 0
    height = 0
    pos_x = 0
    pos_y = 0
    max_lines = 0

    def set_title(self, title):
        self.title = title

    def set_subtext(self, subtext):
        self.subtext = subtext

    def scroll_down(self):
        self.selected = (self.selected + 1) % len(self.entries)

    def scroll_up(self):
        self.selected = self.selected - 1
        if self.selected < 0:
            self.selected = len(self.entries) - 1

    def init(self, x, y, w, h):
        self.height = h
        self.width = w
        self.pos_x = x
        self.pos_y = y
        self.win = curses.newwin(h, w, y, x)
        self.win.border(0)
        self.max_lines = self.height - 2

    def draw(self):
        if self.win is None:
            return None

        self.win.clear()
        self.win.border(0)

        if self.title is not None:
            self.win.addstr(0, 2, self.title, curses.color_pair(1))

        if self.subtext is not None:
            self.win.addstr(self.height - 1, 2, self.subtext, curses.color_pair(1))

        if self.subtext is not None:
            pass

        # for i, entry in enumerate(self.entries):
        for i in range(0, self.max_lines):
            if self.selected < self.max_lines - self.max_lines // 2:
                j = i
            else:
                j = i + self.selected - self.max_lines + 1 + self.max_lines // 2

            if j >= len(self.entries):
                break

            entry = self.entries[j]
            if j == self.selected:
                if entry.text is not None:
                    self.win.addstr(i+1, 1, "-> " + entry.text, curses.color_pair(1))
                if entry.text_right is not None:
                    self.win.addstr(i+1, self.width - len(entry.text_right) - 2, entry.text_right, curses.color_pair(1))
            else:
                if entry.text is not None:
                    self.win.addstr(i+1, 3, entry.text)
                if entry.text_right is not None:
                    self.win.addstr(i+1, self.width - len(entry.text_right) - 2, entry.text_right)

        self.win.refresh()

    def add_entry(self, entry):
        self.entries.append(entry)
