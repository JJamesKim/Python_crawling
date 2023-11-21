import json
from pandas import json_normalize


def json_csv():
  with open('에스케이아이이티_naver_news.json', 'rt', encoding='UTF-8') as data_file:

    data = json.load(data_file)
    df = json_normalize(data)
    df.to_csv('에스케이아이이티_naver_news.json', index=False, encodings='CP949')
    return

def main():
    json_csv() 

if __name__ == '__main__':
    main()