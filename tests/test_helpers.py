# tests/test_helpers.py
import pytest
from utils.helpers import parse_currency, parse_numeric, format_currency, normalize_name

def test_parse_currency():
    assert parse_currency("$1,096.15") == 1096.15
    assert parse_currency("$817,34") == 817.34  # Evropa formati
    assert parse_currency("--") == 0.0
    assert parse_currency("") == 0.0

def test_parse_numeric():
    assert parse_numeric("404 mi") == 404.0
    assert parse_numeric("1,234.56") == 1234.56
    assert parse_numeric("") == 0.0

def test_format_currency():
    assert format_currency(1096.15) == "1096,15"
    assert format_currency(817.34) == "817,34"
    assert format_currency(0.0) == "0,00"

def test_normalize_name():
    assert normalize_name("d. hodjaev") == "D. HODJAEV"
    assert normalize_name("  n. ohai  ") == "N. OHAI"