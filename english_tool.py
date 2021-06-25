from string import punctuation

import requests
from bs4 import BeautifulSoup


def get_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_words(soup):
    for tag in soup(["a", "span", "code", "strong", "b"]):
        tag.extract()
    lines = []
    for line in soup(["p"]):
        lines.append(line.extract().text)
    text = "".join(lines)
    for item in punctuation:
        text = text.replace(item, " ")
    return text


def get_translate(words):
    class TempTranlsate:

        def __init__(self, word):
            self.en = word.lower()
            self.ru = f"^{word.lower()}^"

    return [TempTranlsate(word) for word in words]


def get_words_from_url(url):
    words = get_translate(get_words(get_page(url)).split())
    return [word for word in words if word.en.isalpha()]


if __name__ == '__main__':
    url = "https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/"
    words = get_words_from_url(url)
    for word in words:
        print(word.en, word.ru)
