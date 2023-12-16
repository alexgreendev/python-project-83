import requests
import bs4
from textwrap import wrap


def get_data(url):
    """Make request to url and return responce

    Args:
        url (str):

    Returns:
        requests.Responce
    """
    try:
        responce = requests.get(url)
    except requests.exceptions.ConnectionError:
        return False
    try:
        responce.raise_for_status()
    except requests.HTTPError:
        return False
    return parse_data(responce)


def parse_data(data):
    """Parse status code, title, h1 and description from responce
    and return tuple.

    Args:
        data (requests.Responce):

    Returns:
        tuple
    """
    max_len = 254
    html = bs4.BeautifulSoup(data.text, features="html.parser")
    status = data.status_code
    title = html.title
    h1 = html.find('h1')
    desc = html.find("meta", attrs={'name': 'description'})
    return (status,
            (wrap(h1.get_text(), max_len)[0] if h1.get_text() else '') if h1 else '',
            wrap(title.string, max_len)[0] if title else '',
            wrap(desc['content'], max_len)[0] if desc else '')
