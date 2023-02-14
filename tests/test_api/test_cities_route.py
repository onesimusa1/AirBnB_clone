from tests.conftest import client
from models import storage
from models.city import City
from models.state import State


def test_list_cities(client):
    state = State(name="test")
    storage.new(state)
    storage.save()
    state_id = state.id
    response = client.get(f"/api/v1/states/{state_id}/cities")
    assert response.status_code == 200
    assert response.json == [city.to_dict() for city in storage.all(City).values() if city.state_id == state_id]


def test_add_city(client):
    state = State(name="test")
    storage.new(state)
    storage.save()
    state_id = state.id
    response = client.post(f"/api/v1/states/{state_id}/cities", json={"name": "test"})
    assert response.status_code == 201


def  test_update_city(client):
    state = State(name="test")
    storage.new(state)
    storage.save()
    state_id = state.id
    city = City(name="test", state_id=state_id)
    storage.new(city)
    storage.save()
    city_id = city.id
    response = client.put(f"/api/v1/cities/{city_id}", json={"name": "test2"})
    assert response.status_code == 200
    assert response.json["name"] == "test2"
    
def test_delete_city(client):
    state = State(name="test")
    storage.new(state)
    storage.save()
    state_id = state.id
    city = City(name="test", state_id=state_id)
    storage.new(city)
    storage.save()
    city_id = city.id
    response = client.delete(f"/api/v1/cities/{city_id}")
    assert response.status_code == 200
    
def test_failed_delete_city(client):
    response = client.delete("/api/v1/cities/1234")
    assert response.status_code == 404
    
def test_get_city_by_id(client):
    state = State(name="test")
    storage.new(state)
    storage.save()
    state_id = state.id
    city = City(name="test", state_id=state_id)
    storage.new(city)
    storage.save()
    city_id = city.id
    response = client.get("/api/v1/cities/{}".format(city_id))
    assert response.status_code == 200
    assert response.json == city.to_dict()

def test_get_all_city_bystate(client):
    state = State(name="test")
    storage.new(state)
    storage.save()
    for i in range(4):
        city = City(name="test{}".format(i), state_id=state.id)
        storage.new(city)
        storage.save()
    response = client.get("/api/v1/states/{}/cities".format(state.id))
    assert response.status_code == 200
    assert response.json == [city.to_dict() for city in storage.all(City).values() if city.state_id == state.id]
