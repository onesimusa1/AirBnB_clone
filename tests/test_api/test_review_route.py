from tests.conftest import client
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.review import Review

def test_list_reviews(client):
    place = list(storage.all(Place).values())[0]
    place_id = place.id
    response = client.get(f"/api/v1/places/{place_id}/reviews")
    assert response.status_code == 200
    assert response.json == [review.to_dict() for review in storage.all(Review).values() if review.place_id == place_id]

def test_add_review(client):
    place = list(storage.all(Place).values())[0]
    place_id = place.id
    user = list(storage.all(User).values())[0]
    user_id = user.id
    response = client.post(f"/api/v1/places/{place_id}/reviews", json={"text": "test", "user_id": user_id})
    assert response.status_code == 201

def test_failed_add_review(client):
    place = list(storage.all(Place).values())[0]
    place_id = place.id
    response = client.post(f"/api/v1/places/{place_id}/reviews", json={"text": "test"})
    assert response.status_code == 400

def test_delete_review(client):
    review = list(storage.all(Review).values())[0]
    review_id = review.id
    response = client.delete(f"/api/v1/reviews/{review_id}")
    assert response.status_code == 200


def test_retrive_review(client):
    review = list(storage.all(Review).values())[0]
    review_id = review.id
    response = client.get(f"/api/v1/reviews/{review_id}")
    assert response.status_code == 200
    assert response.json == review.to_dict()

def  test_update_review(client):
    review = list(storage.all(Review).values())[0]
    review_id = review.id
    response = client.put(f"/api/v1/reviews/{review_id}", json={"text": "test2"})
    assert response.status_code == 200
    assert response.json["text"] == "test2"
