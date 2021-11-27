import os
import sys

import requests
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options


def get_links(url: str) -> list[str]:
    """Find and return all hyperlinks.

    Args:
        url: string of html a tag.

    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """
    gecko_path = os.path.dirname(__file__) + "/geckodriver"  # Concat file path
    options = Options()
    options.add_argument("--headless")
    service = Service(gecko_path)  # Create a service from file
    browser = webdriver.Firefox(service=service, options=options)
    browser.get(url)
    all_a_tags = browser.find_elements("tag name", "a")
    obtained_urls = []
    for tag in all_a_tags:
        href_link = tag.get_attribute("href").split("#")
        obtained_urls.append(href_link[0])
    browser.quit()
    return obtained_urls


def is_valid_url(url: str) -> bool:
    """Test if a url is valid and reachable or not.

    Args:
        url: a url to test.

    Returns:
        Return True if the URL is OK, False otherwise.
        Also return False is the URL has invalid syntax.
    """
    try:
        requests.head(url)
        return True
    except ConnectionError:
        return False


def invalid_urls(urllist: list[str]) -> list[str]:
    """Validate the urls in urllist and return a new list containing
    the invalid or unreachable urls.

    Args:
        urllist: a list containing string of url.

    Returns:
        List of invalid urls.
    """
    invalid = []
    for url in urllist:
        if not is_valid_url(url):
            invalid.append(url)
    return invalid


if __name__ == '__main__':
    """Running from command line."""
    args_amount = len(sys.argv)
    if args_amount != 2 or not is_valid_url(sys.argv[1]):
        print("Usage:  python3 link_scan.py url")
        sys.exit()
    all_links = get_links(sys.argv[1])
    bad_links = invalid_urls(all_links)
    print()
    for link in all_links:
        print(link)
    if len(bad_links) > 0:
        print("\nBad Links:")
        for link in bad_links:
            print(link)
