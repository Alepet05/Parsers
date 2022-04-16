import requests
from bs4 import BeautifulSoup
import re
import csv
import json

def write_csv(result):
    with open('SteamParser//result.csv', 'w', encoding='utf-8') as f:
        fields = ['title', 'release_date', 'reviews_count', 'genres']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerows(result)

def write_json(result):
    with open('SteamParser//result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False) 

def get_html(url: str):
    """Возвращает html-код страницы
    """
    response = requests.get(url)
    return response.text

def get_game_info(html: str):
    """Возвращает информацию об игре
    """
    soup = BeautifulSoup(html, 'lxml')

    try:
        title = soup.find('h4', class_='hover_title').text.strip()
    except:
        title = ''

    try:
        release_date = soup.find('div', class_='hover_release').get_text(strip=True).split(':')[-1]
    except:
        release_date = ''

    try:
        reviews = soup.find('div', class_='hover_review_summary').text
    except:
        reviews = ''
        reviews_count = ''
    else:
        pattern = r'\d+'
        reviews_count = int(''.join(re.findall(pattern, reviews)))

    try:
        genres = soup.find_all('div', class_='app_tag')
    except:
        genres = ''
    else:
        genres_text = [genre.text for genre in genres]
        genres = ', '.join(genres_text)

    data = {
        'title': title,
        'release_date': release_date,
        'reviews_count': reviews_count,
        'genres': genres
    }

    return data

def get_games(html: str):
    """Возвращает список игр на странице
    """
    soup = BeautifulSoup(html, 'lxml')
    games = soup.find_all('a', class_='ds_collapse_flag')
    return games

def main():
    all_games = []
    start = 0
    tag = 'survival'
    url = f'https://store.steampowered.com/search/results/?query&start={start}&count=100&term={tag}&infinite=0'
    
    # получаем список игр до тех пор, пока его длина не равна 0 
    while True:
        html = get_html(url)
        games = get_games(html)
        # если нашли игры, то расширяем список всех игр
        if games:
            all_games.extend(games)
            start += 100
            url = f'https://store.steampowered.com/search/results/?query&start={start}&count=100&term={tag}&infinite=0'
        else:
            break

    result = []

    for game in all_games:
        id = game.get('data-ds-appid')
        url = f'https://store.steampowered.com/apphoverpublic/{id}'
        html = get_html(url)
        data = get_game_info(html)
        result.append(data)
    
    write_csv(result)
    write_json(result)

if __name__ == '__main__':
    main()