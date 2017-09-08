import requests
from lxml import html, etree
from .program import Program
import pickle


programs = []


def write_page_content_to_file(file, page_content):
    with open(file, 'wb') as f:
        pickle.dump(page_content, f)


def get_page_from_file(file):
    page = lambda: None
    with open(file, 'rb') as f:
        page.content = pickle.load(f)
    return page


def request_page_content(url):
    req = requests.get(url)
    return req


def get_page_tree(url):
    """Returns the html tree for a given url"""
    # page = request_page_content(url)
    # write_page_to_file('data/overview_html.txt', page.content)
    page = get_page_from_file('data/overview_html.txt')
    # noinspection PyUnresolvedReferences
    html_tree = html.fromstring(page.content)
    return html_tree


def xpath_query(html_tree, xpath_str):
    """Apply xpath query to html tree, return list of elements"""
    return html_tree.xpath(xpath_str)


def xpath_query_single_element(html_tree, xpath_str):
    query = xpath_query(html_tree, xpath_str)
    query_result = None
    if len(query):
        query_result = query[0]
    return query_result


def query_name_overview(subtree):
    program_name = xpath_query_single_element(subtree, '//h3/text()')
    return program_name


def query_date_overview(subtree):
    program_date = xpath_query_single_element(subtree, '//span[@class="date"]/text()')
    return program_date


def update_programs_list(overview_tree):
    """Scrap programs from DLF page 'Alle Sendungen'"""
    program_trees = xpath_query(overview_tree, '//*[@id="content"]/div/section[1]/div[1]/article')
    for i, program_tree in enumerate(program_trees):
        new_program = Program()
        subtree = etree.ElementTree(program_tree)
        new_program.set_name(query_name_overview(subtree))
        new_program.set_date(query_date_overview(subtree))
        print(new_program)
