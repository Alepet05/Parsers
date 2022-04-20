import requests
from bs4 import BeautifulSoup
import re
import json


def get_html(url):
    response = requests.get(url).json()
    return response['html']

def write_json(data):
    with open('FestivalsParser//result.json', 'a', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_contact_info(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    data = {}
    contact_info_block = soup.find('h2', text=re.compile('Venue contact details and info')).find_next_sibling()
    items = contact_info_block.find_all('p')
    for item in items:
        couple = item.get_text(strip=True).split(':')
        key = couple[0].lower()
        val = couple[-1].replace('/', '', 2)
        data[key] = val
    return data

def get_festival_data(html):
    soup = BeautifulSoup(html, 'lxml')

    festival_data = soup.find('div', class_='top-info-cont')
    if not festival_data:
        return False

    title = festival_data.find('h1').get_text(strip=True)
    date = festival_data.find('h3').get_text(strip=True)
    place = festival_data.find_all('p')[-2].get_text()
    contact_info_url = 'https://www.skiddle.com' + festival_data.find_all('p')[-2].find('a').get('href')
    contact_info = get_contact_info(contact_info_url)
    min_age = festival_data.find_all('p')[-1].get_text(strip=True).split(':')[-1]
    data = {
        'title': title,
        'date': date,
        'place': place,
        'min_age': min_age,
    }
    data.update(contact_info)
    return data

def get_festivals(html):
    soup = BeautifulSoup(html, 'lxml')

    urls = soup.find_all('a', class_='card-details-link')
    festivals = [url.get('href') for url in urls]
    return festivals

def main():
    all_festivals = []
    offset = 0

    while True:
        url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=12%20Nov%202021&to_date=&where%5B%5D=2&where%5B%5D=3&where%5B%5D=4&maxprice=500&o={offset}'
        html = get_html(url)
        festivals = get_festivals(html)
        if festivals:
            for festival in festivals:
                url = 'https://www.skiddle.com' + festival
                all_festivals.append(url)
            offset += 24
        else:
            break

    result = []
    for festival in all_festivals:
        html = get_html(festival)
        data = get_festival_data(html)
        if not data:
            continue
        data.update({'url': festival})
        result.append(data)
        
    write_json(result)

if __name__ == '__main__':
    main()