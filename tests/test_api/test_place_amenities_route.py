from tests.conftest import client
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User


def test_place_amenities(client):
    place = list(storage.all(Place).values())[0]
    place_id = place.id
    response = client.get(f"/api/v1/places/{place_id}/amenities")
    assert response.status_code == 200

