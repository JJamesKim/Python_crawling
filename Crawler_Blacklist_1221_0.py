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


search_listA = ["포스코 수소 투자계획 해외", "한화 수소 투자계획 해외"]

search_listB = ["테스트"]
search_list_Final = [search_listA, search_listB]

filtering_keyword_list = ["건립 ", "건설 ", "설립 ", "짓는다 ", "증설 ", "신설 ", "설비 ", "진출 ", "추진 ", "해외 투자 ", "해외 확장 ", "해외 확대 ", "합작법인 ", "합작 ", "투자 ", "업무협약 ", "수주 ", "출자 ", 
                          "구축 ", "사업참여 ", "구축추진 ", "FEED ", "EPC ", "실증 ", "상용화 ", "개발 "
                          ]

# blacklist_keyword_list = []


for Selector in search_list_Final:
    # 검색어 리스트에 따라 검색하는 페이지의 수를 달리하기
    print (Selector)
    print(search_listA)
    if Selector is search_listA:
        page_num = 3
    elif Selector is search_listB:
        page_num = 1
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

    
        df = pd.DataFrame({"title":title_list, "url":url_list, 'press':press_list, 'date':date_list, 'keyword':keyword_list, 'content': content_list, "filtered": isfilter_list, "Scraped_date": today})
        #df.fillna(0, inplace=True) #누락된 값을 0으로 채우기
        df

        if not os.path.exists('./Recycling_Monitoring/%s.csv' %file_name): #기존 파일이 없을 때
            df.to_csv('./Recycling_Monitoring/%s.csv' %file_name, mode='w', index=True, index_label="index", encoding='utf-8-sig') #파일 새로 생성
        else: #기존 파일이 있을 때
            df.to_csv('./Recycling_Monitoring/%s.csv' %file_name, mode='a', index=True, index_label="index", encoding='utf-8-sig', header=False) #파일에 추가하기


