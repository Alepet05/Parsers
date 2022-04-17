import requests
from bs4 import BeautifulSoup
import json
import csv


def get_html(url):
    response = requests.get(url)
    print(response.status_code)
    return response.text
    
def write_csv(products_info):
    with open('FoodParser//result.csv', 'a', newline='', encoding='utf-8') as f:
        fields = ['url', 'title', 'calories', 'proteins', 'fats', 'carbohydrates']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerows(products_info)

def write_json(products_info):
    with open('FoodParser//result.json', 'a', encoding='utf-8') as f:
        json.dump(products_info, f, indent=4, ensure_ascii=False) 

def get_products_data(html):
    soup = BeautifulSoup(html, 'lxml')

    alert_block = soup.find('div', class_='uk-alert-danger')
    if alert_block:
        return None

    products_info = []

    trs = soup.find('table', class_='mzr-tc-group-table').find('tbody').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        product = tds[0]
        url = 'https://health-diet.ru' + product.find('a').get('href')
        title = product.find('a').get_text(strip=True)# .replace(',', '')
        calories = tds[1].get_text(strip=True)
        proteins = tds[2].get_text(strip=True)
        fats = tds[3].get_text(strip=True)
        carbohydrates = tds[4].get_text(strip=True)

        product_info = {
            'url': url,
            'title': title,
            'calories': calories,
            'proteins': proteins,
            'fats': fats,
            'carbohydrates': carbohydrates
        }
    
        products_info.append(product_info)

    return products_info

def get_all_categories(html):
    soup = BeautifulSoup(html, 'lxml')

    categories = soup.find_all('div', class_='mzr-tc-group-item')
    return categories


def main():
    url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
    html = get_html(url)
    categories = get_all_categories(html)
    for category in categories:
        url = 'https://health-diet.ru' + category.find('a', class_='mzr-tc-group-item-href').get('href')
        html = get_html(url)
        products_info = get_products_data(html)
        write_json(products_info)
        write_csv(products_info)

if __name__ == '__main__':
    main()