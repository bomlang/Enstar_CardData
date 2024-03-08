from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json

class EnsembleCard:
    def __init__(self, name, unbloomed_card, bloomed_card, table_data):
        self.name = name
        self.unbloomed_card = unbloomed_card
        self.bloomed_card = bloomed_card
        self.table_data = table_data

    def __str__(self):
        return f"EnsembleCard(name={self.name}, " \
               f"unbloomed_card={self.unbloomed_card}, bloomed_card={self.bloomed_card}, table_data={self.table_data})"

# 크롬 드라이버 경로 설정 (본인의 환경에 맞게 설정)
chrome_driver_path = '/Users/holee/desktop/Ensamble/Ensemble_cardData/chromedriver-mac-arm64'

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument('--headless')  # 만약 화면이 필요 없다면 headless 모드로 설정

# 크롤링할 페이지 URL
url = 'https://ensemble-stars.fandom.com/wiki/(Crown_of_the_Blue_Sea)_Tori_Himemiya'

# Selenium으로 버튼 클릭하여 데이터 로드
with webdriver.Chrome(options=chrome_options, executable_path=chrome_driver_path) as driver:
    driver.get(url)

    # 두 번째 탭으로 이동
    music_tab = driver.find_element_by_css_selector('li[data-item-name="card-music"]')
    music_tab.click()

    # 페이지 소스를 BeautifulSoup으로 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 추가로 가져올 테이블 데이터 (두 번째 테이블 식별자 사용)
    second_table = soup.find('table', {'class': 'wikitable'})
    table_data = {}
    if second_table:
        tbody = second_table.find('tbody')
        if tbody:
            for tr in tbody.find_all('tr'):
                th = tr.find('th')
                tds = tr.find_all('td')
                if th and tds:
                    key = th.text.strip()
                    values = [td.text.strip() for td in tds]
                    table_data[key] = values

    # 추가로 가져올 이미지 데이터
    unbloomed_card_tag = soup.find('div', class_='card-single card-unbloomed')
    unbloomed_card = unbloomed_card_tag.find('img')['src'] if unbloomed_card_tag else None

    bloomed_card_tag = soup.find('div', class_='card-single card-bloomed')
    bloomed_card = bloomed_card_tag.find('img')['src'] if bloomed_card_tag else None

    # 객체 생성
    ensemble_card = EnsembleCard(name="Tori Himemiya",
                                 unbloomed_card=unbloomed_card, bloomed_card=bloomed_card, table_data=table_data)

    # JSON 형식으로 변환
    ensemble_card_json = json.dumps(ensemble_card.__dict__, ensure_ascii=False, indent=2)

    # JSON 파일에 쓰기
    output_file_path = 'torii.json'
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(ensemble_card_json)

    print(f'Data saved to {output_file_path}')
