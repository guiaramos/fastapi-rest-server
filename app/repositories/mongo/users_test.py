import pytest
from fastapi import HTTPException, status
from mongomock import MongoClient

from .connection import create_indexes
from .users import create_one, delete_one, find_one, get_user_collection, check_valid_id, find_one_by_email
from ...models.users import UserInDB

collection = MongoClient().db.collection
create_indexes(collection)

new_user = UserInDB(
    email="test@example.com",
    hashed_password="iuhasiuhdhiuasihud",
    name="test",
    display_name="test test",
    photo_url="http test",
    phone_number="01028969112"
)


# get_mocked_user_id returns the new_user id
def get_mocked_user_id():
    stored_user = collection.find_one({"email": new_user.email})
    return stored_user['_id']


def test_collection_return():
    # test should return collection
    coll = get_user_collection()
    assert hasattr(coll, 'find_one')


def test_create_user():
    # test if create user saves the user on DB
    stored_user = create_one(collection, new_user)
    delattr(stored_user, 'id')
    assert stored_user == new_user


def test_error_duplicated_key():
    # test if create same user two times throw error
    with pytest.raises(HTTPException) as e:
        create_one(collection, new_user)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST


def test_find_one_user():
    # test should return user from DB
    _id = get_mocked_user_id()
    stored_user = find_one(collection, _id)
    delattr(stored_user, 'id')
    assert stored_user == new_user


def test_find_one_no_user():
    # test should return None if the user is not registered
    _id = '601698d6d89d467e68903deb'
    stored_user = find_one(collection, _id)
    assert stored_user is None


def test_find_one_invalid_id():
    # test should raise error when id is invalid
    _id = 'banana'
    with pytest.raises(HTTPException) as e:
        find_one(collection, _id)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST


def test_delete_user():
    # test if delete exists user should return true
    _id = get_mocked_user_id()
    req = delete_one(collection, _id)
    assert req


def test_delete_user_invalid_id():
    # test should raise error when id is invalid
    _id = 'banana'
    with pytest.raises(HTTPException) as e:
        delete_one(collection, _id)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST


def test_check_valid_id():
    # test should raise error when id is invalid
    _id = 'banana'
    with pytest.raises(HTTPException) as e:
        check_valid_id(_id)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST


def test_find_one_by_email():
    # test should return the User
    create_one(collection, new_user)
    stored_user = find_one_by_email(collection, new_user.email)
    delattr(stored_user, 'id')
    assert stored_user == new_user


def test_find_one_by_email_wrong_email():
    # test should return None if the user is not registered
    stored_user = find_one_by_email(collection, 'pizza@burguer.com')
    assert stored_user is None
