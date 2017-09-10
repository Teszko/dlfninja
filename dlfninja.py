import curses

import dlfninja.core as dlf
import dlfninja.curses as dlfcurses
import dlfninja.audio as audio


def main(stdscr):

    stdscr.keypad(True)
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()

    scr_height = curses.LINES
    scr_width = curses.COLS

    dlfcurses.init_overview_menu(dlf.programs, scr_width, scr_height)

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
            dlfcurses.active_menu.expand_element()
        elif c == curses.KEY_LEFT:
            dlfcurses.active_menu = dlfcurses.overview_menu
        elif c == ord('s'):
            if audio.is_playing():
                audio.null()
            else:
                audio.null()

        stdscr.refresh()
        dlfcurses.active_menu.draw()
        banner.draw()


if __name__ == '__main__':
    overview_tree = dlf.get_page_tree('http://www.deutschlandfunk.de/sendungen-a-z.348.de.html')
    dlf.update_programs_list(overview_tree)

    audio.init_player()

    curses.wrapper(main)
