import requests
from bs4 import BeautifulSoup
import json

class EnsembleCard:
    def __init__(self, name, unbloomed_card, bloomed_card, table_data):
        self.name = name
        self.unbloomed_card = unbloomed_card
        self.bloomed_card = bloomed_card
        self.table_data = self.process_table_data(table_data)

    def process_table_data(self, table_data):
        processed_data = {}
        for key, values in table_data.items():
            processed_data[key] = [self.process_value(value) for value in values]
        return processed_data

    def process_value(self, value):
        parts = value.split()
        if len(parts) == 2:
            category, amount = parts
            return {category: amount}
        return {}

    def __str__(self):
        return f"EnsembleCard(name={self.name}, " \
               f"unbloomed_card={self.unbloomed_card}, bloomed_card={self.bloomed_card}, table_data={self.table_data})"

# 크롤링할 페이지 URL
url = 'https://ensemble-stars.fandom.com/wiki/(Crown_of_the_Blue_Sea)_Tori_Himemiya'

# 사이트에 접속
response = requests.get(url)

# 응답이 정상적인지 확인
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # 데이터 추출 및 객체 생성
    card_name_tag = soup.find('h1', class_='page-header__title')
    card_name = card_name_tag.text.strip() if card_name_tag else "Unknown"

    # 추가로 가져올 이미지 데이터
    unbloomed_card_tag = soup.find('div', class_='card-single card-unbloomed')
    unbloomed_card = unbloomed_card_tag.find('img')['src'] if unbloomed_card_tag else None

    bloomed_card_tag = soup.find('div', class_='card-single card-bloomed')
    bloomed_card = bloomed_card_tag.find('img')['src'] if bloomed_card_tag else None

    # 추가로 가져올 테이블 데이터 (data-item-name="card-stats-music" 속성을 가진 section 내부의 테이블)
    music_section = soup.find('section', {'data-item-name': 'card-stats-music'})
    table_data = {}
    if music_section:
        table = music_section.find('table')
        if table:
            tbody = table.find('tbody')
            if tbody:
                for tr in tbody.find_all('tr'):
                    th = tr.find('th')
                    tds = tr.find_all('td')
                    if th and tds:
                        key = th.text.strip()
                        values = [td.text.strip() for td in tds]
                        table_data[key] = values

        # 객체 생성
        ensemble_card = EnsembleCard(name=card_name,
                                     unbloomed_card=unbloomed_card, bloomed_card=bloomed_card, table_data=table_data)

        # JSON 형식으로 변환
        ensemble_card_json = json.dumps(ensemble_card.__dict__, ensure_ascii=False, indent=2)

        # JSON 파일에 쓰기
        output_file_path = 'Tori.json'
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(ensemble_card_json)

        print(f'Data saved to {output_file_path}')
    else:
        print('Error: Section not found with data-item-name="card-stats-music".')
else:
    print(f'Error: {response.status_code}')
