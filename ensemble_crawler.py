import requests
from bs4 import BeautifulSoup
import os
import re

# 크롤링할 페이지 URL
url = 'https://ensemble-stars.fandom.com/wiki/(Leader_of_Heaven)_Eichi_Tenshouin'

# 사이트에 접속
response = requests.get(url)

# 응답이 정상적인지 확인
if response.status_code == 200:
    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 특정 패턴을 제외한 이미지 태그 찾기
    img_tags = soup.find_all('img', src=re.compile(r'https://static.wikia.nocookie.net/ensemble-stars/images/(?!(e/e6/Site-logo\.png)).*'))

    # 이미지 저장할 폴더 생성
    folder_name = 'test'
    os.makedirs(folder_name, exist_ok=True)

    # 이미지 다운로드
    for idx, img_tag in enumerate(img_tags):
        img_url = img_tag['src']

        # 이미지 파일 이름 추출
        img_filename = f'image_{idx + 1}.png'

        # 이미지 다운로드
        img_data = requests.get(img_url).content

        # 이미지 파일 저장
        with open(os.path.join(folder_name, img_filename), 'wb') as img_file:
            img_file.write(img_data)

        print(f'이미지 {idx + 1} 다운로드 및 저장 완료: {img_filename}')

    # 특정 클래스를 가진 div 안의 table 데이터 추출
    pi_data_value = soup.find('div', class_='pi-data-value')
    if pi_data_value:
        table = pi_data_value.find('table')
        if table:
            data = []
            for tr in table.find_all('tr'):
                row_data = []
                for td in tr.find_all(['th', 'td']):
                    span = td.find('span')
                    if span:
                        row_data.append(span.get_text(strip=True))
                    else:
                        row_data.append(td.get_text(strip=True))
                data.append(row_data)

            # 데이터 출력 (이 부분을 원하는 대로 수정하세요)
            for row in data:
                print(row)
else:
    print(f'Error: {response.status_code}')
