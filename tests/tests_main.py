import os
os.environ["TESTING"] = "True"  # Asegurar que FastAPI use SQLite en memoria

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db, engine, SessionLocal
from app.main import app

# Crear y limpiar la base de datos antes de cada prueba
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)  # Crear las tablas antes de cada prueba
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)  #  Eliminar las tablas después de cada prueba

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

# Prueba para crear un usuario
def test_create_user(client):
    response = client.post(
        "/users/",
        json={"name": "John Doe", "email": "johndoe@example.com", "phone": "123456789"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "johndoe@example.com"
    assert data["phone"] == "123456789"

# Prueba: Obtener todos los usuarios
def test_get_all_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# Prueba: Obtener un usuario por ID
def test_get_user_by_id(client):
    # Crear usuario de prueba
    client.post("/users/", json={"name": "Alice", "email": "alice@example.com", "phone": "987654321"})
    
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"

# Prueba: Actualizar un usuario
def test_update_user(client):
    # Crear usuario de prueba
    client.post("/users/", json={"name": "Bob", "email": "bob@example.com", "phone": "555555555"})
    
    response = client.put("/users/1", json={"name": "Bob Updated", "email": "bob_new@example.com", "phone": "666666666"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bob Updated"
    assert data["email"] == "bob_new@example.com"
    assert data["phone"] == "666666666"

# Prueba: Eliminar un usuario
def test_delete_user(client):
    # Crear usuario de prueba
    client.post("/users/", json={"name": "Charlie", "email": "charlie@example.com", "phone": "777777777"})
    
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}
    
    # Verificar que el usuario ya no existe
    response = client.get("/users/1")
    assert response.status_code == 404
