from pymongo import MongoClient

client = MongoClient('mongodb://admin:admin@localhost:27017/')
db = client.todos

