# core/calculator.py
import pandas as pd
from typing import Dict, List, Tuple
from core.models import Trip, Invoice

def build_dataframe(trips_data: Dict[str, Trip], invoice_data: Dict[str, Invoice]) -> pd.DataFrame:
    """Asosiy DataFrame ni yaratish"""
    rows = []
    for t_id, trip in trips_data.items():
        inv = invoice_data.get(t_id)
        paid = inv.paid_amount if inv else 0.0
        miles = trip.miles
        
        # Statusni aniqlash
        if trip.status == "Extra/Dispute":
            final_status = "Extra Pay"
        elif trip.status == "Canceled":
            final_status = "Canceled (Paid)" if paid > 0 else "Canceled (No Pay)"
        else:
            final_status = "Paid" if paid > 0 else "Unpaid"
        
        expected = trip.expected_pay
        diff = paid - expected if final_status != "Canceled (No Pay)" else 0.0
        if final_status == "Canceled (No Pay)":
            expected = 0.0
        
        for driver in trip.drivers:
            if driver == "UNKNOWN" and paid == 0 and trip.status == "Canceled":
                continue
            rows.append({
                "Driver": driver,
                "ID": t_id,
                "Status": final_status,
                "Start Location": trip.start_location,
                "Start Time": trip.start_time,
                "End Location": trip.end_location,
                "End Time": trip.end_time,
                "Kutilgan": expected,
                "Tolangan": paid,
                "Farq": diff,
                "Yuklar (Trips)": trip.loads_str,
                "Yuklar (Inv)": len(inv.items) if inv else 0,
                "RPM": trip.rpm,
                "Miles": miles, 
            })
    
    return pd.DataFrame(rows)

def compute_driver_stats(df: pd.DataFrame, driver_name: str) -> Dict:
    """Berilgan haydovchi uchun statistikani hisoblaydi"""
    driver_df = df[df['Driver'] == driver_name]
    if driver_df.empty:
        return {}
    
    total_earned = driver_df['Tolangan'].sum()
    total_trips = len(driver_df)
    avg_per_trip = total_earned / total_trips if total_trips > 0 else 0
    paid_trips = len(driver_df[driver_df['Tolangan'] > 0])
    unpaid_trips = len(driver_df[driver_df['Status'] == 'Unpaid'])
    
    has_rpm = 'RPM' in driver_df.columns and driver_df['RPM'].sum() > 0
    avg_rpm = driver_df['RPM'].mean() if has_rpm else 0

    # Miles
    has_miles = 'Miles' in driver_df.columns and driver_df['Miles'].sum() > 0
    total_miles = driver_df['Miles'].sum() if has_miles else 0
    
    return {
        'total_earned': total_earned,
        'total_trips': total_trips,
        'avg_per_trip': avg_per_trip,
        'paid_trips': paid_trips,
        'unpaid_trips': unpaid_trips,
        'avg_rpm': avg_rpm,
        'has_rpm': has_rpm,
        'completion_rate': (paid_trips / total_trips * 100) if total_trips > 0 else 0,
        'total_miles': total_miles,
        'has_miles': has_miles
    }