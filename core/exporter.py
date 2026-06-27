# core/exporter.py
import pandas as pd
from io import BytesIO
from datetime import datetime
from typing import Optional

from utils.helpers import format_currency

def generate_txt_report(df: pd.DataFrame) -> str:
    """TXT hisobot yaratish"""
    lines = []
    lines.append("="*160)
    lines.append(f"PRO DRIVER PAYROLL REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("="*160)
    lines.append("")
    
    has_miles = 'Miles' in df.columns and df['Miles'].sum() > 0
    has_rpm = 'RPM' in df.columns and df['RPM'].sum() > 0
    
    for driver in sorted(df['Driver'].unique()):
        d_df = df[df['Driver'] == driver]
        paid_sum = d_df['Tolangan'].sum()
        pending_sum = d_df[d_df['Status'] == 'Unpaid']['Kutilgan'].sum()
        avg_rpm = d_df['RPM'].mean() if has_rpm else 0
        total_miles = d_df['Miles'].sum() if has_miles else 0
        
        lines.append(f"\n{'='*160}")
        lines.append(f"👤 HAYDOVCHI: {driver}")
        lines.append(f"   💰 Jami To'landi: {format_currency(paid_sum)}")
        lines.append(f"   ⏳ Kutilmoqda: {format_currency(pending_sum)}")
        if has_miles:
            lines.append(f"   📏 Jami Miles: {total_miles:.0f}")
        if has_rpm:
            lines.append(f"   📈 Oʻrtacha RPM: {avg_rpm:.2f}")
        lines.append(f"{'='*160}")
        
        # Sarlavha
        header = f"{'ID':<16} {'Start Location':<30} {'Start Time':<25} {'End Location':<30} {'End Time':<25} {'Kutilgan':<12} {'To\'langan':<12} {'Farq':<10}"
        if has_rpm:
            header += " {'RPM':<10}"
        if has_miles:
            header += " {'Miles':<10}"
        lines.append(header)
        lines.append("-" * 160)
        
        for _, row in d_df.iterrows():
            start_loc = (row['Start Location'][:27] + '...') if len(row['Start Location']) > 30 else row['Start Location']
            end_loc = (row['End Location'][:27] + '...') if len(row['End Location']) > 30 else row['End Location']
            start_time = (row['Start Time'][:22] + '...') if len(row['Start Time']) > 25 else row['Start Time']
            end_time = (row['End Time'][:22] + '...') if len(row['End Time']) > 25 else row['End Time']
            
            kut = format_currency(row['Kutilgan']) if isinstance(row['Kutilgan'], (int, float)) else str(row['Kutilgan'])
            tol = format_currency(row['Tolangan']) if isinstance(row['Tolangan'], (int, float)) else str(row['Tolangan'])
            far = format_currency(row['Farq']) if isinstance(row['Farq'], (int, float)) else str(row['Farq'])
            
            line = (f"{row['ID']:<16} {start_loc:<30} {start_time:<25} {end_loc:<30} {end_time:<25} "
                    f"{kut:<12} {tol:<12} {far:<10}")
            if has_rpm:
                rpm_val = row.get('RPM', 0)
                line += f" {rpm_val:<10.2f}"
            if has_miles:
                miles_val = row.get('Miles', 0)
                line += f" {miles_val:<10.0f}"
            lines.append(line)
        lines.append("")
    
    lines.append("\n" + "="*160)
    lines.append(f"UMUMIY JAMI TO'LANGAN: {format_currency(df['Tolangan'].sum())}")
    lines.append(f"UMUMIY KUTILMOQDA: {format_currency(df[df['Status'] == 'Unpaid']['Kutilgan'].sum())}")
    if has_miles:
        total_miles_all = df['Miles'].sum()
        lines.append(f"UMUMIY JAMI MILES: {total_miles_all:.0f}")
    if has_rpm:
        overall_avg_rpm = df['RPM'].mean()
        lines.append(f"UMUMIY OʻRTACHA RPM: {overall_avg_rpm:.2f}")
    lines.append("="*160)
    return "\n".join(lines)


def generate_excel_report(df: pd.DataFrame) -> Optional[BytesIO]:
    """Excel hisobot - Miles va RPM ustunlari bilan"""
    output = BytesIO()
    try:
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Formatlar
            header_format = workbook.add_format({
                'bold': True, 'bg_color': '#4472C4', 'font_color': 'white',
                'border': 1, 'align': 'center', 'valign': 'vcenter'
            })
            currency_format = workbook.add_format({'num_format': '0.00', 'border': 1})
            number_format = workbook.add_format({'num_format': '0', 'border': 1})      # Miles uchun
            avg_format = workbook.add_format({'num_format': '0.0', 'border': 1})       # RPM uchun (bir xona)
            text_format = workbook.add_format({'border': 1, 'align': 'left'})
            total_format = workbook.add_format({
                'bold': True, 'font_size': 14, 'bg_color': "#4444C4",
                'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'
            })
            totalgross_format = workbook.add_format({'bold': True, 'align': 'left'})
            
            has_rpm = 'RPM' in df.columns and df['RPM'].sum() > 0
            has_miles = 'Miles' in df.columns and df['Miles'].sum() > 0
            
            # Summary sheet
            summary_data = []
            for driver in sorted(df['Driver'].unique()):
                d_df = df[df['Driver'] == driver]
                avg_rpm = d_df['RPM'].mean() if has_rpm else 0
                total_miles = d_df['Miles'].sum() if has_miles else 0
                summary_data.append({
                    'Driver': driver,
                    'Total Paid': d_df['Tolangan'].sum(),
                    'Total Pending': d_df[d_df['Status'] == 'Unpaid']['Kutilgan'].sum(),
                    'Total Trips': len(d_df),
                    'Total Miles': total_miles if has_miles else None,
                    'Avg RPM': avg_rpm if has_rpm else None
                })
            
            summary_df = pd.DataFrame(summary_data)
            
            # RPM ni bir xonagacha yaxlitlash
            if has_rpm:
                summary_df['Avg RPM'] = summary_df['Avg RPM'].round(1)
            
            summary_df.to_excel(writer, sheet_name='Summary', index=False, startrow=1)
            ws_summary = writer.sheets['Summary']
            
            # Sarlavhalarni yozish
            for i, col in enumerate(summary_df.columns):
                ws_summary.write(1, i, col, header_format)
            
            # Ma'lumotlarni formatlab yozish (to_excel default formatdan qochish uchun)
            for row_idx, row in summary_df.iterrows():
                row_num = row_idx + 2  # startrow=1, keyin 2-qatordan boshlab
                for col_idx, val in enumerate(row):
                    if col_idx == 0:  # Driver (matn)
                        ws_summary.write(row_num, col_idx, val, text_format)
                    elif col_idx in [1, 2]:  # Total Paid, Total Pending (pul)
                        ws_summary.write(row_num, col_idx, val, currency_format)
                    elif col_idx == 3:  # Total Trips (butun son)
                        ws_summary.write(row_num, col_idx, val, number_format)
                    elif has_miles and col_idx == 4:  # Total Miles
                        ws_summary.write(row_num, col_idx, val, number_format)
                    elif has_rpm and col_idx == (4 + (1 if has_miles else 0)):  # Avg RPM
                        ws_summary.write(row_num, col_idx, val, avg_format)
            
            # Ustun kengliklari
            ws_summary.set_column(0, 0, 25)  # Driver
            ws_summary.set_column(1, 3, 15)  # Total Paid, Total Pending, Total Trips
            col_idx = 4
            if has_miles:
                ws_summary.set_column(col_idx, col_idx, 15)
                col_idx += 1
            if has_rpm:
                ws_summary.set_column(col_idx, col_idx, 15)
            
            # Har bir haydovchi uchun alohida sheet
            for driver in sorted(df['Driver'].unique()):
                d_df = df[df['Driver'] == driver].copy()
                cols = ['ID', 'Start Location', 'Start Time', 'End Location', 'End Time', 'Kutilgan', 'Tolangan', 'Farq']
                if has_rpm:
                    cols.append('RPM')
                if has_miles:
                    cols.append('Miles')
                
                export_df = d_df[cols]
                sheet_name = driver.replace('/', '-')[:31]
                ws = workbook.add_worksheet(sheet_name)
                
                ws.write(1, 0, f'Driver: {driver}', workbook.add_format({'bold': True, 'font_size': 14}))
                
                # Sarlavhalar
                for i, h in enumerate(cols):
                    ws.write(2, i, h, header_format)
                
                # Ma'lumotlar
                for row_idx, row in enumerate(export_df.itertuples(index=False)):
                    for col_idx, val in enumerate(row):
                        if isinstance(val, (int, float)):
                            if col_idx in [5, 6, 7]:  # Kutilgan, Tolangan, Farq
                                ws.write(row_idx+3, col_idx, val, currency_format)
                            elif has_rpm and cols[col_idx] == 'RPM':
                                ws.write(row_idx+3, col_idx, val, avg_format)  # RPM ni 0.0 formatda
                            elif has_miles and cols[col_idx] == 'Miles':
                                ws.write(row_idx+3, col_idx, val, number_format)
                            else:
                                ws.write(row_idx+3, col_idx, val, text_format)
                        else:
                            ws.write(row_idx+3, col_idx, val, text_format)
                
                # Jami qator
                last_row = len(d_df) + 3
                total_tolangan = d_df['Tolangan'].sum()
                ws.merge_range(last_row, 4, last_row, 5, 'TOTAL GROSS:', totalgross_format)
                ws.write(last_row, 6, total_tolangan, total_format)
                
                # Ustun kengliklari
                ws.set_column(0, 0, 16)  # ID
                ws.set_column(1, 1, 30)  # Start Location
                ws.set_column(2, 2, 25)  # Start Time
                ws.set_column(3, 3, 30)  # End Location
                ws.set_column(4, 4, 25)  # End Time
                ws.set_column(5, 7, 15)  # Kutilgan, Tolangan, Farq
                col_idx = 8
                if has_rpm:
                    ws.set_column(col_idx, col_idx, 15)
                    col_idx += 1
                if has_miles:
                    ws.set_column(col_idx, col_idx, 15)
        
        output.seek(0)
        return output
    except Exception as e:
        print(f"Excel xatosi: {e}")
        return None