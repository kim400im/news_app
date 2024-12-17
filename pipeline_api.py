# pip install openai==0.28
import config
import openai

openai_api_key = config.OPENAI_API_KEY

openai.api_key = openai_api_key

model = "gpt-4o-mini"

query = "HBM 반도체에 대해 설명해줘"

# gpt 에게 역할 부여, 유저의 질문 보냄
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