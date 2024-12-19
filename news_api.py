from gdeltdoc import GdeltDoc, Filters
from newspaper import Article  # pip install newspaper3k


f = Filters(
    start_date = "2020-05-01",
    end_date = "2020-05-02",
    num_records = 250,
    keyword = "microsoft",
    domain = ["bbc.co.uk", "nytimes.com"],
    country = "US",

)
gd = GdeltDoc()

# Search for articles matching the filters
articles = gd.article_search(f)
print(articles)

url = articles.loc[1, "url"]
print(articles.loc[1, "title"])
print('--------------------------')

article = Article(url)
article.download()
article.parse()
print(article.text)