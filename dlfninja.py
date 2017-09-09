import dlfninja.core as dlf

if __name__ == '__main__':
    overview_tree = dlf.get_page_tree('http://www.deutschlandfunk.de/sendungen-a-z.348.de.html')
    dlf.update_programs_list(overview_tree)
    # dlf.print_programs()

    program_tree = dlf.get_page_tree('http://www.deutschlandfunk.de/dlf-audio-archiv.2386.de.html?drau:broadcast_id=101')
    dlf.update_episode_list(dlf.programs[11], program_tree)
    dlf.programs[11].print_episodes()
