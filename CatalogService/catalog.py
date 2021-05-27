from pydantic import BaseModel
import os

import requests

class CatalogItem(BaseModel):
    id: int
    item_id: int
    item_name: str
    item_price: int
    item_quantity_remaining: int


class Inventory:
    def _get_inventory_url(self) -> str:
        return os.environ.get("INVENTORY_SERVICE_ENDPOINT")

    def update_quantity(self, item_id: int, quantity: int):
        inventory_url = self._get_inventory_url()
        return requests.patch(f"{inventory_url}/items/{item_id}",
                                        json={ "quantity_delta": quantity })

class FakeInventory:

    def __init__(self, response: dict) -> None:
        self.response = response

    def update_quantity(self, item_id: int, quantity: int):
        return self.response

class InventoryFactory:

    test = (False, "")
    
    def get_inventory(self) -> Inventory:
        if InventoryFactory.test[0]:
            return FakeInventory(InventoryFactory.test[1])
        return Inventory()


class Accounting:
    def _get_accounting_serivce_url(self) -> str:
        return os.environ.get("ACCOUNTING_SERVICE_ENDPOINT")

    def get_item_price(self, item_id: int):
        accounting_url = self._get_accounting_serivce_url()
        return requests.get(f"{accounting_url}/items/{item_id}").json()

class FakeAccounting:

    def __init__(self, response: dict) -> None:
        self.response = response

    def get_item_price(self, item_id: int):
        return self.response

class AccountingFactory:

    test = (False, "")
    
    def get_accounting(self) -> Accounting:
        if AccountingFactory.test[0]:
            return FakeAccounting(AccountingFactory.test[1])
        return Accounting()
