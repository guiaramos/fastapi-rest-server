from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    # test if the app starts with no errors
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Gui's TODO app written with FastAPI"}

