# core/models.py
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Trip:
    id: str
    drivers: List[str] = field(default_factory=list)
    expected_pay: float = 0.0
    status: str = "Active"
    loads_str: str = "?"
    start_location: str = ""
    end_location: str = ""
    start_time: str = ""
    end_time: str = ""
    rpm: float = 0.0
    miles: float = 0.0

@dataclass
class InvoiceItem:
    type: str
    amount: float
    load_id: str

@dataclass
class Invoice:
    paid_amount: float = 0.0
    items: List[InvoiceItem] = field(default_factory=list)
    route: str = ""
    miles: float = 0.0  # agar invoice da miles bo'lsa