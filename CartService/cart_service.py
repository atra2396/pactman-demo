import os

import requests
from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic.main import BaseModel
from .cart import Cart

app = FastAPI()

cart_db: Dict[int, Cart] = {}

@app.get("/carts/{cart_id}")
def get_cart(cart_id: int):
    if cart_id not in cart_db:
        raise HTTPException(404, "Cart not found")
    
    return cart_db[cart_id]

@app.post("/carts", status_code=201)
def create_cart():
    id = len(cart_db)
    cart = Cart(id=id, items=[])
    cart_db[id] = cart

    return id

class AddItemRequest(BaseModel):
    cart_id: int
    item_id: int
    quantity: int

@app.patch("/carts")
def add_item_to_cart(request: AddItemRequest):
    if request.cart_id not in cart_db:
        raise HTTPException(404, "Cart not found")
    
    catalog_url = get_catalog_url()
    order = requests.post(f"{catalog_url}/order", json={ "item_id": request.item_id, "quantity": request.quantity })
    if order.status_code == 400:
        raise HTTPException(400, "Not enough of item in stock to fulfill order")

    cart = cart_db[request.cart_id]
    cart.add_item(request.item_id, request.quantity, order.json()["total_price"])

def get_catalog_url() -> str:
    return os.environ.get("CATALOG_SERVICE_ENDPOINT")