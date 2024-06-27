from fastapi.testclient import TestClient
from app.main import app
from app.db.models import Customer

client = TestClient(app)


def test_create_customer():
    customer_data = {
        "name": "ABC",
        "mobile": "1234567897",
        "age": 30,
        "active": True,
        "status": "ACTIVE",
    }
    response = client.post("/customer/create/", json=customer_data)
    print(response.content)

    assert response.status_code == 200
    assert response.json()["name"] == customer_data["name"]
    assert response.json()["mobile"] == customer_data["mobile"]
    assert response.json()["age"] == customer_data["age"]


# def test_list_customer():
#     response = client.get("/customer/list/")
#     assert response.status_code == 200
#     assert response.json() == [{"username": "user1"}, {"username": "user2"}]
