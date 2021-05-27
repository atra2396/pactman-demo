from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from InventoryService.inventory import InventoryRecord

app = FastAPI()

class Database:
    db: Dict[int, InventoryRecord] = {}

@app.get("/items/{item_id}")
def get_inventory_for_item(item_id: int) -> InventoryRecord:
    if item_id not in Database.db:
        raise HTTPException(404, "Inventory record not found")
    return Database.db[item_id]

class ItemQuantity(BaseModel):
    quantity_delta: int

@app.patch("/items/{item_id}", status_code=200)
def update_item_quantity(item_id: int, item_quantity: ItemQuantity):
    if item_id not in Database.db:
        raise HTTPException(404, "Inventory record not found")
    record = Database.db[item_id]
    if record.quantity - item_quantity.quantity_delta < 0:
        raise HTTPException(400, "Quantity requested is not in stock")
    record.quantity = record.quantity - item_quantity.quantity_delta

@app.get("/items/")
def get_all_records():
    return Database.db

class ProviderState(BaseModel):
    state: str

@app.post("/_pact/setup_provider_state")
def setupState(provider_state: ProviderState):
    Database.db = {}
    if provider_state.state == "item with id 0 has at least 5 units in stock":
        Database.db[0] = InventoryRecord(item_id=0, quantity=6)
