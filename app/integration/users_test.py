from fastapi import status
from fastapi.testclient import TestClient
from mongomock import MongoClient

from app.main import app
from ..env import COOKIE_ACCESS_KEY
from ..mocks.mock_users import get_mock_user
from ..models.users import User
from ..repositories.mongo import users as user_repo

client = TestClient(app)

mock_coll = MongoClient().db.collection

new_user_db = get_mock_user()


def create_mock_cookie(token):
    return {COOKIE_ACCESS_KEY: token}


# get_mocked_user_collection is a mock for collection
def get_mocked_user_collection():
    return mock_coll


# overrides the deps so it uses a mock collection instead of calling the actually database
app.dependency_overrides[user_repo.get_user_collection] = get_mocked_user_collection


def test_create_user():
    # test if user is created with no errors
    response = client.post("/users/", json=new_user_db.dict())
    assert response.status_code == status.HTTP_200_OK

    stored_user = mock_coll.find_one({'email': new_user_db.email})
    new_user = User.from_mongo(stored_user).dict()
    new_user['id'] = str(new_user['id'])
    assert response.json() == new_user

    assert response.cookies[COOKIE_ACCESS_KEY]


def test_get_me():
    # test if user is returned with no error
    response = client.get("/users/me/")
    assert response.status_code == status.HTTP_200_OK

    stored_user = mock_coll.find_one({'email': new_user_db.email})
    new_user = User.from_mongo(stored_user).dict()
    new_user['id'] = str(new_user['id'])
    assert response.json() == new_user


def test_get_me_unauthenticated():
    # test should throw error for non authenticated user
    response = client.get("/users/me/", cookies={'todo.access-token': ''})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
