import os
import httpx

# test en local # export SERVER_URL=http://server.internal:8000
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")


def test_create_user():
    response = httpx.post(
        f"{SERVER_URL}/users/",
        json={"name": "John Doe", "email": "johndoe@example.com", "phone": "123456789"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "johndoe@example.com"
    assert data["phone"] == "123456789"

def test_get_all_users():
    response = httpx.get(f"{SERVER_URL}/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_user():
    response = httpx.get(f"{SERVER_URL}/users/1")
    assert response.status_code in [200, 404]  # Puede que el usuario no exista aún

def test_update_user():
    response = httpx.put(
        f"{SERVER_URL}/users/1",
        json={"name": "Jane Doe", "email": "janedoe@example.com", "phone": "987654321"}
    )
    assert response.status_code in [200, 404]

def test_delete_user():
    response = httpx.delete(f"{SERVER_URL}/users/1")
    assert response.status_code in [200, 404]

if __name__ == "__main__":
    test_create_user()
    test_get_all_users()
    test_get_user()
    test_update_user()
    test_delete_user()
    print("Todas las pruebas pasaron correctamente")
