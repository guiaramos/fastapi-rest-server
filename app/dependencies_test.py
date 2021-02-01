import unittest
from datetime import timedelta

import pytest
from fastapi import HTTPException, status

from .dependencies import get_token_cookie
from .env import ACCESS_TOKEN_EXPIRE_MINUTES
from .mocks.mock_users import get_mock_user
from .models.token import TokenData
from .routers.users import create_access_token

new_user_db = get_mock_user()


def create_mock_token(_id='507f1f77bcf86cd799439011', seconds=ACCESS_TOKEN_EXPIRE_MINUTES):
    access_token_expires = timedelta(seconds=seconds)
    access_token_data = TokenData(id=_id)
    return create_access_token(access_token_data.dict(), access_token_expires)


class TestGetToke(unittest.TestCase):
    async def test_get_token_cookie(self):
        # test should return access token from header
        access_token = create_mock_token()
        found_token = await get_token_cookie(access_token)
        assert access_token == found_token

    async def test_no_found_cookie(self):
        # test should raise error if cookie is not found
        access_token = create_mock_token("")
        with pytest.raises(HTTPException) as e:
            await get_token_cookie(access_token)
        assert e.value.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_no_expired_token(self):
        # test should raise error if cookie is expired
        access_token = create_mock_token(seconds=0)
        with pytest.raises(HTTPException) as e:
            await get_token_cookie(access_token)
        assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
