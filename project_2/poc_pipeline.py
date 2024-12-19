import config
import openai

open_ai_key = config.OPENAI_API_KEY
openai.api_key = open_ai_key
model = "gpt-4o-mini"

def chatgpt_generate(query):
    messages = [{
        "role":"system",
        "content": "You are a helpful assistant"
    },{
        "role": "user",
        "content": query
    }]

    response = openai.ChatCompletion.create(model=model, messages=messages)
    answer = response['choices'][0]['message']['content']
    # print(answer)
    return answer

def prompting(news):
    prompt = """ 아래 뉴스 텍스트를 참고하여 세 가지 task 를 수행하시오. 출력 포멧에 정의된 것만 생성하시오

Task #1: 텍스트를 참고해서 다음과 같은 카테고리로 분류하시오. 아래 카테고리에 해당하지 않으면, 빈 리스트를 반환하시오

카테고리 : 정책/금융, 채권/외환, IB/기업, 증권, 국제뉴스, 해외주식, 부동산

Task #2 : 뉴스 내용을 최대 3문장으로 요약하시오

Task #3 : 뉴스에서 금융 이벤트 예시를 참고하여 내용과 관련된 이벤트릀 생성하시오.  예시에 있는 이벤트가 아닌 뉴스와 관련된 이벤트 문구를 반드시 새로 생성하시오

금융 이벤트 예시 : "신제품 출시", "기업 인수합병", "리콜", "배임횡령", "오너 리스크", "자연재해", "제품 불량" 등

출력 포맷:
{"문서 카테고리":<카테고리>, "요약":<요약 문장>, "주요 이벤트" : [<이벤트1>, <이벤트2>, ... ]}

뉴스:
"""

    answer = chatgpt_generate(prompt + news)
    return answer

news = """테슬라 주가가 푼토 카사 데 볼사의 투자의견 하향 조정 여파로 하방 압력을 받고 있다. 푼토 카사 데 볼사는 테슬라에 대한 투자의견을 '매도'로 낮추고 목표주가를 364.44달러로 제시했다. 이는 테슬라의 현재 가치와 전기차 시장의 불확실성에 대한 우려를 반영한 것이다.
푼토 카사 데 볼사는 테슬라의 미래 실적 전망을 수정하며 현재 주가가 고평가되었다고 판단했다. 이번 투자의견 하향은 전기차 시장 경쟁 심화 등 테슬라를 둘러싼 불확실성이 커지는 가운데 나온 것이다. 특히 364.44달러라는 목표주가는 현재 주가 대비 상당한 하락 가능성을 시사한다.
테슬라 주가는 12월 18일 오전 7시 40분(현지시간) 기준 471달러를 기록하고 있다. 이는 전일 종가인 479.86달러 대비 1.85% 하락한 수준이다.
"""

answer = prompting(news)

print(answer)