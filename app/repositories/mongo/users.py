from bson import ObjectId
from fastapi import HTTPException, status
from pymongo import errors

from .connection import db
from ...models.users import UserInDB


# get_user_collection returns the User collection
def get_user_collection():
    return db.users


# check_valid_id checks if the id is a valid id
def check_valid_id(_id: str):
    if not ObjectId.is_valid(_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the id is not valid")


#  create_one creates one User on DB
def create_one(collection: db.users, user: UserInDB):
    # if has attr id, deletes before insert on db
    if hasattr(user, 'id'):
        delattr(user, 'id')
    try:
        # inserts on db
        ret = collection.insert_one(user.mongo())
    except errors.DuplicateKeyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[e.details])

    # add the generated id
    stored_user = collection.find_one({"_id": ret.inserted_id})

    return UserInDB.from_mongo(stored_user)


# delete_one deletes one User from DB
def delete_one(collection: db.users, user_id: str):
    check_valid_id(user_id)
    result = collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count:
        return True
    return False


# find_one finds one User from DB or return null
def find_one(collection: db.user, user_id: str):
    check_valid_id(user_id)
    stored_user = collection.find_one({"_id": ObjectId(user_id)})
    if stored_user is None:
        return None
    return UserInDB.from_mongo(stored_user)
