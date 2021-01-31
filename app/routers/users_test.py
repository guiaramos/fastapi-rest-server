from datetime import timedelta

from jose import jwt

from .users import check_confirm_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, \
    ALGORITHM, SECRET_KEY
from ..models import token as token_models


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
    fakeid = 'thisisaveryfakeid'
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = token_models.TokenData(id=fakeid)
    access_token = create_access_token(access_token_data.dict(), access_token_expires)
    fakeid_decoded = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
    assert fakeid == fakeid_decoded['id']
