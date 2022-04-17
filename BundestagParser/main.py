import requests
from bs4 import BeautifulSoup
import json
import csv


def get_html(url):
    response = requests.get(url)
    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    return response.text

def write_json(data):
    with open('result.json', 'a', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def write_csv(data):
    with open('result.csv', 'a', newline='', encoding='utf-8') as f:
        fields = ['name', 'fraction']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerows(data)

def get_members(html):
    soup = BeautifulSoup(html, 'lxml')
    members = soup.find_all('div', class_='bt-teaser-person-text')
    return members

def get_member_data(member):
    name = member.find('h3').get_text(strip=True)
    fraction = member.find('p').get_text(strip=True)

    data = {
        'name': name,
        'fraction': fraction
    }

    return data

def main():
    offset = 0
    all_members = []

    while True:
        url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset={offset}'
        html = get_html(url)
        members = get_members(html)
        if members:
            all_members.extend(members)
            offset += 12
        else:
            break

    result = []
    for member in all_members:
        data = get_member_data(member)
        result.append(data)

    write_json(result)
    write_csv(result)

if __name__ == '__main__':
    main()
