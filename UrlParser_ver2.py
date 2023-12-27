import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import re

# 데이터를 가져올 URL 리스트
url_list = ["http://www.newsworks.co.kr/news/articleView.html?idxno=723632", "http://www.energy-news.co.kr/news/articleView.html?idxno=90754", "http://www.m-i.kr/news/articleView.html?idxno=1022018", "http://www.biztribune.co.kr/news/articleView.html?idxno=281290", "http://www.koreastocknews.com/news/articleView.html?idxno=93902", "http://news.mt.co.kr/mtview.php?no=2023082111411439951", "http://www.daejonilbo.com/news/articleView.html?idxno=2097191", "https://www.theguru.co.kr/news/article.html?no=59386", "https://www.theguru.co.kr/news/article.html?no=55603", "http://www.greened.kr/news/articleView.html?idxno=303933", "http://www.g-enews.com/ko-kr/news/article/news_all/202309071336007093e8b8a793f7_1/article.html", "https://biz.chosun.com/industry/company/2023/07/25/I5MSI7G2MRBGBHYSVTOHOAPD6Q/?utm_source=naver&utm_medium=original&utm_campaign=biz", "http://www.edaily.co.kr/news/newspath.asp?newsid=03181606635710600", "https://www.delighti.co.kr/news/articleView.html?idxno=61547", "http://www.newsis.com/view/?id=NISX20230104_0002148336&cID=10401&pID=10400", "https://www.busan.com/view/busan/view.php?code=2023082416433231777", "http://www.energydaily.co.kr/news/articleView.html?idxno=139501", "http://www.newsbrite.net/news/articleView.html?idxno=178256", "http://www.fnnews.com/news/202308080907434278"]

# 최종 분문 데이터를 저장할 리스트 정의
target_list = []

"""
for url in url_list:
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # 예외 발생 시 중단

        soup = BeautifulSoup(response.text, 'html.parser')

        p_tags = soup.select('div > p')
        print(p_tags)
        print(len(p_tags))
        br_tags = soup.select('div > br')
        print(len(br_tags))

        p_texts = []
        br_texts = []

        for p, br in zip(p_tags, br_tags):
            p_clean = p.get_text(strip=True).replace(u'\xa0', u' ')
            p_texts.append(p_clean)
            br_clean = br.get_text(strip=True).replace(u'\xa0', u' ')
            br_texts.append(br_clean)

        # 리스트에 추가
        if (len(p_tags) >= len(br_tags)):
            data_list.append({'URL': url, 'Paragraphs': p_texts})
        elif (len(p_tags) == 0 and len(br_tags) == 0):
            print("크롤링 실패")
            data_list.append({'URL': url, 'Paragraphs': "Data Crawling failed"})
        else:
            data_list.append({'URL': url, 'Paragraphs': br_texts})
        
        #print(news_texts)


    except requests.exceptions.RequestException as e:
        # 예외 발생 시 "can't enter into"를 저장
        print(f"Error accessing {url}: {e}")
        data_list.append({'URL': url, 'Paragraphs': "can't enter into URL"})

"""

def is_valid_tag(tag):
    # Check if the tag has non-empty text and does not contain unwanted text
    return tag and tag.strip() != '' and not re.search(r'<[^>]*>', tag)

for url in url_list:
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # 예외 발생 시 중단

        soup = BeautifulSoup(response.text, 'html.parser')

        p_tags = soup.find_all('div > p', lambda tag: is_valid_tag(tag))
        div_near_br_tags = soup.find_all('div > br', lambda tag: is_valid_tag(tag))
        section_tags = soup.find_all('section > p', lambda tag: is_valid_tag(tag))
        article_tags = soup.find_all('article > p', lambda tag: is_valid_tag(tag))
        
        print("%d번째 URL의 태그 요소 출력 \n " % (int(url_list.index(url))+1))
        print(len(p_tags))
        print(len(div_near_br_tags))
        print(len(section_tags))
        print(len(article_tags))
        print("-" *30 )

        # 텍스트가 존재하는 태그의 개수를 비교. 가장 많은 태그가 해당 URL의 본문이라고 가정 
        """
        if len(p_tags) >= len(br_tags):
            target_tags = p_tags
        
        #elif (len(p_tags) == 0 and ):
        #    target_tags
        
        else:
            target_tags = br_tags

        texts = []
"""
        # 가장 요소의 개수가 많은 리스트를 찾습니다.

        all_types_tags = [p_tags, div_near_br_tags, section_tags, article_tags]
        largest_tag = max(all_types_tags, key=len)
        max_element_count = 0

        for target_tag in all_types_tags:
            if len(target_tag) > max_element_count:
                max_element_count = len(target_tag)
                largest_variable = target_tag
                print(largest_variable)
        
        #print("\n가장 요소의 개수가 많은 변수: %d : %s" (largest_variable, max_element_count))
        
        # 최종 리스트에 추가

        # 원하는 텍스트로 정제
        for t in largest_variable:
            t_clean = t.get_text(strip=True).replace(u'\xa0', u' ')
            target_list.append(t_clean)

    except requests.exceptions.RequestException as e:
        # 예외 발생 시 "can't enter into"를 저장
        print(f"Error accessing {url}: {e}")
        target_list.append({'URL': url, 'Paragraphs': "can't enter into URL"})

# 데이터프레임 생성
df = pd.DataFrame(target_list)

# CSV 파일로 저장
df.to_csv('contents_finder.csv', index=False, mode='w', encoding='utf-8-sig')