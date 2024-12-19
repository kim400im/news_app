# pip install openai==0.28
import config
import openai

openai_api_key = config.OPENAI_API_KEY

openai.api_key = openai_api_key

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
    print(answer)

text = "현대 자동차 주가는 상승했는데 반해, 삼성전자 매출은 하락세다"
prompt = '''다음에 오는 텍스트 기업명을 추출하고, 기업에 해당하는 감성을 분석하시오.
출력포맷은 다음과 같습니다.
{"기업명":<기업명>, "감성":<긍정/부정>}

텍스트: '''

print(chatgpt_generate(prompt + text))
