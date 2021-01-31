from pymongo import MongoClient, ASCENDING

client = MongoClient('mongodb://admin:admin@localhost:27017/')
db = client.todos


# create_indexes creates all the indexes
def create_indexes(collection):
    collection.create_index([("email", ASCENDING), ("phone_number", ASCENDING)], unique=True)
