from tests.conftest import client
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

def test_status(client):
    response = client.get("/api/v1/status"
    )
    print(response.json)
    assert response.json == {'status': 'OK'}
    
def test_stats(client):
    response = client.get("/api/v1/stats"
    )
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])
    assert response.json == num_objs

