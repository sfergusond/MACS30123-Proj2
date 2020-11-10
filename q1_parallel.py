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

def scrape_book(book_id):
    book_url = base_url + f'catalogue/{book_id}'
    r = requests.get(book_url)
    r.encoding = 'utf-8'
    html_soup = BeautifulSoup(r.text, 'html.parser')

    main = html_soup.find(class_='product_main')
    book = {}
    book['book_id'] = book_id
    book['title'] = main.find('h1').get_text(strip=True)
    book['price'] = main.find(class_='price_color').get_text(strip=True)
    book['stock'] = main.find(class_='availability').get_text(strip=True)
    book['rating'] = ' '.join(main.find(class_='star-rating') \
                        .get('class')).replace('star-rating', '').strip()
    book['img'] = html_soup.find(class_='thumbnail').find('img').get('src')
    desc = html_soup.find(id='product_description')
    book['description'] = ''
    if desc:
        book['description'] = desc.find_next_sibling('p') \
                                  .get_text(strip=True)
    book_product_table = html_soup.find(text='Product Information').find_next('table')
    for row in book_product_table.find_all('tr'):
        header = row.find('th').get_text(strip=True)
        # Since we'll use the header as a column, clean it a bit
        # to make sure SQLite will accept it
        header = re.sub('[^a-zA-Z]+', '_', header)
        value = row.find('td').get_text(strip=True)
        book[header] = value
    
    return book

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
book_list = list(itertools.chain(*book_list)) # flatten list
db['books'].insert_many(book_list)

t1 = time.time()
print(f'Finished finding books in {t1 - t0} seconds')

# Scrape each book
lambda_tasks, result = [], []
for i in range(0, 4):
    chunk = book_list[i::4]
    lambda_tasks.append(pwex.map(scrape_book, chunk))

# Wait for all scrapes to complete
for future in lambda_tasks:
    result.extend(pywren.get_all_results(future))

# Add scrape info to database
db['book_info'].insert_many(result)
print(results[:10])

t2 = time.time()
print(f'Finished scraping individual books in {t2 - t1} seconds')
print(f'Total time: {t2-t0} seconds')