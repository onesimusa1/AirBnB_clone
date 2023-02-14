from tests.conftest import client
from models import storage
from models.state import State




def test_list_states(client):
    response = client.get("/api/v1/states")
    assert response.status_code == 200
    assert response.json == [state.to_dict() for state in storage.all(State).values()]

def test_add_state(client):
    response = client.post("/api/v1/states", json={"name": "test"})
    assert response.status_code == 201
    
def test_add_state_fail(client):
    response = client.post("/api/v1/states", json={})
    assert response.status_code == 400


def test_delete_state(client):
    state = State(name="test")
    storage.new(state)
    storage.save()
    response = client.delete(f"/api/v1/states/{state.id}")
    assert response.status_code == 200

def test_update_state(client):
    state = State(name="test")
    storage.new(state)
    storage.save()
    response = client.put(f"/api/v1/states/{state.id}", json={"name":"test2"})
    assert response.status_code == 200
    assert response.json["name"] == "test2"


def test_failed_delete_state(client):
    response = client.delete("/api/v1/states/1234")
    assert response.status_code == 404


def test_update_state_fail(client):
    response = client.put("/api/v1/states/1234", json={"name":"test2"})
    assert response.status_code == 404
