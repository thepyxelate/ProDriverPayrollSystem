# core/parsers.py
import re
import csv
from io import StringIO
from collections import defaultdict
from typing import Dict, Tuple

from config import ID_PATTERN, DRIVER_PATTERN, LOADS_PATTERN, RPM_PATTERN, INVOICE_DELIMITER
from utils.helpers import parse_currency, parse_numeric, normalize_name
from core.models import Trip, Invoice, InvoiceItem

class TripsParser:
    def __init__(self, file_content: str):
        self.content = file_content
        self.trips_data: Dict[str, Trip] = {}

    def parse(self) -> Dict[str, Trip]:
        lines = self.content.splitlines()
        
        current_ids = []
        current_pay = 0.0
        current_drivers = []
        current_loads = "?"
        is_rejected = False
        is_canceled = False
        temp_locations = []
        temp_times = []
        current_rpm = 0.0
        current_miles = 0.0

        def save_block():
            nonlocal current_ids, current_pay, current_drivers, current_loads, is_canceled, is_rejected
            nonlocal temp_locations, temp_times, current_rpm, current_miles
            
            if current_ids:
                drvs = current_drivers if current_drivers else ["UNKNOWN"]
                pay = current_pay

                if is_rejected:
                    status = "Rejected"
                elif is_canceled:
                    status = "Canceled"
                else:
                    status = "Active"

                start_location = temp_locations[0] if temp_locations else ""
                end_location = ""
                
                if len(temp_locations) > 1:
                    end_location = temp_locations[-1]
                elif len(temp_locations) == 1:
                    end_location = temp_locations[0]

                start_time = temp_times[0] if temp_times else ""
                end_time = ""
                if len(temp_times) > 1:
                    end_time = temp_times[-1]

                for _id in current_ids:
                    self.trips_data[_id] = Trip(
                        id=_id,
                        drivers=drvs,
                        expected_pay=pay,
                        status=status,
                        loads_str=current_loads,
                        start_location=start_location,
                        end_location=end_location,
                        start_time=start_time,
                        end_time=end_time,
                        rpm=current_rpm,
                        miles=current_miles,
                        
                    )
            
            current_ids = []
            current_pay = 0.0
            current_drivers = []
            current_loads = "?"
            is_canceled = False
            is_rejected = False
            temp_locations = []
            temp_times = []
            current_rpm = 0.0
            current_miles = 0.0

        loc_pattern = r"([A-Z0-9]{3,6}\s+[A-Z][A-Za-z\s]+,\s+[A-Z]{2}\s+\d{5})"
        time_pattern = r"([A-Za-z]{3},\s+[A-Za-z]{3}\s+\d{1,2},\s+\d{2}:\d{2}\s+[A-Z]{3})"

        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            id_match = re.search(ID_PATTERN, line)
            if id_match:
                found_id = id_match.group(1)
                if current_ids and (current_drivers or current_pay > 0 or is_canceled or is_rejected):
                    save_block()
                current_ids.append(found_id)
                continue
            
            if "Rejected" in line:
                is_rejected = True

            if "Canceled" in line or "Cancelled" in line:
                is_canceled = True
            if line.startswith('$') and '/mi' not in line:
                current_pay = parse_currency(line)
            
            # RPM
            rpm_match = re.search(RPM_PATTERN, line)
            if rpm_match:
                rpm_str = rpm_match.group(1).replace(',', '')
                try:
                    current_rpm = float(rpm_str)
                except:
                    current_rpm = 0.0
            
            # Miles (masofa) - faqat '$' bo'lmagan va '/mi' bo'lmagan qatorlardan
            if '$' not in line and '/mi' not in line:
                miles_match = re.search(r"(\d+)\s*mi", line)
                if miles_match:
                    try:
                        current_miles = float(miles_match.group(1))
                    except:
                        current_miles = 0.0
            
            loads_match = re.search(LOADS_PATTERN, line)
            if loads_match:
                current_loads = loads_match.group(1)
            
            if current_ids:
                l_matches = re.findall(loc_pattern, line)
                for loc in l_matches:
                    if loc not in temp_locations:
                        temp_locations.append(loc)
                
                t_matches = re.findall(time_pattern, line)
                for time in t_matches:
                    if time not in temp_times:
                        temp_times.append(time)

            matches = re.findall(DRIVER_PATTERN, line)
            if matches and len(line) < 60 and not line.startswith('$') and "Load" not in line and "Trailer" not in line:
                for m in matches:
                    norm_name = normalize_name(m)
                    if norm_name not in current_drivers:
                        current_drivers.append(norm_name)
        
        save_block()
        return self.trips_data


class InvoiceParser:
    def __init__(self, file_content: str):
        self.content = file_content
        self.invoice_data: Dict[str, Invoice] = defaultdict(Invoice)
        self.total_invoice_amount = 0.0
        self.has_miles = False

    def parse(self) -> Tuple[Dict[str, Invoice], float]:
        try:
            csv_file = StringIO(self.content)
            reader = csv.DictReader(csv_file, delimiter=INVOICE_DELIMITER)
            fieldnames = reader.fieldnames
            
            # Masofa ustunini topish
            miles_col = None
            from config import INVOICE_MILES_COLUMNS
            for col in fieldnames:
                if col.lower() in [c.lower() for c in INVOICE_MILES_COLUMNS]:
                    miles_col = col
                    self.has_miles = True
                    break
            
            for row in reader:
                block_id = row.get('Block ID', '').strip()
                trip_id = row.get('Trip ID', '').strip()
                load_id = row.get('Load ID', '').strip()
                gross_pay = parse_currency(row.get('Gross Pay', '0'))
                item_type = row.get('Item Type', 'Unknown')
                route = row.get('Route', '')
                
                miles = 0.0
                if self.has_miles and miles_col in row:
                    miles_str = row.get(miles_col, '').strip()
                    if miles_str:
                        miles = parse_numeric(miles_str)
                
                self.total_invoice_amount += gross_pay
                primary_id = block_id if block_id else (trip_id if trip_id else load_id)
                
                if primary_id:
                    inv = self.invoice_data[primary_id]
                    inv.paid_amount += gross_pay
                    inv.route = route or inv.route
                    inv.items.append(InvoiceItem(
                        type=item_type,
                        amount=gross_pay,
                        load_id=load_id
                    ))
                    inv.miles += miles
            
            return dict(self.invoice_data), self.total_invoice_amount
            
        except Exception as e:
            raise RuntimeError(f"Invoice faylini o'qishda xatolik: {e}")