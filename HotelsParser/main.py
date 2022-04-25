import requests
from bs4 import BeautifulSoup
import json


def get_html(url):
    response = requests.get(url)
    return response.text

def write_json(data):
    with open('HotelsParser//result.json', 'a', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_hotel_info(hotel):
    title = hotel.find('a', class_='hotel_name').get_text()
    resort = hotel.find('a', class_='resort').get_text()
    country = hotel.find('a', class_='country').get_text()
    try:
        rating = hotel.find('li', title='Рейтинг').get_text()
    except:
        rating = ''

    data = {
        'title': title,
        'resort': resort,
        'country': country,
        'rating': rating
    }

    return data

def get_hotels(html):
    soup = BeautifulSoup(html, 'lxml')
    hotels = soup.find_all('div', class_='hotel_card_dv')
    return hotels

def main():
    offset = 0
    all_hotels = []

    while True:
        url = f'https://api.rsrv.me/hc.php?a=hc&most_id=1317&l=ru&sort=most&hotel_link=/hotel/id/%HOTEL_ID%&r=654227328&s={offset}'
        html = get_html(url)
        hotels = get_hotels(html)
        if hotels:
            all_hotels.extend(hotels)
            offset += 30
        else:
            break

    data = []
    for hotel in all_hotels:
        hotel_info = get_hotel_info(hotel)
        data.append(hotel_info)
    
    write_json(data)

if __name__ == '__main__':
    main()