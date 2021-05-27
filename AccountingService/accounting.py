from pydantic import BaseModel
from typing import Optional

class AccountingRecord(BaseModel):
    item_id: int
    price: str
    tax: Optional[float]