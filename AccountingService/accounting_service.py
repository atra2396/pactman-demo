from typing import Dict
from fastapi import FastAPI, HTTPException
from AccountingService.accounting import AccountingRecord
from pydantic import BaseModel

app = FastAPI()

class Database:
    db: Dict[int, AccountingRecord] = {}

@app.get("/items/{item_id}")
def get_accounting_record(item_id: int):
    if item_id not in Database.db:
        raise HTTPException(404, "AccouningRecord not found")
    return Database.db[item_id]


class ProviderState(BaseModel):
    state: str

@app.post("/_pact/setup_provider_state")
def setupState(provider_state: ProviderState):
    Database.db = {}
    if provider_state.state == "item with id 0 has price 10":
        Database.db[0] = AccountingRecord(item_id=0, price=10, tax=1.5)