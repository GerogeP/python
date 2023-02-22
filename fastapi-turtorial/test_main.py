from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    print(response.json())
#    assert response.status_code == 200
#    assert response.json() == {"message": "Hello Bigger Applications!"}
    assert response.json() == {"message": "Hello Bigger Applications!"}

