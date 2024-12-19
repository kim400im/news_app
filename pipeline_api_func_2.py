# pip install openai==0.28
import config
import openai

from gdeltdoc import GdeltDoc, Filters
from newspaper import Article

openai_api_key = config.OPENAI_API_KEY

openai.api_key = openai_api_key

model = "gpt-4o-mini"
gd = GdeltDoc()


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

def get_url(keyword):
    f = Filters(
    start_date = "2020-05-01",
    end_date = "2020-05-02",
    num_records = 250,
    keyword = keyword,
    domain = ["bbc.co.uk", "nytimes.com"],
    country = "US",
    )
    articles = gd.article_search(f)
    return articles

def url_crawling(df):
    urls = df["url"]
    titles = df['title']
    texts = []
    for url in urls:
        article = Article(url)
        article.download()
        article.parse()
        try:
            texts.append(article.text)
        except:
            print(e)
    return texts

# prompt = '''아래 뉴스에서 기업명을 모두 추출하고, 기업에 해당하는 감성을 분석하시오.
# 출력포맷은 다음과 같습니다.
# {"기업명":<기업명>, "감성":<긍정/부정>}

# 뉴스: '''
prompt = '''아래 뉴스에서 기업명을 모두 추출하고, 기업에 해당하는 감성을 분석하시오.
각 감성에 스코어링을 하시오. 각 스코어의 합은 1이 되어야 합니다. 소수점 첫번째까지만 생성하세요.
출력포맷은 리스트이며, 세부 내용은 다음과 같습니다.
불필요한 ``` 나 ' 같은 기호는 들어가지 않도록 하세요.
[{"organization":<기업명>,"positive":0~1, "negative":0~1, "neutral":0~1}, ... ]

뉴스: '''

# df = get_url("microsoft")
# # print(len(df))
# texts = url_crawling(df)
# # print(len(texts))

# answer = chatgpt_generate(prompt + texts[2])
# print(prompt + texts[0])
# print("---------------")
# print(answer)
# print(eval(answer))

result = []
orgs = ["microsoft", "apple"]
for org in orgs:
    df = get_url(org)
    texts = url_crawling(df)
    for text in texts:
        answer = chatgpt_generate(prompt + text)
        result.append(eval(answer))

print(result)