# tests/test_exporter.py
import io
import pandas as pd
from core.exporter import generate_txt_report, generate_excel_report
from core.calculator import build_dataframe

def test_generate_txt_report(sample_trip_data, sample_invoice_data):
    df = build_dataframe(sample_trip_data, sample_invoice_data)
    report = generate_txt_report(df)
    assert "PRO DRIVER PAYROLL REPORT" in report
    assert "N. OHAI" in report
    assert "UMUMIY JAMI TO'LANGAN" in report
    assert "1096,15" in report

def test_generate_excel_report(sample_trip_data, sample_invoice_data):
    df = build_dataframe(sample_trip_data, sample_invoice_data)
    excel_bytes = generate_excel_report(df)
    assert excel_bytes is not None
    
    # Excel faylini o'qish
    df_result = pd.read_excel(io.BytesIO(excel_bytes.getvalue()), sheet_name='Summary', header=1)
    assert not df_result.empty
    assert 'Driver' in df_result.columns
    assert 'Total Miles' in df_result.columns  
    assert 'Avg RPM' in df_result.columns      