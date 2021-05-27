from pydantic import BaseModel

class InventoryRecord(BaseModel):
    item_id: int
    quantity: int