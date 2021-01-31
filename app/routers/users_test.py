from datetime import timedelta

import pytest
from fastapi import HTTPException, status
from jose import jwt
from mongomock import MongoClient

from .users import check_confirm_password, get_password_hash, create_access_token, get_user_on_db, create_user_on_db
from ..env import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from ..mocks.mock_users import get_mock_user
from ..models.token import TokenData

mock_coll = MongoClient().db.collection


def test_check_confirm_password():
    # test if the confirm password returns true when the passwords are correct
    password = 'banana'
    password_confirm = 'banana'
    is_same = check_confirm_password(password, password_confirm)
    assert is_same


def test_check_confirm_wrong_password():
    # test if the confirm password returns false when the passwords are incorrect
    password = 'pizza'
    password_confirm = 'banana'
    is_same = check_confirm_password(password, password_confirm)
    assert not is_same


def test_get_password_hash():
    # test if function hashes the password
    password = 'pizza'
    hashed_password = get_password_hash(password)
    assert password != hashed_password


def test_create_access_token():
    # test if function creates the access_token
    fakeid = '507f1f77bcf86cd799439011'
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = TokenData(id=fakeid)
    access_token = create_access_token(access_token_data.dict(), access_token_expires)
    fakeid_decoded = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
    assert fakeid == fakeid_decoded.get('id')


def test_get_user_on_db():
    # test should return user from db
    mock_user = get_mock_user()
    hashed_password = get_password_hash(mock_user.password)
    created_user = create_user_on_db(coll=mock_coll, hashed_password=hashed_password, user_in=mock_user)
    delattr(created_user, 'hashed_password')
    stored_user = get_user_on_db(str(created_user.id), mock_coll)
    assert stored_user == created_user


def test_get_user_on_db_not_found():
    # test should return error for user not found
    mocked_id = '507f1f77bcf86cd799439011'
    with pytest.raises(HTTPException) as e:
        get_user_on_db(mocked_id, mock_coll)

    assert e.value.status_code == status.HTTP_404_NOT_FOUND


def test_get_user_on_db_wrong_id():
    # test should raise error for wrong id
    mocked_id = 'banana'
    with pytest.raises(HTTPException) as e:
        get_user_on_db(mocked_id, mock_coll)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST

# TODO: get_current_user
# TODO: create_user_on_db
