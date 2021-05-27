from typing import Dict
from fastapi import FastAPI, HTTPException
from .item import Item

app = FastAPI()

item_db: Dict[int, Item] = {}

@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    if item_id not in item_db:
        return HTTPException(status_code=404, detail="Item not found")
    return item_db[item_id]

@app.get("/items")
def get_all_items() -> Dict[int, Item]:
    return item_db

@app.post("/_pact/provider_state")
def setup_provider_state(provider_state: dict):
    pass