import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd
import csv

#API 정보
client_id = "2Gq2T4SoDvLBlNAuz64W"
client_secret = "AkJnZueIre"

def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if(response.getcode() ==200):
            print("[%s] URL Request Success" % datetime.datetime.now())
            return response.read().decode("utf-8")
            
    except Exception as e:
            print(e)
            print("[%s] Error for URL: %s" %(datetime.datetime.now(), url))
            return None


# 네이버 서버에 보낼 요청 변수 생성
def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    # json으로 받기
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), start, display)

    url = base + node + parameters
    responseDecode = getRequestUrl(url)  # [getRequestUrl로 보내주기]

    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)
    
# getPostData: 값을 저장하는 함수
def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({'cnt': cnt, 'title': title, 'description': description,
                       'org_link': org_link, 'link': org_link, 'pDate': pDate})
    return



# 메인함수
def main():
    # csv_result = []
    node = 'news'  # 크롤링 할 대상
    srcText = input('검색어를 입력하세요: ')
    cnt = 0
    jsonResult = []

    jsonResponse = getNaverSearch(node, srcText, 1, 100)  
    total = jsonResponse['total']

    while ((jsonResponse != None) and (jsonResponse['display'] != 0)):
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)  

        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 10) 

    # 검색 결과 확인
    print('전체 검색 : %d 건' % total)

    # json 파일에 값 넣어주기 (json.dumps)
    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)

        outfile.write(jsonFile)

    datafrmae = pd.read_json('%s_naver_%s.json' % (srcText, node), orient= 'column')
    datafrmae.to_csv('%s_naver_%s.csv' % (srcText, node))
    

    



"""
    with open(jsonFile, 'r', encoding = 'utf-8') as input_file, open('%s_naver_%s.csv' % (srcText, node), 'w', newline = '') as output_file :    
        data = json.load(input_file)

        f = csv.writer(output_file)

        f.writerow(["cnt", "description", "link", "org_link", "pDate", "title"])

        for datum in data:
            f.writerow([datum["cnt"], datum["description"], datum["link"], datum["org_link"], datum["pDate"], datum["title"]])

    """
    
if __name__ == '__main__':
    main()


