import requests
import dataset
import re
import time
import pywren
import itertools
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

db = dataset.connect('sqlite:///books.db')
base_url = 'http://books.toscrape.com/'
pwex = pywren.default_executor()
r = requests.get(base_url)
html_soup = BeautifulSoup(r.text, 'html.parser')

def scrape_books(url):
    result = []

    r = requests.get(url)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    for book in html_soup.select('article.product_pod'):
        # For now, we'll only store the books url
        book_url = book.find('h3').find('a').get('href')
        book_url = urljoin(url, book_url)
        path = urlparse(book_url).path
        book_id = path.split('/')[2]
        result.append({'book_id': book_id, 'last_seen': datetime.now()})

    return result

# Scrape the pages in the catalogue
inp = input('Do you wish to re-scrape the catalogue (y/n)? ')
t0 = time.time()

# Get number of pages to iterate over
pages = html_soup.select('li.current')
pages = int(pages[0].getText().split()[-1])

# Get a list of URLs to map over
catalogue_urls = [base_url + f'catalogue/page-{i}.html' for i in range(1, pages + 1)]

# Scrape every result page using Lambda
book_list = pywren.get_all_results(pwex.map(scrape_books, catalogue_urls))
db['books'].insert_many(list(itertools.chain(*book_list)))

t1 = time.time()
print(f'Finished finding books in {t1 - t0} seconds')

t2 = time.time()
print(f'Finished scraping individual books in {t2 - t1} seconds')
print(f'Total time: {t2-t0} seconds')