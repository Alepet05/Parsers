import re
import requests
from bs4 import BeautifulSoup
import json


def get_html(url):
    response = requests.get(url)
    return response.text

def write_json(data):
    with open('BooksParser//result2.json', 'a', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_pagination(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-numbers').find_all('a', class_='pagination-number__text')
    last_page = pages[-1].get_text(strip=True)
    return int(last_page)

def get_books(html):
    soup = BeautifulSoup(html, 'lxml')
    books = soup.find('table', class_='products-table').find('tbody').find_all('tr')
    return books

def get_books_info(html):
    books_info = []
    soup = BeautifulSoup(html, 'lxml')
    books = soup.find('table', class_='products-table').find('tbody').find_all('tr')
    for book in books:
        tds = book.find_all('td')
        url = 'https://www.labirint.ru' + tds[0].find('a', class_='book-qtip').get('href')
        title = tds[0].find('a', class_='book-qtip').get_text(strip=True)
        author = tds[1].get_text(strip=True)
        publishing = tds[2].get_text(strip=True)
        current_price = int(''.join(re.findall('\d+', tds[3].find('span', class_='price-val').get_text(strip=True))))
        try:
            discount = int(re.search('\d+', tds[3].find('span', class_='price-val').get('title')).group())
        except:
            discount = 'Скидка отсутствует'

        data = {
            'url': url,
            'title': title,
            'publishing': publishing,
            'author': author,
            'price': current_price,
            'discount': discount
        }

        books_info.append(data)

    return books_info

def main():
    all_books = []
    url = 'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&page=1&display=table'
    html = get_html(url)
    pages_count = get_pagination(html)

    for page in range(1, pages_count):
        url = f'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&page=1&display=table&page={page}'
        html = get_html(url)
        books_info = get_books_info(html)
        all_books.extend(books_info)

    write_json(all_books)

if __name__ == '__main__':
    main()