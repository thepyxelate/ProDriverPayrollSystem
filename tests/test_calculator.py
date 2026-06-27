# tests/test_calculator.py
import pandas as pd
import pytest
from core.calculator import build_dataframe, compute_driver_stats

def test_build_dataframe(sample_trip_data, sample_invoice_data):
    df = build_dataframe(sample_trip_data, sample_invoice_data)
    
    assert len(df) == 3
    assert set(df['Driver'].unique()) == {"D. HODJAEV", "N. OHAI"}
    # To'g'ri summa: 1096.15*2 + 817.34 = 3009.64
    expected_sum = 1096.15 * 2 + 817.34
    assert df['Tolangan'].sum() == pytest.approx(expected_sum, 0.01)

# tests/test_calculator.py
def test_compute_driver_stats(sample_trip_data, sample_invoice_data):
    df = build_dataframe(sample_trip_data, sample_invoice_data)
    stats = compute_driver_stats(df, "N. OHAI")
    
    assert stats['total_trips'] == 2
    assert stats['total_earned'] == pytest.approx(1096.15 + 817.34, 0.01)
    assert stats['paid_trips'] == 2
    assert stats['unpaid_trips'] == 0
    assert stats['has_rpm'] == True
    assert stats['avg_rpm'] == pytest.approx((2.72 + 3.37) / 2, 0.01)
    assert stats['completion_rate'] == 100.0
    
    # Miles testlari
    # Bu yerda sample data da Miles mavjud, shuning uchun has_miles True bo'lishi kerak
    # Agar sample data da Miles bo'lmasa, has_miles False bo'ladi
    # Sizning sample data da Invoice dan miles olinadi, shuning uchun True
    assert stats['has_miles'] == True
    assert stats['total_miles'] == pytest.approx(404.0 + 243.0, 0.01)