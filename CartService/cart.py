from typing import List
from pydantic import BaseModel

class CartItem(BaseModel):
    item_id: int
    item_quantity: int
    total_cost: int

class Cart(BaseModel):
    id: int
    items: List[CartItem]

    def add_item(self, item_id: int, quantity: int, cost: int):
        item = [i for i in self.items if i.item_id == item_id]
        if len(item) == 0:
            item = CartItem(item_id=item_id, item_quantity=quantity, total_cost=cost)
            self.items.append(item)
        else:
            item[0].item_quantity += quantity
            item[0].total_cost += cost
