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
from tqdm import tqdm_notebook
import re
from time import sleep
import time
from datetime import datetime, timedelta
today = datetime.today()
today = today.strftime("%Y-%m-%d")
today


search_list = ["LG에너지솔루션 배터리", "삼성SDI 배터리", "SK온 배터리", "롯데에너지머티리얼즈 배터리", "롯데알미늄 배터리", 
               "포스코 배터리", "포스코퓨처엠 배터리", "에코프로비엠 배터리", "SK아이이테크놀로지 배터리", "SKIET 배터리", 
               "에코프로 머티리얼즈 배터리", "에코프로 CNG 배터리", "LG 화학 배터리", "롯데 케미칼 배터리"
]


existing_data_path = './Battery_Monitoring/Battery_Recycling.csv'
if os.path.exists(existing_data_path):
    existing_data = pd.read_csv(existing_data_path)
    print("existing data 존재")
else:
    print(f"파일 '{existing_data_path}'이(가) 존재하지 않습니다.")


for search in search_list:
    
    # for search in searches:
    print("-"*30)
    print('"'+ search + '"', '크롤링 시작')

    # 크롬창 띄우기
    driver = webdriver.Chrome()  # 윈도우 : "chromedriver.exe"
    driver.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}".format(search))
    time.sleep(3)

    # 옵션 클릭
    # option_bt = driver.find_element_by_css_selector(".btn_option._search_option_open_btn")
    option_bt = driver.find_element(By.CSS_SELECTOR,'.btn_option._search_option_open_btn')
    option_bt.click()
    time.sleep(1)

    # 기간 선택
    #driver.find_element_by_link_text('1주').click()  # 1시간, 1일, 1주, 1개월, 3개월, 6개월, 1년
    driver.find_element(By.LINK_TEXT, '3개월').click()

    # page 수 확인
    # page_count = driver.find_elements_by_css_selector('.sc_page_inner .btn')
    page_count = driver.find_elements(By.CSS_SELECTOR,'.sc_page_inner .btn')
    page_num = len(page_count)
    print('페이지 수: ', page_num)

    time.sleep(1)

    # 뉴스 전체 페이지를 돌면서 기사의 title, url 수집하기
    url_list = []
    title_list = []
    press_list = []
    date_list = []
    keyword_list = []
    content_list = []
    SDate_list = [] #스크랩한 날짜

    # 원하는 페이지수
    page_num = 2

    for i in tqdm_notebook(range(page_num)):


        things = driver.find_elements(By.CSS_SELECTOR, '.news_tit')
        print(things)

        # title에 essential이 들어있는 기사 추려내기
        in_title_list = []
        #ind_list = []

        # url 수집
        for thing in in_title_list:
            title = thing.get_attribute('href')
            if title not in existing_data['url'].values:
                exit()
            url_list.append(title)
        #     print(url_list)
            for j, thing in enumerate(things):
                    title = thing.get_attribute('title')
                    in_title_list.append(thing)
                    in_title_list

            # 기사 제목 수집
            for thing in in_title_list:
                title = thing.get_attribute('title')   
                title_list.append(title)
                print(title_list)

            # 신문사 수집
            # press_raw= driver.find_elements_by_css_selector('.info.press')
            press_raws = driver.find_elements(By.CSS_SELECTOR,'.info.press')
            for press in press_raws:
                press_list.append(press.text)
            #     print(press_list)

            # 날짜 수집
            #date_raw = driver.find_elements_by_css_selector('.info_group > span')
            date_raws = driver.find_elements(By.CSS_SELECTOR,'.info_group > span')
            for date in date_raws:
                #date_list.append(date.text)
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

            #   print(content_list)
        
            #     print(date_list)

        

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

        # page 이동 버튼 누르기
        try:
            #driver.find_element_by_css_selector('.btn_next').click()
            #driver.find_elements(By.CSS_SELECTOR,'.btn_next.btn').click()
            # xpath로 클릭
            next_btn = driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[2]/div/a[2]')
            next_btn.send_keys(Keys.ENTER)
            time.sleep(2)
        except:
            pass

        time.sleep(1)


    df = pd.DataFrame({"title":title_list, "url":url_list, 'press':press_list, 'date':date_list, 'keyword':keyword_list, 'content': content_list, "Scraped_date": today})
    df.fillna(0, inplace=True) #누락된 값을 0으로 채우기
    df
    if search_list.index(search) == 0:
        df.to_csv('./Battery_Monitoring/naver_news_Battery_test%s.csv' %today, index=True, index_label="index", mode='w', encoding='utf-8-sig')
    else:
        df.to_csv('./Battery_Monitoring/naver_news_Battery_test%s.csv' %today, mode='a', index=True, index_label="index", encoding='utf-8-sig', header=False)

'''
    if not os.path.exists('./Battery_Monitoring/naver_news_{}_{}.csv'.format(search, today)):
        df.to_csv('./Battery_Monitoring/naver_news_{}_{}.csv'.format(search, today), index=True, index_label="index", mode='w', encoding='utf-8-sig')
    else:
        df.to_csv('./Battery_Monitoring/naver_news_{}_{}.csv'.format(search, today), mode='a', index=True, index_label="index", encoding='utf-8-sig', header=False)
'''

