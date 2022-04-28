from textwrap import indent
import requests
from bs4 import BeautifulSoup
import json


def get_html(url, city_code=2398):
    cookies = {'mg_geo_id': str(city_code)}
    response = requests.get(url, cookies=cookies)
    return response.text

def write_json(data):
    with open('MagnitParser//result.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_discount_products(html):
    soup = BeautifulSoup(html, 'lxml')

    all_products = soup.find_all('a', class_='card-sale_catalogue')
    discount_products = list(filter(lambda product: product.find('div', class_='label__price_old'), all_products))
    return discount_products

def get_product_info(product):
    title = product.find('div', class_='card-sale__title').text.strip()
    discount = product.find('div', class_='card-sale__discount').text.strip()

    old_price_block = product.find('div', class_='label__price_old')
    old_price_integer = old_price_block.find('span', class_='label__price-integer').text
    old_price_decimal = old_price_block.find('span', class_='label__price-decimal').text
    old_price = f'{old_price_integer}.{old_price_decimal}'

    current_price_block = product.find('div', class_='label__price_new')
    current_price_integer = current_price_block.find('span', class_='label__price-integer').text
    current_price_decimal = current_price_block.find('span', class_='label__price-decimal').text
    current_price = f'{current_price_integer}.{current_price_decimal}'

    date_block = product.find('div', class_='card-sale__date')
    since = date_block.find('p').text
    until = date_block.find('p').find_next_sibling('p').text
    date = f'{since} {until}'

    product_info = {
        'title': title,
        'old_price': old_price,
        'current_price': current_price,
        'discount': discount,
        'date': date
    }

    return product_info

def main():
    url = 'https://magnit.ru/promo/'
    html = get_html(url)
    discount_products = get_discount_products(html)

    data = []
    for product in discount_products:
        product_info = get_product_info(product)
        data.append(product_info)

    write_json(data)

if __name__ == '__main__':
    main()