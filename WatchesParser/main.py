import requests
from bs4 import BeautifulSoup
import json


def get_html(url):
    response = requests.get(url)
    return response.text

def write_json(data):
    with open('WatchesParser//result.json', 'a', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_watches(html): 
    soup = BeautifulSoup(html, 'lxml')

    watches = soup.find_all('a', class_='product-item__link')
    return watches

def get_watch_info(watch):
    url = 'https://shop.casio.ru' + watch.get('href')
    title = watch.find('p', class_='product-item__articul').get_text(strip=True)
    price = watch.find('p', class_='product-item__price').get_text(strip=True).split('.')[1]

    data = {
        'url': url,
        'title': title,
        'price': price
    }

    return data

def main():
    page = 1
    all_wathces = []

    while True:
        url = f'https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/?PAGEN_1={page}'
        html = get_html(url)
        watches = get_watches(html)

        if watches and watches[0] not in all_wathces:
            print(page)
            all_wathces.extend(watches)
            page += 1
        else:
            break
    
    data = []
    for watch in all_wathces:
        watch_info = get_watch_info(watch)
        data.append(watch_info)
    
    write_json(data)

if __name__ == '__main__':
    main()