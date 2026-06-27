# tests/conftest.py
import sys
import os

# Loyiha ildizini (ProDriverPayrollSystem) Python path ga qo'shish
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from core.models import Trip, Invoice, InvoiceItem


# tests/conftest.py
@pytest.fixture
def sample_trip_data():
    """Namuna Trip maʼlumotlari"""
    return {
        "T-123ABC": Trip(
            id="T-123ABC",
            drivers=["D. HODJAEV", "N. OHAI"],
            expected_pay=1096.15,
            status="Active",
            loads_str="3/4",
            start_location="ACY9 Swedesboro, NJ 08085",
            end_location="BOS7 Fall River, MA 02720",
            start_time="Sat, Jan 17, 18:26 EST",
            end_time="Sun, Jan 18, 07:00 EST",
            rpm=2.72,
            miles=404.0   
        ),
        "T-456DEF": Trip(
            id="T-456DEF",
            drivers=["N. OHAI"],
            expected_pay=817.34,
            status="Active",
            loads_str="2/2",
            start_location="JFK8 Staten Island, NY 10314",
            end_location="ORH3 CHARLTON, MA 01507",
            start_time="Sat, Jan 17, 19:15 EST",
            end_time="Sun, Jan 18, 03:16 EST",
            rpm=3.37,
            miles=243.0   
        )
    }


@pytest.fixture
def sample_invoice_data():
    """Namuna Invoice maʼlumotlari"""
    return {
        "T-123ABC": Invoice(
            paid_amount=1096.15,
            items=[
                InvoiceItem(type="Spot", amount=1096.15, load_id="L-001")
            ],
            route="ACY9 → BOS7",
            miles=404.0
        ),
        "T-456DEF": Invoice(
            paid_amount=817.34,
            items=[
                InvoiceItem(type="Spot", amount=817.34, load_id="L-002")
            ],
            route="JFK8 → ORH3",
            miles=243.0
        )
    }


@pytest.fixture
def sample_trips_file_content():
    """Trips.txt namuna mazmuni"""
    return """
T-114BSKL1H
Spot
1
ACY9 Swedesboro, NJ 08085
Sat, Jan 17, 18:26 EST
6
BOS7 Fall River, MA 02720
Sun, Jan 18, 07:00 EST
404 mi
13h 5m
53' Trailer
P
$1,096.15
$2.72/mi
D. Hodjaev, N. Ohai
3/4 Loads
1
"""