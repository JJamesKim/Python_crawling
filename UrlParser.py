import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import re


def clean_str(text):
    pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '<[^>]*>'         # HTML 태그 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '[^\w\s\n]'         # 특수기호제거
    text = re.sub(pattern=pattern, repl='', string=text)
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]','', string=text)
    text = re.sub('\n', '.', string=text)
    return text

url_list = ["http://www.newsworks.co.kr/news/articleView.html?idxno=723632", "http://www.energy-news.co.kr/news/articleView.html?idxno=90754", "http://www.m-i.kr/news/articleView.html?idxno=1022018", "http://www.biztribune.co.kr/news/articleView.html?idxno=281290", "http://www.koreastocknews.com/news/articleView.html?idxno=93902", "http://news.mt.co.kr/mtview.php?no=2023082111411439951", "http://www.daejonilbo.com/news/articleView.html?idxno=2097191", "https://www.theguru.co.kr/news/article.html?no=59386", "https://www.theguru.co.kr/news/article.html?no=55603", "http://www.greened.kr/news/articleView.html?idxno=303933", "http://www.g-enews.com/ko-kr/news/article/news_all/202309071336007093e8b8a793f7_1/article.html", "https://biz.chosun.com/industry/company/2023/07/25/I5MSI7G2MRBGBHYSVTOHOAPD6Q/?utm_source=naver&utm_medium=original&utm_campaign=biz", "http://www.edaily.co.kr/news/newspath.asp?newsid=03181606635710600", "https://www.delighti.co.kr/news/articleView.html?idxno=61547", "http://www.newsis.com/view/?id=NISX20230104_0002148336&cID=10401&pID=10400", "https://www.busan.com/view/busan/view.php?code=2023082416433231777", "http://www.energydaily.co.kr/news/articleView.html?idxno=139501", "http://www.newsbrite.net/news/articleView.html?idxno=178256", "http://www.fnnews.com/news/202308080907434278"]


# 각 URL에 대해 데이터를 저장할 리스트 초기화
data_list = []

# 최대 길이의 p 태그를 저장할 변수
max_length_p = None
max_length = 0


for url in url_list:
    try:
        # URL에서 페이지 가져오기
        response = requests.get(url, verify=False)
        response.raise_for_status()  # 예외 발생 시 중단

        # BeautifulSoup를 사용하여 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # <p> 태그 추출
        p_tags = soup.find_all('p')
        #print(p_tags)
        # 반환값은 리스트

        # <p> 태그의 텍스트를 리스트에 추가
        #p_texts = [p.get_text() for p in p_tags]


        p_texts = []
        for p in p_tags:
            p_clean = clean_str(p.get_text(strip=True)).replace(u'\xa0', u' ')
            current_length = len(p_clean)
            if current_length > max_length:
                max_length = current_length
                max_length_p = p.text
            p_texts.append(max_length_p)
            #print(p_texts)


        # 데이터 리스트에 추가
        data_list.append({'URL': url, 'Paragraphs': p_texts})
        
        # max_len(p) finder 초기화
        max_length_p = None
        max_length = 0

    except requests.exceptions.RequestException as e:
        # 예외 발생 시 "can't enter into"를 저장
        print(f"Error accessing {url}: {e}")
        data_list.append({'URL': url, 'Paragraphs': "can't enter into"})
        sleep(1)


# 데이터프레임 생성
df = pd.DataFrame(data_list)

# CSV 파일로 저장
df.to_csv('contents_final.csv', index=False, mode='w', encoding='utf-8-sig')