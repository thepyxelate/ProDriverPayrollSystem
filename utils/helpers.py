# utils/helpers.py
import re
import pandas as pd

def parse_currency(value_str):
    """Valyuta qiymatini float ga aylantirish"""
    if not value_str or pd.isna(value_str) or str(value_str).strip() == '' or '--' in str(value_str):
        return 0.0
    
    clean = str(value_str).replace('$', '').replace('\xa0', ' ').strip()
    if not clean:
        return 0.0
    
    has_comma = ',' in clean
    has_dot = '.' in clean
    is_euro = False
    
    if has_comma and not has_dot:
        is_euro = True
    elif has_comma and has_dot:
        if clean.rfind(',') > clean.rfind('.'):
            is_euro = True
    
    if is_euro:
        clean = clean.replace(' ', '').replace('.', '').replace(',', '.')
    else:
        clean = clean.replace(' ', '').replace(',', '')
    
    try:
        return float(clean)
    except:
        return 0.0

def parse_numeric(value_str):
    """Har qanday raqamli qiymatni float ga aylantirish (masofa, sonlar)"""
    if not value_str or pd.isna(value_str):
        return 0.0
    clean = str(value_str).strip()
    clean = re.sub(r'[^\d.]', '', clean)
    try:
        return float(clean)
    except:
        return 0.0

def format_currency(value):
    """Valyutani 1234,56 ko'rinishida formatlash"""
    try:
        if pd.isna(value):
            return "0,00"
        s = f"{value:.2f}"
        return s.replace('.', ',')
    except:
        return "0,00"

def normalize_name(name):
    """Ismni katta harflarga va bo'shliqlarni tozalash"""
    return name.strip().upper()