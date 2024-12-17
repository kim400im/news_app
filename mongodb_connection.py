# pip install pymongo

from pymongo import MongoClient

client = MongoClient(host="localhost", port=27017)

print(client.list_database_names())

db = client['test']

print(db)

collection = db['NewsText']

print(collection)

# import datetime
# item = {
#     "title":"amd 주가 일시 상승",
#     "text": "amd의 주가가 일시적으로 상승했다 ..",
#     "date": datetime.datetime.now()}

# insert_id = collection.insert_one(item).inserted_id
# print(insert_id)

print(collection.find_one())