import requests
from bs4 import BeautifulSoup
import json

def get_herb_info(herb_name):
    url = f'https://www.drugs.com/npp/{herb_name}.html'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to get page for {herb_name}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    content_box_div = soup.find('div', {'class': 'contentBox'})

    if content_box_div:
        h3s = [tag.get_text(strip=True) for tag in content_box_div.find_all('h3')]
        ps = [tag.get_text(strip=True) for tag in content_box_div.find_all('p')]
        content = h3s + ps
    else:
        print(f"No contentBox found for {herb_name}")
        return None

    return {'name': herb_name, 'content': content}

herbs = ['reishi-mushroom', 'turmeric', 'echinacea']
herb_data = {}

for herb in herbs:
    info = get_herb_info(herb)
    if info is not None:
        herb_data[herb] = info
        print(herb + ':' + "\n" +  json.dumps(herb_data[herb], indent=4))

with open('herb_data.json', 'w') as f:
    json.dump(herb_data, f, indent=4)
