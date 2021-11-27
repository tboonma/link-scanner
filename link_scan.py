from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from selenium.webdriver.firefox.options import Options


def get_links(url: str) -> list:
    """Find and return all hyperlinks.

    Args:
        url: string of html a tag.

    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """
    url = url.replace("'", "\"")  # prepare string before split to links
    split_url = url.split("\"")
    obtained_urls = []
    for link in split_url:
        if link.startswith("http://") or link.startswith("https://"):
            obtained_urls.append(link)
    if len(obtained_urls) > 0:
        return obtained_urls


print(get_links("<a href='https://kucafe.com/menu' href='http'>"))
