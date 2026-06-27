# config.py
# =============================================================================
# KONSTANTALAR VA SOZLAMALAR
# =============================================================================

# Parser patternlari
ID_PATTERN = r"(B-[A-Z0-9]{8,9}|T-[A-Z0-9]{8,9}|\b[0-9][0-9A-Z]{8,9}\b)"
DRIVER_PATTERN = r"(?i)([a-z]\.\s+[a-z]+(?:\s+[a-z]+)?)"
LOADS_PATTERN = r"(?i)(\d+(?:/\d+)?)\s+Loads"
RPM_PATTERN = r"\$\s*([\d,]+\.\d{2})\s*/\s*mi"

# Fayl sozlamalari
INVOICE_DELIMITER = '\t'
INVOICE_MILES_COLUMNS = ['Distance (Mi)', 'Miles', 'Distance', 'Mileage']  # avtomatik aniqlash uchun

# Valyuta formati
CURRENCY_LOCALE = 'uz'  # 'en' yoki 'uz' - 'uz' da vergul bilan ajratish

# UI ranglar
COLOR_SCHEMES = {
    'primary': ['#3a7bd5', '#00d2ff', '#00fff2'],
    'secondary': ['#ff9068', '#f7b733', '#fc4a1a'],
    'rpm': ['#f093fb', '#4facfe', '#00f2fe'],
}