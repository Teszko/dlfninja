from lxml import html, etree
import os.path

from dlfninja.helpers import xpath_query, query_url_overview, query_date_overview, \
    query_name_overview, get_page_from_file, request_page_content, write_page_content_to_file, \
    xpath_query_single_element
from dlfninja.program import Program
from dlfninja.episode import Episode

XPATH_SUBTREE_PROGRAM = '//*[@id="content"]/div/section[1]/div[1]/article'

DLF_URL = 'http://www.deutschlandfunk.de/'


programs = []


def query_name_episode(html_tree):
    return xpath_query_single_element(html_tree, '//div[2]/h3/a/span/text()')


def query_url_episode(html_tree):
    return xpath_query_single_element(html_tree, '//div[2]/h3/a/@href')


def update_episode_list(program, html_tree):
    program.clear_episodes()
    episode_trees = xpath_query(html_tree, '//*[@id="content"]/div/section[1]/div[1]/ul/li')
    for i, episode_tree in enumerate(episode_trees):
        new_episode = Episode(id=i)
        subtree = etree.ElementTree(episode_tree)
        new_episode.set_name(query_name_episode(subtree))
        new_episode.set_url(query_url_episode(subtree))
        program.add_episode(new_episode)


def print_programs():
    for program in programs:
        print(program)


def get_page_tree(url):
    """Returns the html tree for a given url and caches the page"""
    file_name = url.split('/')[-1]
    if os.path.isfile('data/'+file_name):
        page = get_page_from_file('data/'+file_name)
    else:
        page = request_page_content(url)
        write_page_content_to_file('data/'+file_name, page.content)
    html_tree = html.fromstring(page.content)
    return html_tree


def update_programs_list(overview_tree):
    """Scrap programs from DLF page 'Alle Sendungen'"""
    del programs[:]
    program_trees = xpath_query(overview_tree, XPATH_SUBTREE_PROGRAM)
    for i, program_tree in enumerate(program_trees):
        new_program = Program(id=i)
        subtree = etree.ElementTree(program_tree)
        new_program.set_name(query_name_overview(subtree))
        new_program.set_date(query_date_overview(subtree))
        new_program.set_url(query_url_overview(subtree))
        programs.append(new_program)
