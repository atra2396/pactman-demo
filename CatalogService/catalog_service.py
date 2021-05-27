from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from CatalogService.catalog import AccountingFactory, InventoryFactory

app = FastAPI()

class OrderRequest(BaseModel):
    item_id: int
    quantity: int

class OrderResponse(BaseModel):
    total_price: int

@app.post("/order")
def order_item(request: OrderRequest):
    inventory = InventoryFactory().get_inventory()
    accounting = AccountingFactory().get_accounting()

    inventory_response = inventory.update_quantity(request.item_id, request.quantity)

    if not inventory_response:
        raise HTTPException(400, "Item not in sufficient stock to fulfill quantity requested")
    
    accounting_info = accounting.get_item_price(request.item_id)
    total_price = accounting_info["price"] * request.quantity

    return OrderResponse(total_price=total_price)


class ProviderState(BaseModel):
    state: str

@app.post("/_pact/setup_provider_state")
def setupState(provider_state: ProviderState):
    if provider_state.state == "item with id 0 exists":
        InventoryFactory.test = (True, True)
        AccountingFactory.test = (True, { "price": 10 })
    elif provider_state.state == "item with if 0 exists with 0 stock":
        InventoryFactory.test = (True, False)
        AccountingFactory.test = (True, { "price": 10 })