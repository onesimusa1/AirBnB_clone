from tests.conftest import client
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User


def test_add_place_not_found(client):
    city_id = list(storage.all(City).values())[0].id
    user_id = list(storage.all(User).values())[0].id
    response = client.post(f"/api​/v1​/cities​/{city_id}​/places", json={"name": "test", "user_id": user_id})
    print(response.json)
    assert response.status_code == 404



def test_list_places(client):
    city_id = list(storage.all(City).values())[0].id
    response = client.get(f"/api/v1/cities/{city_id}/places")
    assert response.status_code == 200
    assert response.json == [place.to_dict() for place in storage.all(Place).values() if place.city_id == city_id]


def test_delete_place(client):
    place = list(storage.all(Place).values())[0]
    place_id = place.id
    response = client.delete(f"/api/v1/places/{place_id}")
    assert response.status_code == 200

def test_update_place(client):
    place = list(storage.all(Place).values())[0]
    place_id = place.id
    response = client.put(f"/api/v1/places/{place_id}", json={"name": "test2"})
    assert response.status_code == 200
    assert response.json["name"] == "test2"

def test_search_place_fail(client):
    response = client.post("/api/v1/places_search", json={"cities": ["1234"]})
    assert response.status_code == 200
    assert response.json == []

def test_search_valid(client):
    city = list(storage.all(City).values())[0]
    city_id = city.id
    response = client.post("/api/v1/places_search", json={"cities": [city_id]})
    assert response.status_code == 200
    assert response.json == [place.to_dict() for place in storage.all(Place).values() if place.city_id == city_id]
