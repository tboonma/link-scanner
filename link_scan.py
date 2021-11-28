import os
import sys
from urllib.request import urlopen
import requests
from urllib.error import HTTPError
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
    obtained_urls = set()
    for tag in all_a_tags:
        href_link = tag.get_attribute("href")
        # check if there's a link in href
        if not isinstance(href_link, str):
            continue
        href_link = href_link.split("?")  # remove parameters from link
        href_link = href_link[0].split("#")  # remove page fragments
        href_link = href_link[0]  # get link after sliced
        # check if it's not None and not empty string
        if len(href_link) < 4 and not href_link.startswith("http"):
            continue
        obtained_urls.add(href_link)
    browser.quit()
    return list(obtained_urls)


def is_valid_url(url: str) -> bool:
    """Test if a url is valid and reachable or not.

    Args:
        url: a url to test.

    Returns:
        Return True if the URL is OK, False otherwise.
        Also return False is the URL has invalid syntax.
    """
    try:
        with urlopen(url) as conn:
            conn.close()
        return True
    except HTTPError:
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


def is_html_page(url: str) -> bool:
    """Check whether URL is the html page or not.

    Args:
        url: url to check

    Returns:
        True if url is html, otherwise return false.
    """

    response = requests.head(url)
    return "text/html" in response.headers["content-type"]


if __name__ == '__main__':
    """Running from command line."""
    args_amount = len(sys.argv)
    url = sys.argv[1]
    if args_amount != 2 or not is_valid_url(url):
        print("Usage:  python3 link_scan.py url")
        sys.exit()
    if not is_html_page(url):
        print("URL is not HTML")
        sys.exit()
    all_links = get_links(url)
    print()
    for link in all_links:
        print(link)

    # get bad link
    bad_links = invalid_urls(all_links)
    if len(bad_links) > 0:
        print("\nBad Links:")
        for link in bad_links:
            print(link)
