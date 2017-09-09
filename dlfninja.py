import dlfninja.core as dlf
from dlfninja.curses import Menu, Entry, Banner
import curses

def main(stdscr):
    stdscr.keypad(True)
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    stdscr.clear()

    scr_height = curses.LINES
    scr_width = curses.COLS

    menu = Menu()
    menu.init(0, scr_height // 2, scr_width, scr_height - scr_height // 2)
    menu.set_title(" Alle Sendungen ")
    menu.set_subtext(" quit(q)  play/pause(space) ")

    for prog in dlf.programs:
        entry = Entry()
        entry.set_text(prog.name)
        entry.set_text_right(prog.date)
        menu.add_entry(entry)

    banner = Banner()

    stdscr.refresh()
    menu.draw()
    banner.draw()
    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break  # Exit Program
        elif c == curses.KEY_UP or c == ord('k'):
            menu.scroll_up()
        elif c == curses.KEY_DOWN or c == ord('j'):
            menu.scroll_down()

        stdscr.refresh()
        menu.draw()
        banner.draw()


if __name__ == '__main__':
    overview_tree = dlf.get_page_tree('http://www.deutschlandfunk.de/sendungen-a-z.348.de.html')
    dlf.update_programs_list(overview_tree)
    # dlf.print_programs()

    program_tree = dlf.get_page_tree('http://www.deutschlandfunk.de/dlf-audio-archiv.2386.de.html?drau:broadcast_id=101')
    dlf.update_episode_list(dlf.programs[11], program_tree)
    # dlf.programs[11].print_episodes()
    curses.wrapper(main)
