from tests.conftest import client
from models import storage
from models.user import User

def test_list_users(client):
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert response.json == [user.to_dict() for user in storage.all(User).values()]
    


def test_add_user(client):
    response = client.post("/api/v1/users", json={
        "email": "test@test.com",
        "password": "test"})
    assert response.status_code == 201


def test_add_user_fail(client):
    response = client.post("/api/v1/users", json={
        "email": "test@test.com"
        })
    assert response.status_code == 400


def test_delete_user(client):
    user = User(email="test@test.tech", password="test")
    storage.new(user)
    storage.save()
    response = client.delete(f"/api/v1/users/{user.id}")
    assert response.status_code == 200


def test_failed_delete_user(client):
    response = client.delete("/api/v1/users/1234")
    assert response.status_code == 404


def test_update_user(client):
    user = User(email="test@test.tech", password="test")
    storage.new(user)
    storage.save()
    response = client.put(f"/api/v1/users/{user.id}", json={"last_name":"test","first_name":"test"})
    assert response.status_code == 200
    assert response.json["last_name"] == "test"
    assert response.json["first_name"] == "test"
    
