import streamlit as st
import pandas as pd

data = [
    {"기업명":"현대차",
     "날짜": "2024-09-02",
     "문서 카테고리":"인수합병",
     "요약":"현대차가 보스턴 다이나믹스에 투자를 하기로 발표했다",
     "주요 이벤트": ["기업 인수합병", "신규 투자"]
     
     },
]

df = pd.DataFrame(data)
df['날짜']= pd.to_datetime(df['날짜'])

st.sidebar.title("필터 옵션")
selected_company = st.sidebar.selectbox("기업명 선택", df['기업명'].unique())
date_range = st.sidebar.date_input("날짜 범위 선택", [df['날짜'].min().date(), df['날짜'].max().date()])

start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# 기업명과 날짜로 필터링
filtered_df = df[(df['기업명']==selected_company) & (df['날짜'].between(start_date, end_date))]

#필터링된 데이터 날짜별로 그룹화
grouped_df= filtered_df.groupby("날짜").agg({
    '문서 카테고리':'first',
    '주요 이벤트': 'first',
    '요약':'first'
}).reset_index()

#결과를 테이블 형태로 표시
st.title(f"{selected_company}의 문서 목록")
st.dataframe(grouped_df[['날짜', '문서 카테고리', '주요 이벤트']])

#요약
if st.checkbox("요약 보기"):
    for idx, row in grouped_df.iterrows():
        st.subheader(f"{row['날짜']} = {row['문서 카테고리']}")
        st.write(row['요약'])


# streamlit run streamlit.py