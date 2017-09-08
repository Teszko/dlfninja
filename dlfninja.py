import dlfninja.core as dlf

if __name__ == '__main__':
    overview_tree = dlf.get_page_tree('http://www.deutschlandfunk.de/sendungen-a-z.348.de.html')
    dlf.update_programs_list(overview_tree)
