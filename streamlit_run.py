import streamlit as st
import pandas as pd
from gdeltdoc import GdeltDoc, Filters
from newspaper import Article
import os
import openai
import datetime
from dotenv import load_dotenv

# API 키 넣기
gd = GdeltDoc()
# openai.api_key = config.OPENAI_API_KEY
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 뉴스 기사 가져오기
def get_urls(keyword: str, start_date: str, end_date: str):
    f = Filters(
        start_date=start_date,
        end_date=end_date,
        num_records=10,
        keyword=keyword,
        domain=["bbc.co.uk", "nytimes.com"],
        country="US",
    )
    articles = gd.article_search(f)
    return pd.DataFrame(articles)

# 뉴스 정보 파싱하기
def parse_text(article_df: pd.DataFrame):
    result = []
    for _, row in article_df.iterrows():
        try:
            url = row['url']
            article = Article(url)
            article.download()
            article.parse()

            temp = {
                "title": row['title'],
                "date": row['seendate'],
                "text": article.text
            }
            result.append(temp)
        except Exception as e:
            st.write(f"Error parsing article: {e}")
    return result

# GPT를 활용하여 뉴스 요약하기
def chatgpt_generate(query):
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": query}
    ]
    response = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages)
    return response['choices'][0]['message']['content']

# 프롬프트 만들기
def prompting(news):
    prompt = """ 아래 뉴스 텍스트를 참고하여 세 가지 task 를 수행하시오. 출력 포멧에 정의된 것만 생성하시오. 

Task #1: 텍스트를 참고해서 다음과 같은 카테고리로 분류하시오. 아래 카테고리에 해당하지 않으면, 빈 리스트를 반환하시오

카테고리 : 정책/금융, 채권/외환, IB/기업, 증권, 국제뉴스, 해외주식, 부동산

Task #2 : 뉴스 내용을 최대 3문장으로 요약하시오. 모두 한국어로 표현하시오

Task #3 : 뉴스에서 금융 이벤트 예시를 참고하여 내용과 관련된 이벤트를 생성하시오.  예시에 있는 이벤트가 아닌 뉴스와 관련된 이벤트 문구를 반드시 새로 생성하시오

금융 이벤트 예시 : "신제품 출시", "기업 인수합병", "리콜", "배임횡령", "오너 리스크", "자연재해", "제품 불량" 등

출력 포맷:
{"문서 카테고리": <카테고리>, "요약": <요약 문장>, "주요 이벤트" : [<이벤트1>, <이벤트2>, ... ]}

뉴스:
"""
    return chatgpt_generate(prompt + news)

# Streamlit 사이드바
st.sidebar.title("필터 옵션")
selected_company = st.sidebar.text_input("기업명 입력", "Microsoft")
date_range = st.sidebar.date_input("날짜 범위 선택", [datetime.date(2024, 11, 1), datetime.date(2024, 11, 30)])

# 화면
if selected_company:
    start_date = date_range[0].strftime('%Y-%m-%d')
    end_date = date_range[1].strftime('%Y-%m-%d')
    st.sidebar.write(f"검색 중: {selected_company}")

    # 기사 가져오기
    articles_df = get_urls(selected_company, start_date, end_date)
    parsed_articles = parse_text(articles_df)

    # 요약 가져오기
    processed_data = []
    for article in parsed_articles:
        answer = prompting(article['text'])
        try:
            result = eval(answer)
            result.update({
                "기업명": selected_company,
                "날짜": article['date'],
                "제목": article['title']
            })
            processed_data.append(result)
        except Exception as e:
            st.write(f"Error processing article: {e}")

    if processed_data:
        df = pd.DataFrame(processed_data)
        df['날짜'] = pd.to_datetime(df['날짜'])

        grouped_data = df.groupby("날짜").agg({
            '문서 카테고리': 'first',
            '주요 이벤트': 'first',
            '요약': 'first'
        }).reset_index()

        st.title(f"{selected_company}의 뉴스 분석 결과")
        st.dataframe(grouped_data[['날짜', '문서 카테고리', '주요 이벤트']])

        if st.checkbox("요약 보기"):
            for idx, row in grouped_data.iterrows():
                st.subheader(f"{row['날짜'].strftime('%Y-%m-%d')} - {row['문서 카테고리']}")
                st.write(row['요약'])
    else:
        st.write("검색된 뉴스가 없습니다.")

# Streamlit 실행방법
st.sidebar.markdown("**실행 방법**: `streamlit run <script_name>.py`")
