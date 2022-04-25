import requests
from bs4 import BeautifulSoup
import json


def get_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.66',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'X-Is-Ajax-Request': 'X-Is-Ajax-Request',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.get(url, headers=headers)
    content = response.json()
    return content

def get_pages_count():
    url = 'https://roscarservis.ru/catalog/legkovye/?isAjax=true&PAGEN_1=1'
    content = get_content(url)
    return content['pageCount']

def write_json(data):
    with open('WheelsParser//result.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_wheels(content):
    wheels = content['items']
    return wheels

def get_wheels_info(wheel):
    url = 'https://roscarservis.ru' + wheel['url']
    img = 'https://roscarservis.ru' + wheel['imgSrc']
    season = wheel['season']
    price = wheel['price']
    title = wheel['name']
    total_amount = 0
    confirmed_stores = []
    potential_stores = ['discountStores', 'fortochkiStores', 'commonStores']

    for store in potential_stores:
        if wheel[store]:
            for confirmed_store in wheel[store]:
                store_info = {
                    'store_amount': confirmed_store['AMOUNT'],
                    'store_name': confirmed_store['STORE_NAME'],
                    'store_price': confirmed_store['PRICE']
                }
                confirmed_stores.append(store_info)
                total_amount += int(store_info['store_amount'])
    data = {
        'url': url,
        'img': img,
        'season': season,
        'title': title,
        'price': price,
        'stores': confirmed_stores,
        'total_amount': total_amount
    }

    return data

def main():
    page = 1
    all_wheels = []
    pages_count = get_pages_count()

    for page in range(1, pages_count+1):
        url = f'https://roscarservis.ru/catalog/legkovye/?isAjax=true&PAGEN_1={page}'
        content = get_content(url)
        wheels = get_wheels(content)
        all_wheels.extend(wheels)

    data = []
    for wheel in all_wheels:
        wheel_info = get_wheels_info(wheel)
        data.append(wheel_info)

    write_json(data)

if __name__ == '__main__':
    main()
