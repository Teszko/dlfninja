import curses

import dlfninja.core as dlf
import dlfninja.curses as dlfcurses
from dlfninja.curses import init_overview_menu, init_episodes_menu


def main(stdscr):

    stdscr.keypad(True)
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    stdscr.clear()

    scr_height = curses.LINES
    scr_width = curses.COLS

    init_overview_menu(dlf.programs, scr_width, scr_height)

    banner = dlfcurses.Banner()

    stdscr.refresh()
    dlfcurses.overview_menu.draw()
    banner.draw()
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

    program_tree = dlf.get_page_tree('http://www.deutschlandfunk.de/dlf-audio-archiv.2386.de.html?drau:broadcast_id=101')
    dlf.update_episode_list(dlf.programs[11], program_tree)
    # dlf.programs[11].print_episodes()
    curses.wrapper(main)
