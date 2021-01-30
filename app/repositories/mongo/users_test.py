import pytest
from mongomock import MongoClient
from pymongo import errors

from ...models import users as user_models

collection = MongoClient().db.collection

new_user = user_models.UserInDB(
    email="test@example.com",
    hashed_password="iuhasiuhdhiuasihud",
    name="test",
    display_name="test test",
    photo_url="http test",
    phone_number="01028969112"
)


def test_create_user():
    # test if create user saves the user on DB
    req = collection.insert_one(new_user.dict(by_alias=True))
    stored_user = collection.find_one({'_id': req.inserted_id})

    assert stored_user == new_user.dict(by_alias=True)


def test_error_duplicated_key():
    # test if create same user two times throw error
    with pytest.raises(errors.DuplicateKeyError):
        assert collection.insert_one(new_user.dict(by_alias=True))
