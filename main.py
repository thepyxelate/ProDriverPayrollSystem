import streamlit as st
import re
import csv
import pandas as pd
from io import StringIO, BytesIO
from datetime import datetime
from collections import defaultdict

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Pro Driver Payroll System",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. ADVANCED STYLING (PROFESSIONAL DARK THEME)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #0F1116 0%, #1a1d29 100%);
        color: #E2E8F0;
    }
    
    .hero-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-weight: 800;
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
        text-shadow: 0 0 80px rgba(102, 126, 234, 0.5);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.4)); }
        to { filter: drop-shadow(0 0 30px rgba(118, 75, 162, 0.6)); }
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #94A3B8;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    div[data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 12px 48px 0 rgba(102, 126, 234, 0.3);
    }
    
    div[data-testid="stMetric"]:hover::before {
        opacity: 1;
    }
    
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
        font-size: 0.875rem;
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div[data-testid="stMetricValue"] {
        font-weight: 700;
        font-size: 2rem;
        color: #F8FAFC !important;
        margin: 0.5rem 0;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #13151C 0%, #1a1d29 100%);
        border-right: 1px solid rgba(71, 85, 105, 0.3);
    }
    
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    div[data-testid="stFileUploader"] {
        background: rgba(30, 41, 59, 0.6);
        border: 2px dashed rgba(100, 116, 139, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s;
    }
    
    div[data-testid="stFileUploader"]:hover {
        border-color: rgba(102, 126, 234, 0.5);
        background: rgba(30, 41, 59, 0.8);
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.6) !important;
        backdrop-filter: blur(10px);
        color: #E2E8F0 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(100, 116, 139, 0.3) !important;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(30, 41, 59, 0.8) !important;
        border-color: rgba(102, 126, 234, 0.5) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(100, 116, 139, 0.3) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    div[data-baseweb="select"] > div {
        background: rgba(45, 55, 72, 0.8) !important;
        border: 1px solid rgba(100, 116, 139, 0.3) !important;
        border-radius: 8px !important;
        transition: all 0.3s;
    }
    
    div[data-baseweb="select"]:hover > div {
        border-color: rgba(102, 126, 234, 0.5) !important;
    }
    
    .stAlert {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 12px;
        border-left: 4px solid;
    }
    
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(100, 116, 139, 0.3), transparent);
        margin: 2rem 0;
    }
    
    .card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.4);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(100, 116, 139, 0.6);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(102, 126, 234, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. UTILITY FUNCTIONS & PARSERS
# ==============================================================================

ID_PATTERN = r"(B-[A-Z0-9]{8,9}|T-[A-Z0-9]{8,9}|\b[0-9][0-9A-Z]{8,9}\b)"
DRIVER_PATTERN = r"(?i)([a-z]\.\s+[a-z]+(?:\s+[a-z]+)?)"
LOADS_PATTERN = r"(?i)(\d+(?:/\d+)?)\s+Loads"

def parse_currency(value_str):
    """Parse currency values with high precision"""
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

def format_currency(value):
    """Format currency without dollar sign and without comma separator"""
    return f"{value:.2f}"

def normalize_name(name):
    """Normalize driver names"""
    return name.strip().upper()

class TripsParser:
    """Enhanced trips file parser with improved location and time tracking"""
    
    def __init__(self, file_content):
        self.content = file_content
        self.trips_data = {}
        self.multi_driver_trips = []

    def parse(self):
        lines = self.content.splitlines()
        
        current_ids = []
        current_pay = 0.0
        current_drivers = []
        current_loads = "?"
        is_canceled = False
        temp_locations = []
        temp_times = []

        def save_block():
            nonlocal current_ids, current_pay, current_drivers, current_loads, is_canceled
            nonlocal temp_locations, temp_times
            
            if current_ids:
                drvs = current_drivers if current_drivers else ["UNKNOWN"]
                pay = current_pay
                status = "Canceled" if is_canceled else "Active"
                
                # FIXED: Improved location parsing
                start_location = temp_locations[0] if temp_locations else ""
                end_location = ""
                
                # Get end location (last unique location different from start)
                if len(temp_locations) > 1:
                    # Find last location that's different from start
                    for loc in reversed(temp_locations):
                        if loc != start_location:
                            end_location = loc
                            break
                    # If all locations are same, use the last one anyway
                    if not end_location:
                        end_location = temp_locations[-1]
                
                # Time parsing
                start_time = temp_times[0] if temp_times else ""
                end_time = ""
                if len(temp_times) > 1:
                    end_time = temp_times[-1]

                if len(drvs) > 1 or (drvs == ["UNKNOWN"]):
                    for _id in current_ids:
                        self.multi_driver_trips.append({
                            'id': _id,
                            'drivers': drvs,
                            'status': status
                        })

                for _id in current_ids:
                    self.trips_data[_id] = {
                        'drivers': drvs,
                        'expected_pay': pay,
                        'status': status,
                        'loads_str': current_loads,
                        'start_location': start_location,
                        'end_location': end_location,
                        'start_time': start_time,
                        'end_time': end_time
                    }
            
            current_ids = []
            current_pay = 0.0
            current_drivers = []
            current_loads = "?"
            is_canceled = False
            temp_locations = []
            temp_times = []

        # IMPROVED: Better regex patterns
        loc_pattern = r"([A-Z0-9]{3,6}\s+[A-Z][A-Za-z\s]+,\s+[A-Z]{2}\s+\d{5})"
        time_pattern = r"([A-Za-z]{3},\s+[A-Za-z]{3}\s+\d{1,2},\s+\d{2}:\d{2}\s+[A-Z]{3})"

        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            id_match = re.search(ID_PATTERN, line)
            if id_match:
                found_id = id_match.group(1)
                if current_ids and (current_drivers or current_pay > 0 or is_canceled):
                    save_block()
                current_ids.append(found_id)
                continue

            if "Canceled" in line or "Cancelled" in line:
                is_canceled = True
            if line.startswith('$') and '/mi' not in line:
                current_pay = parse_currency(line)
            
            loads_match = re.search(LOADS_PATTERN, line)
            if loads_match:
                current_loads = loads_match.group(1)
            
            if current_ids:
                # Find all locations in the line
                l_matches = re.findall(loc_pattern, line)
                for loc in l_matches:
                    if loc not in temp_locations:  # Avoid duplicates
                        temp_locations.append(loc)
                
                # Find all times in the line
                t_matches = re.findall(time_pattern, line)
                for time in t_matches:
                    if time not in temp_times:  # Avoid duplicates
                        temp_times.append(time)

            matches = re.findall(DRIVER_PATTERN, line)
            if matches and len(line) < 60 and not line.startswith('$') and "Load" not in line and "Trailer" not in line:
                for m in matches:
                    norm_name = normalize_name(m)
                    if norm_name not in current_drivers:
                        current_drivers.append(norm_name)
        
        save_block()
        return self.trips_data, self.multi_driver_trips

class InvoiceParser:
    """Enhanced invoice file parser"""
    
    def __init__(self, file_content):
        self.content = file_content
        self.invoice_data = defaultdict(lambda: {'paid_amount': 0.0, 'items': [], 'route': ''})
        self.total_invoice_amount = 0.0

    def parse(self):
        try:
            csv_file = StringIO(self.content)
            reader = csv.DictReader(csv_file, delimiter='\t')
            
            for row in reader:
                block_id = row.get('Block ID', '').strip()
                trip_id = row.get('Trip ID', '').strip()
                load_id = row.get('Load ID', '').strip()
                gross_pay = parse_currency(row.get('Gross Pay', '0'))
                item_type = row.get('Item Type', 'Unknown')
                route = row.get('Route', '')
                
                self.total_invoice_amount += gross_pay
                primary_id = block_id if block_id else (trip_id if trip_id else load_id)
                
                if primary_id:
                    self.invoice_data[primary_id]['paid_amount'] += gross_pay
                    if route:
                        self.invoice_data[primary_id]['route'] = route
                    self.invoice_data[primary_id]['items'].append({
                        'type': item_type,
                        'amount': gross_pay,
                        'load_id': load_id
                    })
            
            return self.invoice_data, self.total_invoice_amount
            
        except Exception as e:
            st.error(f"❌ Invoice faylini o'qishda xatolik: {e}")
            return {}, 0

# ==============================================================================
# 4. UI COMPONENTS
# ==============================================================================

def render_hero_header():
    """Render hero header section"""
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🚚 Pro Driver Payroll System</div>
        <div class="hero-subtitle">Professional Dispatch & Accounting Data Management</div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render enhanced sidebar"""
    with st.sidebar:
        st.markdown("""
        <div class="logo-container">
            <img src="https://cdn-icons-png.flaticon.com/512/2554/2554978.png" width="80">
            <h3 style="margin-top: 1rem; color: #E2E8F0;">Payroll Manager</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📁 Fayllarni Yuklash")
        st.caption("Quyidagi formatdagi fayllarni yuklang")
        
        trips_file = st.file_uploader(
            "📋 Trips File",
            type=['txt'],
            help="Dispatch tomonidan tayyorlangan trips fayli",
            key="trips_uploader"
        )
        
        invoice_file = st.file_uploader(
            "💰 Invoice File",
            type=['txt'],
            help="Buxgalteriya invoice fayli (TSV format)",
            key="invoice_uploader"
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset", use_container_width=True, type="secondary"):
                st.session_state.clear()
                st.rerun()
        
        with col2:
            if st.button("ℹ️ Help", use_container_width=True, type="secondary"):
                st.session_state['show_help'] = not st.session_state.get('show_help', False)
        
        if st.session_state.get('show_help', False):
            with st.expander("📖 Ko'rsatmalar", expanded=True):
                st.markdown("""
                **Fayl Formatlari:**
                - **Trips File**: Dispatch ma'lumotlari (.txt)
                - **Invoice File**: Tab-separated values (.txt)
                
                **Qadamlar:**
                1. Ikkala faylni yuklang
                2. Avtomatik parsing kutiladi
                3. Muammoli yuklarni biriktiring
                4. Hisobotni ko'ring va yuklab oling
                """)
        
        st.markdown("---")
        st.caption("v4.2 Fixed | Made with ❤️")
        st.caption(f"Last update: {datetime.now().strftime('%H:%M')}")
        
        return trips_file, invoice_file

def render_metrics_dashboard(df, invoice_total):
    """Render KPI metrics dashboard"""
    st.markdown("### 📊 Dashboard - Asosiy Ko'rsatkichlar")
    
    total_paid = df['Tolangan'].sum()
    total_drivers = df['Driver'].nunique()
    
    if "NOMA'LUM (UNKNOWN)" in df['Driver'].unique():
        total_drivers -= 1
    
    total_trips = len(df)
    avg_pay = total_paid / total_drivers if total_drivers > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Haydovchilar",
            value=f"{total_drivers}",
            delta=f"{total_trips} trips",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            label="💵 Jami To'langan",
            value=format_currency(total_paid),
            delta=f"Avg: {format_currency(avg_pay)}",
            delta_color="off"
        )
    
    with col3:
        st.metric(
            label="📄 Invoice Total",
            value=format_currency(invoice_total),
            delta=None,
            delta_color="off"
        )
    
    with col4:
        diff = total_paid - invoice_total
        st.metric(
            label="⚖️ Farq",
            value=format_currency(diff),
            delta="OK" if abs(diff) < 1 else "Check",
            delta_color="normal" if abs(diff) < 1 else "inverse"
        )

def render_assignment_section(ids_to_resolve, trips_data, invoice_data, sorted_drivers_list):
    """FIXED: Render manual assignment section with working button"""
    if not ids_to_resolve:
        st.success("✅ Barcha yuklar muvaffaqiyatli biriktirilgan!")
        return
    
    st.warning(f"⚠️ **E'tibor:** {len(ids_to_resolve)} ta yukni haydovchiga biriktirish kerak")
    
    with st.expander("🔧 Yuklarni Haydovchilarga Biriktirish", expanded=True):
        st.markdown("""
        <div style='background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <h4 style='margin: 0; color: #818CF8;'>📌 Muammoli Yuklar Turlari:</h4>
            <ul style='margin: 0.5rem 0 0 0; color: #CBD5E0;'>
                <li><strong>Multi-Driver:</strong> Bir nechta haydovchi belgilangan</li>
                <li><strong>No Driver:</strong> Haydovchi aniqlanmagan (to'lov mavjud)</li>
                <li><strong>Extra Pay:</strong> Trips faylida yo'q (eski/dispute)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        for idx, item in enumerate(ids_to_resolve):
            t_id = item['id']
            reason = item['reason']
            options = item['options']
            
            current_drivers = trips_data[t_id]['drivers']
            default_idx = 0
            
            if len(current_drivers) == 1 and current_drivers[0] in options:
                default_idx = options.index(current_drivers[0])
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"**🆔 ID:** `{t_id}`")
                
                reason_color = "#F59E0B" if "Multi" in reason else "#8B5CF6"
                st.markdown(f"""
                <span style='background: {reason_color}20; color: {reason_color}; 
                padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; 
                font-weight: 600;'>{reason}</span>
                """, unsafe_allow_html=True)
                
                # Show location info
                start_loc = trips_data[t_id].get('start_location', 'N/A')
                end_loc = trips_data[t_id].get('end_location', '')
                if end_loc and end_loc != start_loc:
                    st.caption(f"📍 {start_loc} → {end_loc}")
                else:
                    st.caption(f"📍 {start_loc}")
                
                if invoice_data.get(t_id):
                    amount = invoice_data[t_id]['paid_amount']
                    st.markdown(f"<h4 style='color: #10B981; margin: 0.5rem 0 0 0;'>{format_currency(amount)}</h4>", 
                               unsafe_allow_html=True)
            
            with col2:
                # FIXED: Use unique key for each selectbox
                selected = st.selectbox(
                    "Haydovchi tanlang",
                    options=options,
                    index=default_idx,
                    key=f"driver_select_{t_id}_{idx}",
                    help="Yukni biriktirish uchun haydovchini tanlang"
                )
            
            with col3:
                # FIXED: Button functionality
                if st.button("✅ Assign", key=f"assign_btn_{t_id}_{idx}", use_container_width=True, type="primary"):
                    # Update the driver assignment
                    st.session_state['trips_data'][t_id]['drivers'] = [selected]
                    st.toast(f"✅ {t_id} → {selected}", icon="💾")
                    # Force rerun to update the UI
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

def render_driver_report(df):
    """Render enhanced driver report section with new column order"""
    st.markdown("### 📋 Batafsil Hisobot - Haydovchilar")
    
    all_drivers = sorted([d for d in df['Driver'].unique() if d != "NOMA'LUM (UNKNOWN)"])
    if "NOMA'LUM (UNKNOWN)" in df['Driver'].unique():
        all_drivers.append("NOMA'LUM (UNKNOWN)")
    
    if not all_drivers:
        st.info("Hali haydovchilar ma'lumotlari mavjud emas")
        return
    
    selected_driver = st.selectbox(
        "🔍 Haydovchini tanlang",
        options=all_drivers,
        help="Batafsil ma'lumot olish uchun haydovchini tanlang"
    )
    
    if selected_driver:
        df_driver = df[df['Driver'] == selected_driver].copy()
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        d_paid = df_driver['Tolangan'].sum()
        d_pending = df_driver[df_driver['Status'] == 'Unpaid']['Kutilgan'].sum()
        d_total_trips = len(df_driver)
        d_paid_trips = len(df_driver[df_driver['Tolangan'] > 0])
        
        with col1:
            st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: #94A3B8; margin: 0; font-size: 0.875rem; text-transform: uppercase;'>Jami To'landi</p>
                <h2 style='color: #10B981; margin: 0.5rem 0;'>{format_currency(d_paid)}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: #94A3B8; margin: 0; font-size: 0.875rem; text-transform: uppercase;'>Kutilmoqda</p>
                <h2 style='color: #EF4444; margin: 0.5rem 0;'>{format_currency(d_pending)}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: #94A3B8; margin: 0; font-size: 0.875rem; text-transform: uppercase;'>Jami Yuklar</p>
                <h2 style='color: #F8FAFC; margin: 0.5rem 0;'>{d_total_trips}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            completion_rate = (d_paid_trips / d_total_trips * 100) if d_total_trips > 0 else 0
            st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: #94A3B8; margin: 0; font-size: 0.875rem; text-transform: uppercase;'>To'lov %</p>
                <h2 style='color: #8B5CF6; margin: 0.5rem 0;'>{completion_rate:.0f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Format numeric columns for display
        df_display = df_driver.copy()
        df_display['Kutilgan'] = df_display['Kutilgan'].apply(format_currency)
        df_display['Tolangan'] = df_display['Tolangan'].apply(format_currency)
        df_display['Farq'] = df_display['Farq'].apply(format_currency)
        
        # FIXED: New column order as requested
        st.dataframe(
            df_display,
            column_order=(
                "ID", 
                "Start Location", 
                "Start Time", 
                "End Location", 
                "End Time", 
                "Kutilgan", 
                "Tolangan", 
                "Farq", 
                "Yuklar (Trips)", 
                "Yuklar (Inv)"
            ),
            hide_index=True,
            use_container_width=True,
            height=400,
            column_config={
                "ID": st.column_config.TextColumn("ID", width="small"),
                "Start Location": st.column_config.TextColumn("Start Location", width="medium"),
                "Start Time": st.column_config.TextColumn("Start Time", width="medium"),
                "End Location": st.column_config.TextColumn("End Location", width="medium"),
                "End Time": st.column_config.TextColumn("End Time", width="medium"),
                "Kutilgan": st.column_config.TextColumn("Kutilgan", width="small"),
                "Tolangan": st.column_config.TextColumn("To'langan", width="small"),
                "Farq": st.column_config.TextColumn("Farq", width="small"),
            }
        )
        
        with st.expander("ℹ️ Statuslar Ma'nosi"):
            st.markdown("""
            <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;'>
                <div>
                    <strong style='color: #10B981;'>PAID</strong>
                    <p style='margin: 0.5rem 0 0 0; color: #CBD5E0; font-size: 0.875rem;'>Muvaffaqiyatli to'langan yuklar</p>
                </div>
                <div>
                    <strong style='color: #EF4444;'>UNPAID</strong>
                    <p style='margin: 0.5rem 0 0 0; color: #CBD5E0; font-size: 0.875rem;'>Hali to'lanmagan yuklar</p>
                </div>
                <div>
                    <strong style='color: #F59E0B;'>CANCELED (PAID)</strong>
                    <p style='margin: 0.5rem 0 0 0; color: #CBD5E0; font-size: 0.875rem;'>Bekor qilingan, lekin to'langan (TONU)</p>
                </div>
                <div>
                    <strong style='color: #6B7280;'>CANCELED (NO PAY)</strong>
                    <p style='margin: 0.5rem 0 0 0; color: #CBD5E0; font-size: 0.875rem;'>Bekor qilingan, to'lanmagan</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def generate_txt_report(df):
    """Generate formatted text report with new format"""
    lines = []
    lines.append("="*160)
    lines.append(f"PRO DRIVER PAYROLL REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("="*160)
    lines.append("")
    
    for driver in sorted(df['Driver'].unique()):
        d_df = df[df['Driver'] == driver]
        paid_sum = d_df['Tolangan'].sum()
        pending_sum = d_df[d_df['Status'] == 'Unpaid']['Kutilgan'].sum()
        
        lines.append(f"\n{'='*160}")
        lines.append(f"👤 HAYDOVCHI: {driver}")
        lines.append(f"   💰 Jami To'landi: {format_currency(paid_sum)}")
        lines.append(f"   ⏳ Kutilmoqda: {format_currency(pending_sum)}")
        lines.append(f"{'='*160}")
        
        # Header with new column order
        lines.append(f"{'ID':<16} {'Start Location':<30} {'Start Time':<25} {'End Location':<30} {'End Time':<25} {'Kutilgan':<12} {'To\'langan':<12} {'Farq':<10}")
        lines.append("-" * 160)
        
        for _, row in d_df.iterrows():
            start_loc = (row['Start Location'][:27] + '...') if len(row['Start Location']) > 30 else row['Start Location']
            end_loc = (row['End Location'][:27] + '...') if len(row['End Location']) > 30 else row['End Location']
            start_time = (row['Start Time'][:22] + '...') if len(row['Start Time']) > 25 else row['Start Time']
            end_time = (row['End Time'][:22] + '...') if len(row['End Time']) > 25 else row['End Time']
            
            lines.append(
                f"{row['ID']:<16} {start_loc:<30} {start_time:<25} {end_loc:<30} {end_time:<25} "
                f"{format_currency(row['Kutilgan']):<12} {format_currency(row['Tolangan']):<12} {format_currency(row['Farq']):<10}"
            )
        
        lines.append("")
    
    lines.append("\n" + "="*160)
    lines.append(f"UMUMIY JAMI TO'LANGAN: {format_currency(df['Tolangan'].sum())}")
    lines.append(f"UMUMIY KUTILMOQDA: {format_currency(df[df['Status'] == 'Unpaid']['Kutilgan'].sum())}")
    lines.append("="*160)
    
    return "\n".join(lines)

def generate_excel_report(df):
    """NEW: Generate Excel report with separate sheets for each driver"""
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4472C4',
            'font_color': 'white',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        
        currency_format = workbook.add_format({
            'num_format': '0.00',  # Changed from '#,##0.00' to '0.00'
            'border': 1
        })
        
        text_format = workbook.add_format({
            'border': 1,
            'align': 'left'
        })
        
        # Summary sheet
        summary_data = []
        for driver in sorted(df['Driver'].unique()):
            d_df = df[df['Driver'] == driver]
            paid_sum = d_df['Tolangan'].sum()
            pending_sum = d_df[d_df['Status'] == 'Unpaid']['Kutilgan'].sum()
            total_trips = len(d_df)
            
            summary_data.append({
                'Driver': driver,
                'Total Paid': paid_sum,
                'Total Pending': pending_sum,
                'Total Trips': total_trips
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False, startrow=1)
        
        summary_sheet = writer.sheets['Summary']
        summary_sheet.write(0, 0, 'PAYROLL SUMMARY REPORT', workbook.add_format({'bold': True, 'font_size': 14}))
        
        for col_num, value in enumerate(summary_df.columns.values):
            summary_sheet.write(1, col_num, value, header_format)
        
        # Apply currency format to numeric columns in summary
        for row_num in range(len(summary_df)):
            summary_sheet.write(row_num + 2, 1, summary_df.iloc[row_num]['Total Paid'], currency_format)
            summary_sheet.write(row_num + 2, 2, summary_df.iloc[row_num]['Total Pending'], currency_format)
        
        summary_sheet.set_column('A:A', 25)
        summary_sheet.set_column('B:C', 15)
        summary_sheet.set_column('D:D', 12)
        
        # Individual driver sheets
        for driver in sorted(df['Driver'].unique()):
            d_df = df[df['Driver'] == driver].copy()
            
            # Clean sheet name (Excel has restrictions)
            sheet_name = driver.replace('/', '-')[:31]  # Max 31 chars
            
            d_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=2)
            
            worksheet = writer.sheets[sheet_name]
            
            # Write title
            worksheet.write(0, 0, f'Driver: {driver}', workbook.add_format({'bold': True, 'font_size': 14}))
            
            # Write headers
            for col_num, value in enumerate(d_df.columns.values):
                worksheet.write(2, col_num, value, header_format)
            
            # Apply formats to data rows
            for row_num in range(len(d_df)):
                worksheet.write(row_num + 3, 0, d_df.iloc[row_num]['ID'], text_format)
                worksheet.write(row_num + 3, 1, d_df.iloc[row_num]['Start Location'], text_format)
                worksheet.write(row_num + 3, 2, d_df.iloc[row_num]['Start Time'], text_format)
                worksheet.write(row_num + 3, 3, d_df.iloc[row_num]['End Location'], text_format)
                worksheet.write(row_num + 3, 4, d_df.iloc[row_num]['End Time'], text_format)
                worksheet.write(row_num + 3, 5, d_df.iloc[row_num]['Kutilgan'], currency_format)
                worksheet.write(row_num + 3, 6, d_df.iloc[row_num]['Tolangan'], currency_format)
                worksheet.write(row_num + 3, 7, d_df.iloc[row_num]['Farq'], currency_format)
                worksheet.write(row_num + 3, 8, d_df.iloc[row_num]['Yuklar (Trips)'], text_format)
                worksheet.write(row_num + 3, 9, d_df.iloc[row_num]['Yuklar (Inv)'], text_format)
            
            # Set column widths
            worksheet.set_column('A:A', 16)  # ID
            worksheet.set_column('B:B', 30)  # Start Location
            worksheet.set_column('C:C', 25)  # Start Time
            worksheet.set_column('D:D', 30)  # End Location
            worksheet.set_column('E:E', 25)  # End Time
            worksheet.set_column('F:H', 12)  # Kutilgan, Tolangan, Farq
            worksheet.set_column('I:J', 10)  # Yuklar
    
    output.seek(0)
    return output

# ==============================================================================
# 5. MAIN APPLICATION
# ==============================================================================

def main():
    """Main application logic"""
    
    render_hero_header()
    trips_file, invoice_file = render_sidebar()
    
    if not trips_file or not invoice_file:
        st.markdown("""
        <div style='text-align: center; padding: 100px 20px; color: #6B7280;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>📤</div>
            <h2 style='color: #94A3B8; margin-bottom: 1rem;'>Xush Kelibsiz!</h2>
            <p style='font-size: 1.1rem; color: #64748B;'>
                Ishni boshlash uchun chap paneldan <strong>Trips</strong> va <strong>Invoice</strong> fayllarini yuklang
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Parse files
    if 'trips_data' not in st.session_state:
        with st.spinner("🔄 Ma'lumotlar tahlil qilinmoqda..."):
            trips_content = trips_file.getvalue().decode("utf-8")
            t_parser = TripsParser(trips_content)
            data, multi = t_parser.parse()
            
            st.session_state['trips_data'] = data
            st.session_state['multi_driver_trips'] = multi
            
            st.success("✅ Trips fayli muvaffaqiyatli o'qildi!")
    
    if 'invoice_data' not in st.session_state:
        with st.spinner("💰 Invoice ma'lumotlari o'qilmoqda..."):
            invoice_content = invoice_file.getvalue().decode("utf-8")
            i_parser = InvoiceParser(invoice_content)
            data, total = i_parser.parse()
            
            st.session_state['invoice_data'] = data
            st.session_state['invoice_total'] = total
            
            st.success("✅ Invoice fayli muvaffaqiyatli o'qildi!")
    
    trips_data = st.session_state['trips_data']
    invoice_data = st.session_state['invoice_data']
    multi_drivers = st.session_state['multi_driver_trips']
    
    # Prepare assignment section
    all_known_drivers = set()
    for t in trips_data.values():
        for d in t['drivers']:
            if d != "UNKNOWN":
                all_known_drivers.add(d)
    sorted_drivers_list = sorted(list(all_known_drivers))
    
    ids_to_resolve = []
    extra_pay_items = []
    
    # Collect conflicts
    unique_conflicts = {m['id']: m['drivers'] for m in multi_drivers if len(m['drivers']) > 1}
    for t_id, drvs in unique_conflicts.items():
        ids_to_resolve.append({
            'id': t_id,
            'reason': 'Multi-Driver',
            'options': drvs
        })
    
    # Paid but no driver
    for t_id, t_info in trips_data.items():
        inv_info = invoice_data.get(t_id)
        is_paid = inv_info and inv_info['paid_amount'] > 0
        is_unknown = t_info['drivers'] == ["UNKNOWN"]
        
        if is_paid and is_unknown:
            if t_id not in unique_conflicts:
                ids_to_resolve.append({
                    'id': t_id,
                    'reason': 'Paid (No Driver)',
                    'options': sorted_drivers_list
                })
    
    # Extra payments
    processed_trips_ids = set(trips_data.keys())
    for i_id, i_info in invoice_data.items():
        if i_id not in processed_trips_ids:
            extra_pay_items.append({
                'id': i_id,
                'amount': i_info['paid_amount'],
                'route': i_info.get('route', 'Invoice Route')
            })
    
    if extra_pay_items:
        for item in extra_pay_items:
            if item['id'] not in st.session_state['trips_data']:
                st.session_state['trips_data'][item['id']] = {
                    'drivers': ["UNKNOWN"],
                    'expected_pay': 0.0,
                    'status': "Extra/Dispute",
                    'loads_str': "-",
                    'start_location': item['route'],
                    'end_location': "",
                    'start_time': "Invoice Date",
                    'end_time': ""
                }
                ids_to_resolve.append({
                    'id': item['id'],
                    'reason': 'Qo\'shimcha To\'lov (Extra/Dispute)',
                    'options': sorted_drivers_list
                })
    
    # Render assignment section
    render_assignment_section(ids_to_resolve, st.session_state['trips_data'], invoice_data, sorted_drivers_list)
    
    st.markdown("---")
    
    # Generate report data
    report_rows = []
    
    for t_id, t_info in st.session_state['trips_data'].items():
        drivers = t_info['drivers']
        status = t_info['status']
        expected = t_info['expected_pay']
        loads_str = t_info['loads_str']
        start_location = t_info.get('start_location', '')
        end_location = t_info.get('end_location', '')
        start_time = t_info.get('start_time', '')
        end_time = t_info.get('end_time', '')
        
        inv_info = invoice_data.get(t_id)
        paid = 0.0
        inv_loads = 0
        
        if inv_info:
            paid = inv_info['paid_amount']
            inv_loads = len(inv_info['items'])
        
        final_status = status
        
        if status == "Extra/Dispute":
            final_status = "Extra Pay"
        elif status == "Canceled":
            if paid > 0:
                final_status = "Canceled (Paid)"
            else:
                final_status = "Canceled (No Pay)"
        elif status == "Active":
            if paid == 0:
                final_status = "Unpaid"
            else:
                final_status = "Paid"
        
        diff = paid - expected
        if final_status == "Canceled (No Pay)":
            diff = 0.0
            expected = 0.0
        
        for driver in drivers:
            if driver == "UNKNOWN" and paid == 0 and status == "Canceled":
                continue
            
            report_rows.append({
                "Driver": driver,
                "ID": t_id,
                "Status": final_status,
                "Start Location": start_location,
                "Start Time": start_time,
                "End Location": end_location,
                "End Time": end_time,
                "Kutilgan": expected,  # Keep as number
                "Tolangan": paid,      # Keep as number
                "Farq": diff,          # Keep as number
                "Yuklar (Trips)": loads_str,
                "Yuklar (Inv)": inv_loads
            })
    
    df_main = pd.DataFrame(report_rows)
    
    if not df_main.empty:
        render_metrics_dashboard(df_main, st.session_state['invoice_total'])
        
        st.markdown("---")
        
        render_driver_report(df_main)
        
        st.markdown("---")
        
        # Download section
        st.markdown("### 📥 Download")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 TXT Hisobot", use_container_width=True, type="primary"):
                txt_report = generate_txt_report(df_main)
                st.download_button(
                    label="⬇️ TXT Download",
                    data=txt_report,
                    file_name=f"payroll_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col2:
            # NEW: Excel download with separate sheets
            excel_data = generate_excel_report(df_main)
            st.download_button(
                label="📊 Excel report",
                data=excel_data,
                file_name=f"payroll_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="secondary"
            )
    else:
        st.info("Ma'lumotlar topilmadi")

if __name__ == "__main__":
    main()
