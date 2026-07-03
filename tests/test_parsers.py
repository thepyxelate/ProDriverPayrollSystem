# tests/test_parsers.py
import pytest
from core.parsers import TripsParser, InvoiceParser
from core.models import Trip, Invoice

def test_trips_parser(sample_trips_file_content):
    parser = TripsParser(sample_trips_file_content)
    result = parser.parse()
    
    assert len(result) == 1
    assert "T-114BSKL1H" in result
    trip = result["T-114BSKL1H"]
    
    assert trip.id == "T-114BSKL1H"
    assert trip.drivers == ["D. HODJAEV", "N. OHAI"]
    assert trip.expected_pay == 1096.15
    assert trip.rpm == 2.72
    assert trip.start_location == "ACY9 Swedesboro, NJ 08085"
    assert trip.end_location == "BOS7 Fall River, MA 02720"

# tests/test_parsers.py
def test_invoice_parser():
    content = """Invoice Number\tBlock ID\tTrip ID\tLoad ID\tStart Date\tEnd Date\tRoute\tOperator Type\tEquipment\tDistance (Mi)\tItem Type\tProgram Type\tBase Rate\tFuel Surcharge\tTolls\tDetention\tTONU\tGross Pay
INV-001\t\tT-114BSKL1H\tL-001\t2025-01-17\t2025-01-18\tACY9→BOS7\t\t\t404\tSpot\t\t1000\t50\t46.15\t0\t0\t1096.15
INV-002\t\tT-456DEF\tL-002\t2025-01-17\t2025-01-18\tJFK8→ORH3\t\t\t243\tSpot\t\t750\t30\t37.34\t0\t0\t817.34
"""
    parser = InvoiceParser(content)
    data, total = parser.parse()
    assert len(data) == 2
    assert total == 1096.15 + 817.34
    inv1 = data["T-114BSKL1H"]
    assert inv1.paid_amount == 1096.15
    assert inv1.miles == 404.0


def test_trips_parser_miles(sample_trips_file_content):
    parser = TripsParser(sample_trips_file_content)
    data = parser.parse()
    trip = data["T-114BSKL1H"]
    assert trip.miles == 404.0