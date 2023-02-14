from tests.conftest import client
from models import storage
from models.amenity import Amenity


def test_list_amenities(client):
    response = client.get("/api/v1/amenities")
    assert response.status_code == 200
    assert response.json == [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    
def test_add_amenity(client):
    response = client.post("/api/v1/amenities", json={"name": "test"})
    assert response.status_code == 201


def test_delete_amenity(client):
    amenity = Amenity(name="test")
    storage.new(amenity)
    storage.save()
    response = client.delete(f"/api/v1/amenities/{amenity.id}")
    assert response.status_code == 200


def test_update_amenity(client):
    amenity = Amenity(name="test")
    storage.new(amenity)
    storage.save()
    response = client.put(f"/api/v1/amenities/{amenity.id}", json={"name":"test2"})
    assert response.status_code == 200
    assert response.json["name"] == "test2"
