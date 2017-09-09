import pickle

import requests

XPATH_URL_OVERVIEW = '//ul/li/a[text()="Nachhören"]/@href'

XPATH_DATE_OVERVIEW = '//span[@class="date"]/text()'

XPATH_NAME_OVERVIEW = '//h3/text()'


def write_page_content_to_file(file, page_content):
    with open(file, 'wb') as f:
        pickle.dump(page_content, f)


def get_page_from_file(file):
    page = lambda: None
    with open(file, 'rb') as f:
        page.content = pickle.load(f)
    return page


def xpath_query(html_tree, xpath_str):
    """Apply xpath query to html tree, return list of elements"""
    return html_tree.xpath(xpath_str)


def xpath_query_single_element(html_tree, xpath_str):
    query = xpath_query(html_tree, xpath_str)
    query_result = None
    if len(query):
        query_result = query[0]
    return query_result


def query_url_overview(subtree):
    program_url = xpath_query_single_element(subtree, XPATH_URL_OVERVIEW)
    return program_url


def query_date_overview(subtree):
    program_date = xpath_query_single_element(subtree, XPATH_DATE_OVERVIEW)
    return program_date


def query_name_overview(subtree):
    program_name = xpath_query_single_element(subtree, XPATH_NAME_OVERVIEW)
    return program_name


def request_page_content(url):
    req = requests.get(url)
    return req
