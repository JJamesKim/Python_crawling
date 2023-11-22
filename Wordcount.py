import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
"""
df = pd.read_csv('./Battery_Monitoring/naver_news_Battery_2023-11-21.csv')

title_count = df['title'].value_counts().values
print(title_count)

print("-" *30)

content_count = df['content'].value_counts().values
print(content_count)
"""




df = pd.read_table('./Battery_Monitoring/naver_news_Battery_2023-11-21.csv')

# 결측치 존재 여부 확인
# print(df.isnull().sum)


# Null 값이 있을 경우
# df.dropna(inplace=True)

# 특정 열에서 중복을 제외하고 카운트 했을 때 데이터의 수는? 
# print(df['title'].nunique()) 

df.drop_duplicates(subset=['title'], inplace=True)
len(df)