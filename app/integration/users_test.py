from fastapi.testclient import TestClient
from fastapi import status
from mongomock import MongoClient

from app.main import app
from ..models import users as user_models
from ..repositories.mongo import users as user_repo
from ..routers.users import COOKIE_ACCESS_KEY

client = TestClient(app)

mock_coll = MongoClient().db.collection

new_user_db = user_models.UserIn(
    email="test@aaaa.com",
    password='banana',
    password_confirm='banana',
    name="test",
    display_name="test test",
    photo_url="http test",
    phone_number="01028969112"
)


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
    stored_user['id'] = str(stored_user['_id'])
    new_user = user_models.User(**stored_user)
    print(response.cookies)
    assert response.json() == new_user

    assert response.cookies[COOKIE_ACCESS_KEY]
