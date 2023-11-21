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
from tqdm import tqdm
from tqdm import tqdm_notebook
import re
from time import sleep
import time
from datetime import datetime, timedelta
today = datetime.today()
today = today.strftime("%Y-%m-%d")
today


search = "배터리 투자"
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
driver.find_element(By.LINK_TEXT, '1주').click()

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

# 원하는 페이지수
page_num = 5

for i in tqdm_notebook(range(page_num)):

    things = driver.find_elements(By.CSS_SELECTOR, '.news_tit')
    # print(things)

    # title에 essential이 들어있는 기사 추려내기
    in_title_list = []
    ind_list = []

    for j, thing in enumerate(things):
            title = thing.get_attribute('title')
            in_title_list.append(thing)
    #     in_title_list

    # url 수집
    for thing in in_title_list:
        title = thing.get_attribute('href')
        url_list.append(title)

    #     print(url_list)
    # 기사 제목 수집
    for thing in in_title_list:
        title = thing.get_attribute('title')        
        title_list.append(title)
    #     print(title_list)

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
        date_list.append(date.text)
    date_list = [x for x in date_list if '전' in x]
    #     print(date_list)

    print('')
    time.sleep(1)

    print(len(url_list), url_list)
    print(len(title_list), title_list)
    print(len(press_list), press_list)
    print(len(date_list), date_list)

    # page 이동 버튼 누르기
    try:
        #driver.find_element_by_css_selector('.btn_next').click()
        driver.find_element(By.CSS_SELECTOR,'.btn_next').click()
        time.sleep(2)
    except:
        pass

    time.sleep(1)
    
df = pd.DataFrame({"title":title_list, "url":url_list, 'press':press_list, 'date':date_list})
df

df.to_csv('naver_news_{}_{}.csv'.format(search, today), encoding='utf-8-sig')