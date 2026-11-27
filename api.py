from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

VERSION = "1.0.0"

app = FastAPI(title="Tienda API", version=VERSION)


class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int = 0


productos: dict[int, Producto] = {
    1: Producto(nombre="Teclado", precio=499.0, stock=10),
    2: Producto(nombre="Mouse", precio=249.5, stock=25),
}


@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la Tienda API", "version": VERSION}


@app.get("/salud")
def salud():
    return {"estado": "ok"}


@app.get("/productos")
def listar_productos():
    return [{"id": i, **p.model_dump()} for i, p in productos.items()]


@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    if producto_id not in productos:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"id": producto_id, **productos[producto_id].model_dump()}


@app.post("/productos", status_code=201)
def crear_producto(producto: Producto):
    nuevo_id = max(productos, default=0) + 1
    productos[nuevo_id] = producto
    return {"id": nuevo_id, **producto.model_dump()}
