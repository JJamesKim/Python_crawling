# 라이브러리 import
import os
import pandas as pd
import numpy as np

# 워닝 무시
import warnings
warnings.filterwarnings('ignore')

from selenium import webdriver  # 라이브러리(모듈) 가져오라
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
# from tqdm import tqdm_notebook
import re
from time import sleep
import time
from datetime import datetime, timedelta
today = datetime.today()
today = today.strftime("%Y-%m-%d")
today


file_name = input("Name of this file:  ")

"""
search_listA = ["DL이엔씨 CCUS 신사업 해외", "GS건설 CCUS 신사업 해외", "GS칼텍스 CCUS 신사업 해외", "LG화학 CCUS 신사업 해외", "SK E&S CCUS 신사업 해외", "SK 가스 CCUS 신사업 해외", "Sk 에코엔지니어링 CCUS 신사업 해외", 
                "SK 에코플랜트 CCUS 신사업 해외", "고등기술연구원 CCUS 신사업 해외", "고려아연 CCUS 신사업 해외", "LG화학 CCUS 신사업 해외", "SK E&S CCUS 신사업 해외", "SK 가스 CCUS 신사업 해외", "Sk 에코엔지니어링 CCUS 신사업 해외", 
                "SK 에코플랜트 CCUS 신사업 해외", "고등기술연구원 CCUS 신사업 해외", "고려아연 CCUS 신사업 해외", "두산에너빌러티 CCUS 신사업 해외", "두산지오솔루션 CCUS 신사업 해외", "롯데케미칼 CCUS 신사업 해외", "삼성물산 CCUS 신사업 해외", 
                "삼성엔지니어링 CCUS 신사업 해외", "삼성중공업 CCUS 신사업 해외", "에너지기술연구원 CCUS 신사업 해외", "코오롱 CCUS 신사업 해외", "파나시아 CCUS 신사업 해외", "포스코이앤씨 CCUS 신사업 해외", "포스코홀딩스 CCUS 신사업 해외", 
                "플랜텍 CCUS 신사업 해외", "한국가스공사 CCUS 신사업 해외", "한국가스기술공사 CCUS 신사업 해외", "한국가스안전공사 CCUS 신사업 해외", "한국남동발전 CCUS 신사업 해외", "한국남부발전 CCUS 신사업 해외", 
                "한국동서발전 CCUS 신사업 해외", "한국서부발전 CCUS 신사업 해외", "한국수력원자력 CCUS 신사업 해외", "한국조선해양 CCUS 신사업 해외", "한국중부발전 CCUS 신사업 해외", "한화솔루션 CCUS 신사업 해외", 
                "한화에너지 CCUS 신사업 해외", "한화오션 CCUS 신사업 해외", "한화임팩트 CCUS 신사업 해외", "한화파워시스템 CCUS 신사업 해외", "현대건설 CCUS 신사업 해외", "현대엔지니어링 CCUS 신사업 해외", "현대오일뱅크 CCUS 신사업 해외", 
                "현대제철 CCUS 신사업 해외", "현대중공업 CCUS 신사업 해외", "롯데정밀화학 CCUS 신사업 해외", "휴켐스 CCUS 신사업 해외", "E1 CCUS 신사업 해외", "SK 머트리얼즈 CCUS 신사업 해외", "SK 이노베이션  CCUS 신사업 해외", 
                "카본코 CCUS 신사업 해외", "석유공사 CCUS 신사업 해외", "로우카본 CCUS 신사업 해외", "포스코인터내셔널 CCUS 신사업 해외", "DL이엔씨 CCUS 투자계획 해외", "GS건설 CCUS 투자계획 해외", "GS칼텍스 CCUS 투자계획 해외", 
                "LG화학 CCUS 투자계획 해외", "SK E&S CCUS 투자계획 해외", "SK 가스 CCUS 투자계획 해외", "Sk 에코엔지니어링 CCUS 투자계획 해외", "SK 에코플랜트 CCUS 투자계획 해외", "고등기술연구원 CCUS 투자계획 해외", 
                "고려아연 CCUS 투자계획 해외", "LG화학 CCUS 투자계획 해외", "SK E&S CCUS 투자계획 해외", "SK 가스 CCUS 투자계획 해외", "Sk 에코엔지니어링 CCUS 투자계획 해외", "SK 에코플랜트 CCUS 투자계획 해외", 
                "고등기술연구원 CCUS 투자계획 해외", "고려아연 CCUS 투자계획 해외", "두산에너빌러티 CCUS 투자계획 해외", "두산지오솔루션 CCUS 투자계획 해외", "롯데케미칼 CCUS 투자계획 해외", "삼성물산 CCUS 투자계획 해외", 
                "삼성엔지니어링 CCUS 투자계획 해외", "삼성중공업 CCUS 투자계획 해외", "에너지기술연구원 CCUS 투자계획 해외", "코오롱 CCUS 투자계획 해외", "파나시아 CCUS 투자계획 해외", "포스코이앤씨 CCUS 투자계획 해외", 
                "포스코홀딩스 CCUS 투자계획 해외", "플랜텍 CCUS 투자계획 해외", "한국가스공사 CCUS 투자계획 해외", "한국가스기술공사 CCUS 투자계획 해외", "한국가스안전공사 CCUS 투자계획 해외", "한국남동발전 CCUS 투자계획 해외", 
                "한국남부발전 CCUS 투자계획 해외", "한국동서발전 CCUS 투자계획 해외", "한국서부발전 CCUS 투자계획 해외", "한국수력원자력 CCUS 투자계획 해외", "한국조선해양 CCUS 투자계획 해외", "한국중부발전 CCUS 투자계획 해외", 
                "한화솔루션 CCUS 투자계획 해외", "한화에너지 CCUS 투자계획 해외", "한화오션 CCUS 투자계획 해외", "한화임팩트 CCUS 투자계획 해외", "한화파워시스템 CCUS 투자계획 해외", "현대건설 CCUS 투자계획 해외", 
                "현대엔지니어링 CCUS 투자계획 해외", "현대오일뱅크 CCUS 투자계획 해외", "현대제철 CCUS 투자계획 해외", "현대중공업 CCUS 투자계획 해외", "롯데정밀화학 CCUS 투자계획 해외", "휴켐스 CCUS 투자계획 해외", 
                "E1 CCUS 투자계획 해외", "SK 머트리얼즈 CCUS 투자계획 해외", "SK 이노베이션  CCUS 투자계획 해외", "카본코 CCUS 투자계획 해외", "석유공사 CCUS 투자계획 해외", "로우카본 CCUS 투자계획 해외", "포스코인터내셔널 CCUS 투자계획 해외"
]
"""

search_listA = ["석유공사 CCUS 신사업 해외", "로우카본 CCUS 신사업 해외", "포스코인터내셔널 CCUS 신사업 해외"]

search_listB = ["탄소포집저장 투자", "CCU 투자 해외"]

search_list_Final = [search_listA, search_listB]

filtering_keyword_list = ["건립", "건설", "설립", "짓는다", "증설", "신설", "설비", "진출", "추진", "해외 투자", "해외 확장", "해외 확대", "합작법인", "합작", "투자", "업무협약", "수주", "출자", "구축", 
                          "사업참여", "구축추진", "FEED", "EPC", "실증", "상용화", "개발", "신사업", "생태계", "집중", "유치", "착수", "착공"
]


blacklist_keyword_list = ["모멘텀", "주가", "질주", "회복", "신년사", "결산", "평가", "취임", "기획", "신년", "주간추천종목", "종목", "주간", "월간", "주차", "핫클립", "동향", "일자", "특징주", "관련주", 
                          "총정리", "오늘의", "상한가", "하한가", "목표가", "기대", "주요기사", "CEO", "리포트", "Who Is", "증시", "실적", "강세", "약세", "주식", "반등", "매수", "매도", "폭락", "폭등", "매출"
]


for Selector in search_list_Final:
    # 검색어 타입에 따라 검색하는 페이지의 수를 유동화하기 // specific한 키워드는 검색 결과가 적을 것이므로 적게 스크랩 <-> broad한 키워드는 많이 스크랩 => for Efficiency
    print (Selector)
    print(search_listA)
    if Selector is search_listA:
        page_num = 3; page_num_A = 3
    elif Selector is search_listB:
        page_num = 20; page_num_B = 20
    else:
        pass
    for search in Selector:
        print("-" * 30)
        print('"'+ search + '"', '크롤링 시작')

        # 크롬창 띄우기
        driver = webdriver.Chrome()  # 윈도우 : "chromedriver.exe"
        driver.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}".format(search))
        time.sleep(3)

        # 옵션 클릭
        #option_bt = driver.find_element(By.CSS_SELECTOR,'.btn_option._search_option_open_btn')
        #option_bt.click()
        #time.sleep(1)

        # 기간 선택
        #driver.find_element(By.LINK_TEXT, '3개월').click() # 1시간, 1일, 1주, 1개월, 3개월, 6개월, 1년

        # page 수 확인
        page_count = driver.find_elements(By.CSS_SELECTOR,'.sc_page_inner .btn')
        page_check = len(page_count)
        print('페이지 수: ', page_check)

        time.sleep(1)

        
        # 데이터를 저장할 리스트 선언
        url_list = []
        title_list = []
        press_list = []
        date_list = []
        keyword_list = []
        content_list = []
        SDate_list = [] #스크랩한 날짜
        isfilter_list = []
        isBlacklist_list = []

        # 검색어별로 검색 가능한 페이지 수가 사전에 정의한 페이지 수보다 적을 수 있으므로, 페이지 size에 따라 탄력적으로 검색 페이지를 조정하는 예외 처리 로직
        if page_num >= page_check and page_num > 10:
            pass
        elif page_num >= page_check:
            page_num = page_check
        else:
            pass

        # 뉴스 전체 페이지를 돌면서 기사의 title, url 수집하기
        for i in tqdm(range(page_num), desc = "Page iteration status "):


            things = driver.find_elements(By.CSS_SELECTOR, '.news_tit')
            # print(things)

            # title에 essential이 들어있는 기사 추려내기
            in_title_list = []
            # ind_list = []

            for j, thing in enumerate(things):
                    title = thing.get_attribute('title')
                    in_title_list.append(thing)


            # url 수집
            for thing in in_title_list:
                title = thing.get_attribute('href')
                url_list.append(title)


            # 기사 제목 수집
            for thing in in_title_list:
                title = thing.get_attribute('title')   
                title_list.append(title)
                for keyword in filtering_keyword_list:
                    if keyword.strip() in title:
                        isfilter_list.append("success")
                        break
                else:
                    isfilter_list.append("fail")

                for Black_keyword in blacklist_keyword_list:
                    if Black_keyword.strip() in title:
                        isBlacklist_list.append("Blacklist")
                        break
                else:
                    isBlacklist_list.append("Not in Blacklist")

            # 신문사 수집
            press_raws = driver.find_elements(By.CSS_SELECTOR,'.info.press')
            for press in press_raws:
                press_list.append(press.text)

            # 날짜 수집
            date_raws = driver.find_elements(By.CSS_SELECTOR,'.info_group > span')
            for date in date_raws:
                if '전' in date.text or re.match(r'\d{4}\.\d{2}\.\d{2}', date.text):
                    date_list.append(date.text)

            #본문 일부 수집
            content_raws = driver.find_elements(By.CSS_SELECTOR, '.api_txt_lines')
            for content in content_raws:
                content_list.append(content.text)
                # 키워드 추가 (Pandas 각 열의 len 개수를 맞추기 위해 여기서 추가)
                keyword_list.append(search)
                # 크롤링 날짜 추가 (Pandas 각 열의 len 개수를 맞추기 위해 여기서 추가)
                SDate_list.append(today)

        
            print('')
            time.sleep(1)

            print(len(url_list), url_list)
            print("\n")
            print(len(title_list), title_list)
            print("\n")
            print(len(press_list), press_list)
            print("\n")
            print(len(date_list), date_list)
            print("\n")
            print(len(keyword_list), keyword_list)
            print("\n")
            print(len(content_list), content_list)
            print("\n")
            print(len(isfilter_list), isfilter_list)
            

            # page 이동 버튼 누르기
            try:
                #driver.find_element_by_css_selector('.btn_next').click()
                #driver.find_elements(By.CSS_SELECTOR,'.btn_next.btn').click()
                # xpath로 선택
                next_btn = driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[2]/div/a[2]')
                next_btn.send_keys(Keys.ENTER)
                time.sleep(2)
            except:
                pass

            time.sleep(1)

    
        df = pd.DataFrame({"title":title_list, "url":url_list, 'press':press_list, 'date':date_list, 'keyword':keyword_list, 'content': content_list, "filtered": isfilter_list, "Blacklist": isBlacklist_list, "Scraped_date": today})
        #df.fillna(0, inplace=True) #누락된 값을 0으로 채우기
        df

        # 키워드별 검색 페이지수 초기화
        if Selector is search_listA:
            page_num = page_num_A
        elif Selector is search_listB:
            page_num = page_num_B

        if not os.path.exists('./Recycling_Monitoring/%s.csv' %file_name): #기존 파일이 없을 때
            df.to_csv('./Recycling_Monitoring/%s.csv' %file_name, mode='w', index=True, index_label="index", encoding='utf-8-sig') #파일 새로 생성
        else: #기존 파일이 있을 때
            df.to_csv('./Recycling_Monitoring/%s.csv' %file_name, mode='a', index=True, index_label="index", encoding='utf-8-sig', header=False) #파일에 추가하기


