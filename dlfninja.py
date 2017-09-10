import curses

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

import dlfninja.core as dlf
import dlfninja.curses as dlfcurses
from dlfninja.curses import init_overview_menu, init_episodes_menu


player = None


def on_tag(bus, msg):
    taglist = msg.parse_tag()
    print('on_tag:')
    for key in taglist.keys():
        print('\t%s = %s' % (key, taglist[key]))


def init_player():
    global player
    Gst.init([])

    music_stream_uri = 'http://ondemand-mp3.dradio.de/file/dradio/2017/09/09/info_update_09092017_dlf_20170909_1653_81d0dbb4.mp3 '
    # creates a playbin (plays media form an uri)
    player = Gst.ElementFactory.make("playbin", "player")

    # set the uri
    player.set_property('uri', music_stream_uri)

    # start playing
    player.set_state(Gst.State.PLAYING)

    # listen for tags on the message bus; tag event might be called more than once
    bus = player.get_bus()
    bus.enable_sync_message_emission()
    bus.add_signal_watch()
    bus.connect('message::tag', on_tag)

def main(stdscr):

    stdscr.keypad(True)
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()

    scr_height = curses.LINES
    scr_width = curses.COLS

    init_overview_menu(dlf.programs, scr_width, scr_height)

    banner = dlfcurses.Banner()

    stdscr.refresh()
    dlfcurses.overview_menu.draw()
    banner.draw()

    # init_player()

    while True:
        c = stdscr.getch()

        if c == ord('q'):
            break  # Exit Program
        elif c == curses.KEY_UP or c == ord('k'):
            dlfcurses.active_menu.scroll_up()
        elif c == curses.KEY_DOWN or c == ord('j'):
            dlfcurses.active_menu.scroll_down()
        elif c == curses.KEY_RIGHT:
            dlfcurses.overview_menu.expand_element()
        elif c == curses.KEY_LEFT:
            dlfcurses.active_menu = dlfcurses.overview_menu

        stdscr.refresh()
        dlfcurses.active_menu.draw()
        banner.draw()


if __name__ == '__main__':
    overview_tree = dlf.get_page_tree('http://www.deutschlandfunk.de/sendungen-a-z.348.de.html')
    dlf.update_programs_list(overview_tree)
    # dlf.print_programs()

    # program_tree = dlf.get_page_tree('http://www.deutschlandfunk.de/dlf-audio-archiv.2386.de.html?drau:broadcast_id=101')
    # dlf.update_episode_list(dlf.programs[11], program_tree)
    # dlf.programs[11].print_episodes()
    curses.wrapper(main)
