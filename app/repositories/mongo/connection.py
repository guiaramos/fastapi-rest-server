from pymongo import MongoClient, ASCENDING

client = MongoClient('mongodb://admin:admin@localhost:27017/')
db = client.todos
db.users.create_index([("email", ASCENDING), ("phone_number", ASCENDING)], unique=True)
