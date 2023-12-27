import pandas as pd
from konlpy.tag import Okt
import re
from konlpy.tag import Hannanum

# 프로세스의 목적: Filtering Keywords와 Blacklist Keywords를 찾기 위해 단어 빈도수 검사를 시행
# 궁극적으로는 자동 분류하는 프로세스를 강화하여 오퍼레이션 시간을 단축시키고자 함

# 데이터 불러오기
data = pd.read_csv('./Recycling_Monitoring/H2 Origin.csv')

# 'title' 칼럼 데이터를 문자열로 변환
data['title'] = data['title'].astype(str)


# 'title' 칼럼 데이터를 텍스트로 저장
text_data = ' '.join(data['title'])

# 숫자 제거
text_data = re.sub('[0-9]+', '', text_data)

# 영문 제거 (필요에 따라 실행)
# text_data = re.sub('[A-Za-z]+', '', text_data)

# 특수문자 제거
text_data = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ·!』\\‘’|\(\)\[\]\<\>`\'…》]', '', text_data)


# 형태소 분석을 위한 konlpy 태그 객체 생성
okt = Okt()

# 형태소 분석 및 빈도수 분석
word_counts = {}
morphs = okt.morphs(text_data)
for morph in morphs:
    if morph in word_counts:
        word_counts[morph] += 1
    else:
        word_counts[morph] = 1

# 결과 출력
print(word_counts)


# CSV 파일로 저장
file_name = input("Name of this file : ")

df = pd.DataFrame(list(word_counts.items()), columns=['단어', '빈도수'])
df = df.sort_values("빈도수", ascending=False) # 내림차순 정렬
df.to_csv('./Recycling_Monitoring/%s.csv' %file_name, index=False, encoding='utf-8-sig')