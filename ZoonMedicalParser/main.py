import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import unquote


def write_json(data):
    with open('ZoonMedicalParser//result2.json', 'a', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_html(url):
    # url = 'https://spb.zoon.ru/medical/?action=listJson&type=service'
    # params = {'need[]': 'items','search_query_form': 1, 'page': 1}
    # response = requests.post(url, params=params)
    # print(response.url)
    response = requests.get(url)
    if 'json' in response.headers['Content-Type']:
        json_data = response.json()
        if json_data['success']:
            return json_data['html']
        return None
    else:
        return response.text

def get_cards(html):
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.find_all('div', class_='minicard-item__container')
    return cards


def get_card_info(html):
    soup = BeautifulSoup(html, 'lxml')

    title = soup.find('div', class_='service-page-header').find('h1').text.strip()

    rating = soup.find('span', class_='rating-value').get_text(strip=True)

    review_count = soup.find('span', class_='mr10').find_next_sibling().get_text(strip=True)

    phones = soup.find('div', class_='service-phones-box').find_all('span', class_='js-phone')#.find('a').get('href').split(':')[1]
    phones = [phone.find('a').get('href').split(':')[1] for phone in phones]

    address = soup.find('address', class_='iblock').get_text()

    try:
        website_full_url = soup.find('div', class_='service-website-value').find('a').get('href')
        if 'token' in website_full_url:
            website = website_full_url.split('?')[0]
        elif 'redirect' in website_full_url:
            website = unquote(website_full_url).split('=')[1].split('&')[0] # re.findall(r'to=((http|https)://.+?)&', url)
    except:
        website = 'Вебсайт отсутствует'

    try:
        social_networks = soup.find('div', class_='z-text--13').find_all('a')
        social_networks = [unquote(net.get('href')).split('?to=')[1].split('&')[0] for net in social_networks]
    except:
        social_networks = 'Страницы в соц. сетях отсутствуют'

    data = {
        'title': title,
        'rating': rating,
        'review_count': review_count,
        'phones': phones,
        'address': address,
        'website': website,
        'social_networks': social_networks
    }

    return data
    

def main():
    all_cards = []
    page = 1

    while True:
        url = f'https://spb.zoon.ru/medical/?action=listJson&type=service&need%5B%5D=items&search_query_form=1&page={page}'
        html = get_html(url)
        if html:
            page += 1
            cards = get_cards(html)
            all_cards.extend(cards)
        else:
            break
    
    data = []
    for card in all_cards:
        url = card.find('a', class_='title-link').get('href')
        print(url)
        html = get_html(url)
        card_info = get_card_info(html)
        card_info.update({'url': url})
        data.append(card_info)
    

    write_json(data)

if __name__ == '__main__':
    main()