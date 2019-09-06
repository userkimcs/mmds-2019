import hashlib
from bs4 import BeautifulSoup
import urllib.parse
import requests


def to_sha1(text):
    sha = hashlib.sha1(text.encode('utf-8'))
    return sha.hexdigest()


def get_absolute_links(url):
    """
    Get all absolute link from given url
    :param url:
    :return:
    """
    rq = requests.get(url)
    soup = BeautifulSoup(rq.text)
    all_links = list()
    for atag in soup.find_all('a'):
        link = urllib.parse.urljoin(url, atag.get('href'))
        all_links.append(link)

    return all_links

