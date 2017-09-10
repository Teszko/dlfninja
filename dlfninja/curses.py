import curses
from dlfninja.core import get_page_tree, update_episode_list
import dlfninja.audio as audio

BANNER = """
 ______   _____     ________    ____  _____  _____  ____  _____     _____     _      
|_   _ `.|_   _|   |_   __  |  |_   \|_   _||_   _||_   \|_   _|   |_   _|   / \     
  | | `. \ | |       | |_ \_|    |   \ | |    | |    |   \ | |       | |    / _ \    
  | |  | | | |   _   |  _|       | |\ \| |    | |    | |\ \| |   _   | |   / ___ \   
 _| |_.' /_| |__/ | _| |_       _| |_\   |_  _| |_  _| |_\   |_ | |__' | _/ /   \ \_ 
|______.'|________||_____|     |_____|\____||_____||_____|\____|`.____.'|____| |____|
                                                                               v0.1.0"""

overview_menu = None
active_menu = None
episodes_menu = None


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
    program = None

    def set_text(self, text):
        self.text = text

    def set_text_right(self, text):
        if text is not None:
            self.text_right = text.strip().rstrip('.')

    def set_url(self, url):
        self.url = url

    def set_program(self, program):
        self.program = program


class Menu:
    win = None
    entries = None
    selected = 0
    title = None
    subtext = None
    width = 0
    height = 0
    pos_x = 0
    pos_y = 0
    max_lines = 0
    type = None

    def __init__(self, type):
        self.entries = []
        self.type = type

    def set_title(self, title):
        self.title = title

    def set_subtext(self, subtext):
        self.subtext = subtext

    def scroll_down(self):
        num_elements = len(self.entries)
        if num_elements:
            self.selected = (self.selected + 1) % num_elements

    def scroll_up(self):
        num_elements = len(self.entries)
        if not num_elements:
            return None
        self.selected = self.selected - 1
        if self.selected < 0:
            self.selected = num_elements - 1

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

        for i in range(0, self.max_lines):
            j = self.max_lines * (self.selected // self.max_lines)
            if j+i >= len(self.entries):
                break

            entry = self.entries[j+i]
            if j+i == self.selected:
                if entry.text is not None:
                    self.win.addstr(i+1, 1, "> " + entry.text, curses.color_pair(1))
                if entry.text_right is not None:
                    self.win.addstr(i+1, self.width - len(entry.text_right) - 2, entry.text_right, curses.color_pair(1))
            else:
                color = curses.color_pair(0)
                if entry.program and entry.program.disabled:
                    color =  curses.color_pair(2)
                if entry.text is not None:
                    self.win.addstr(i+1, 3, entry.text, color)
                if entry.text_right is not None:
                    self.win.addstr(i+1, self.width - len(entry.text_right) - 2, entry.text_right, color)

        self.win.refresh()

    def add_entry(self, entry):
        self.entries.append(entry)

    def expand_element(self):
        selected_entry = self.entries[self.selected]
        if self.type == 'overview':
            if selected_entry.url is not None:
                init_episodes_menu(selected_entry, curses.COLS, curses.LINES)
        if self.type == 'episodes':
            if selected_entry.url is not None:
                audio.null()
                audio.set_uri(selected_entry.url)
                audio.play()


def init_overview_menu(programs, scr_width, scr_height):
    global overview_menu
    global active_menu
    overview_menu = Menu('overview')
    active_menu = overview_menu
    overview_menu.init(0, scr_height // 2, scr_width, scr_height - scr_height // 2)
    overview_menu.set_title(" Alle Sendungen({}) ".format(len(programs)))
    overview_menu.set_subtext(" quit(q)  play/pause(space) ")

    for i, prog in enumerate(programs):
        entry = Entry()
        entry.set_text(str(i+1)+"\t"+prog.name)
        entry.set_text_right(prog.date)
        entry.set_url(prog.url)
        entry.set_program(prog)
        overview_menu.add_entry(entry)


def init_episodes_menu(entry, scr_width, scr_height):
    global episodes_menu
    global active_menu
    active_menu.win.clear()
    episodes_menu = Menu('episodes')
    active_menu = episodes_menu

    episodes_tree = get_page_tree('http://www.deutschlandfunk.de/'+entry.url)
    update_episode_list(entry.program, episodes_tree)

    episodes_menu.init(0, scr_height // 2, scr_width, scr_height - scr_height // 2)
    episodes_menu.set_title(" {}({}) ".format(entry.text, len(entry.program.episodes)))
    episodes_menu.set_subtext(" zurück(left)  play/pause(space) ")
    episodes_menu.draw()

    for i, episode in enumerate(entry.program.episodes):
        ep = Entry()
        ep.set_text(str(i+1)+"\t"+episode.name)
        # ep.set_text_right(episode.date)
        ep.set_url(episode.url)
        # ep.set_program(episode)
        episodes_menu.add_entry(ep)
