from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_inicio():
    r = client.get("/")
    assert r.status_code == 200
    assert "version" in r.json()


def test_salud():
    assert client.get("/salud").json() == {"estado": "ok"}


def test_listar_productos():
    r = client.get("/productos")
    assert r.status_code == 200
    assert len(r.json()) >= 2


def test_producto_inexistente():
    assert client.get("/productos/999").status_code == 404


def test_crear_producto():
    r = client.post("/productos", json={"nombre": "Monitor", "precio": 3200, "stock": 3})
    assert r.status_code == 201
    assert r.json()["nombre"] == "Monitor"
