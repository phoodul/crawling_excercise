''' 파이썬 웹 크롤링 '''
#1. 필요한 모듈 불러오기
import requests
from bs4 import BeautifulSoup as bs
import lxml                    #conda install lxml(library extended markup language)이 필요함
import time                    #timesleep을 설정하기 위해 필요

#2 web page 불러오기 (예제: )
url =  'https://search.naver.com/search.naver'
params = {'query': '부산날씨'} # {'query': '', 'page': }
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'} 
#headers는 사람이 동작하는 것처럼 서버를 속이기 위함이다. 

response = requests.get(url, params=params, headers=headers)
# 응답이 정상인지 확인
print(response.status_code) # 200이 나와야 함

    
# 이 결과 response는 Byte 상태로 reponse.text를 하면 utf-8로 인코딩한 후 string으로 디코딩해서 text로 보여준다. 
'''여러 페이지에서 scrawling 하는 방법

# 1. 수집하고 싶은 페이지 범위 설정
start_page = 1
end_page = 5

for page in range(start_page, end_page + 1):
    url = f"https://example.com/list/"
    params = {'query': '검색어', 'page': page}    
# 3. 서버에 요청 (User-Agent 설정은 필수 매너!)
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 여기에 데이터 추출 로직 작성
        print(f"현재 {page}페이지 수집 중...")
        
# 4. 서버 과부하 방지를 위한 휴식 (중요!)
        time.sleep(1) 
    else:
        print(f"{page}페이지를 불러오지 못했습니다.")
        break
'''

#3 parsing
'''
파싱(Parsing): 무의미하게 나열된 텍스트에서 <html>, <body>, <a>, <div> 같은 태그들을 구분해냅니다.
트리(Tree) 구조 생성: HTML의 계층 구조(부모-자식 관계)를 파악하여 메모리에 올립니다.
검색 기능 활성화: 이제 파이썬의 find(), select() 같은 메서드를 사용해서 특정 태그만 쏙쏙 뽑아낼 수 있는 상태가 됩니다.
'''
soup = bs(response.text, 'lxml')     #'lxml' 대신에 'html.parser'를 사용하기도 하나, 최근에는 'lxml'을 사용하는 추세임
# print(soup)
#4 find/find_all/select_one/select
'''
find/find_all은 BeautifulSoup 기반 method임
select_one/select는 CSS 선택자 방식으로 이 방식이 더 추천됨 (Chrome 개발자 도구에서 Copy Selector로 바로 복사해서 사용할 수 있어서 생산성이 훨씬 더 좋다.)
1) find('tag명', class_=''): 조건에 맞는 첫 번째 요소 하나만 가져온다. 요소가 없으면 None을 반환
    예: soup.find('p', class_='title')
2) find_all('tag명', class_=''): 조건에 맞는 모든 요소를 리스트 형태로 가져온다. 리스트가 없으면 []를 반환
3) select_one('CSS경로'): CSS 선택자로 지정한 첫 번째 요소를 가져온다.
4) select('CSS경로'): CSS 선택자로 지정한 모든 요소를 리스트로 가져온다.
    예: soup.select_one('div > ul .item') (div 안의 ul안의 item 클래스)
'''
temp = soup.select_one('.open .temperature_text strong').get_text() #.text를 해도 결과는 동일하다
temp = soup.select_one('.open .temperature_text strong').text
#select_one 안에 넣을 값을 찾기 위해 Web Scraper를 활용하는 게 한 가지 방법이 된다. 
print(temp)
'''
Tip: copy selector결과가 너무 길다면 에러가 난다. 
    크롬 개발자 도구에서 Copy Selector로 가져온 값은 때때로 너무 길어서 비효율적입니다. a.p-name 처럼 핵심 클래스명만 찍어서 시도해 보세요.
'''
