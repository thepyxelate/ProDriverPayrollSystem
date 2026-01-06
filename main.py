import streamlit as st
import re
import csv
import pandas as pd
from io import StringIO
from datetime import datetime
from collections import defaultdict
import time

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
    /* Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0F1116 0%, #1a1d29 100%);
        color: #E2E8F0;
    }
    
    /* Hero Header */
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
    
    /* Metric Cards - Glassmorphism Effect */
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
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #13151C 0%, #1a1d29 100%);
        border-right: 1px solid rgba(71, 85, 105, 0.3);
    }
    
    section[data-testid="stSidebar"] .sidebar-content {
        padding: 1rem;
    }
    
    /* Logo Container */
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* File Uploader Styling */
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
    
    /* Button Styling */
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
    
    /* Expander Styling */
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
    
    /* Select Box Styling */
    div[data-baseweb="select"] > div {
        background: rgba(45, 55, 72, 0.8) !important;
        border: 1px solid rgba(100, 116, 139, 0.3) !important;
        border-radius: 8px !important;
        transition: all 0.3s;
    }
    
    div[data-baseweb="select"]:hover > div {
        border-color: rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Alert Styling */
    .stAlert {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 12px;
        border-left: 4px solid;
    }
    
    /* Info Alert */
    div[data-baseweb="notification"][kind="info"] {
        border-left-color: #3B82F6;
    }
    
    /* Warning Alert */
    div[data-baseweb="notification"][kind="warning"] {
        border-left-color: #F59E0B;
    }
    
    /* Success Alert */
    div[data-baseweb="notification"][kind="success"] {
        border-left-color: #10B981;
    }
    
    /* DataFrame Styling */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(100, 116, 139, 0.3), transparent);
        margin: 2rem 0;
    }
    
    /* Card Container */
    .card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-paid {
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-unpaid {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .status-canceled {
        background: rgba(107, 114, 128, 0.2);
        color: #6B7280;
        border: 1px solid rgba(107, 114, 128, 0.3);
    }
    
    /* Scrollbar Styling */
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
    
    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Toast Notification Style */
    .stToast {
        background: rgba(30, 41, 59, 0.95) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. UTILITY FUNCTIONS & PARSERS
# ==============================================================================

# Regex Patterns
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

def normalize_name(name):
    """Normalize driver names"""
    return name.strip().upper()

def get_status_color(status):
    """Get color for status badge"""
    status_colors = {
        'Paid': '#10B981',
        'Unpaid': '#EF4444',
        'Canceled (Paid)': '#F59E0B',
        'Canceled (No Pay)': '#6B7280',
        'Extra Pay': '#8B5CF6'
    }
    return status_colors.get(status, '#6B7280')

class TripsParser:
    """Enhanced trips file parser with location and time tracking"""
    
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
        start_location = None
        end_location = None
        start_time = None
        end_time = None
        temp_locations = []
        temp_times = []

        def save_block():
            nonlocal current_ids, current_pay, current_drivers, current_loads, is_canceled
            nonlocal start_location, end_location, start_time, end_time, temp_locations, temp_times
            
            if current_ids:
                drvs = current_drivers if current_drivers else ["UNKNOWN"]
                pay = current_pay
                status = "Canceled" if is_canceled else "Active"
                
                if temp_locations:
                    start_location = temp_locations[0]
                    end_location = temp_locations[-1] if len(temp_locations) > 1 else ""
                if temp_times:
                    start_time = temp_times[0]
                    end_time = temp_times[-1] if len(temp_times) > 1 else ""

                route_info = f"{start_location} → {end_location}" if end_location else start_location
                time_info = f"{start_time} - {end_time}" if end_time else start_time

                if len(drvs) > 1 or (drvs == ["UNKNOWN"]):
                    for _id in current_ids:
                        self.multi_driver_trips.append({
                            'id': _id,
                            'drivers': drvs,
                            'status': status,
                            'route': route_info
                        })

                for _id in current_ids:
                    self.trips_data[_id] = {
                        'drivers': drvs,
                        'expected_pay': pay,
                        'status': status,
                        'loads_str': current_loads,
                        'route': route_info,
                        'time': time_info
                    }
            
            current_ids = []
            current_pay = 0.0
            current_drivers = []
            current_loads = "?"
            is_canceled = False
            temp_locations = []
            temp_times = []

        loc_pattern = r"([A-Z0-9]+[\s]+[A-Z\s]+,\s+[A-Z]{2}\s+\d{5})"
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
                l_match = re.search(loc_pattern, line)
                if l_match:
                    temp_locations.append(l_match.group(1))
                
                t_match = re.search(time_pattern, line)
                if t_match:
                    temp_times.append(t_match.group(1))

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
                3. Muammoli yuk larni biriktiring
                4. Hisobotni ko'ring va yuklab oling
                """)
        
        st.markdown("---")
        st.caption("v4.0 Pro | Made with ❤️ by ex UT|member")
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
            value=f"${total_paid:,.2f}",
            delta=f"Avg: ${avg_pay:,.0f}",
            delta_color="off"
        )
    
    with col3:
        st.metric(
            label="📄 Invoice Total",
            value=f"${invoice_total:,.2f}",
            delta=None,
            delta_color="off"
        )
    
    with col4:
        diff = total_paid - invoice_total
        st.metric(
            label="⚖️ Farq",
            value=f"${diff:,.2f}",
            delta="OK" if abs(diff) < 1 else "Check",
            delta_color="normal" if abs(diff) < 1 else "inverse"
        )

def render_assignment_section(ids_to_resolve, trips_data, invoice_data, sorted_drivers_list):
    """Render manual assignment section with improved UX"""
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
        
        progress = st.progress(0)
        total = len(ids_to_resolve)
        
        for idx, item in enumerate(ids_to_resolve):
            progress.progress((idx + 1) / total)
            
            t_id = item['id']
            reason = item['reason']
            options = item['options']
            route = item.get('route', 'N/A')
            
            current_drivers = trips_data[t_id]['drivers']
            default_idx = 0
            
            if len(current_drivers) == 1 and current_drivers[0] in options:
                default_idx = options.index(current_drivers[0])
            
            # Card for each assignment
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"**🆔 ID:** `{t_id}`")
                
                # Reason badge
                reason_color = "#F59E0B" if "Multi" in reason else "#8B5CF6"
                st.markdown(f"""
                <span style='background: {reason_color}20; color: {reason_color}; 
                padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; 
                font-weight: 600;'>{reason}</span>
                """, unsafe_allow_html=True)
                
                st.caption(f"📍 {route}")
                
                if invoice_data.get(t_id):
                    amount = invoice_data[t_id]['paid_amount']
                    st.markdown(f"<h4 style='color: #10B981; margin: 0.5rem 0 0 0;'>${amount:,.2f}</h4>", 
                               unsafe_allow_html=True)
            
            with col2:
                selected = st.selectbox(
                    "Haydovchi tanlang",
                    options=options,
                    index=default_idx,
                    key=f"sel_{t_id}",
                    help="Yukni biriktirish uchun haydovchini tanlang"
                )
            
            with col3:
                if st.button("✅ Biriktirish", key=f"btn_{t_id}", use_container_width=True, type="primary"):
                    trips_data[t_id]['drivers'] = [selected]
                    st.toast(f"✅ {t_id} → {selected}", icon="💾")
                    time.sleep(0.5)
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

def render_driver_report(df):
    """Render enhanced driver report section"""
    st.markdown("### 📋 Batafsil Hisobot - Haydovchilar")
    
    all_drivers = sorted([d for d in df['Driver'].unique() if d != "NOMA'LUM (UNKNOWN)"])
    if "NOMA'LUM (UNKNOWN)" in df['Driver'].unique():
        all_drivers.append("NOMA'LUM (UNKNOWN)")
    
    if not all_drivers:
        st.info("Hali haydovchilar ma'lumotlari mavjud emas")
        return
    
    # Driver selector with search
    selected_driver = st.selectbox(
        "🔍 Haydovchini tanlang",
        options=all_drivers,
        help="Batafsil ma'lumot olish uchun haydovchini tanlang"
    )
    
    if selected_driver:
        df_driver = df[df['Driver'] == selected_driver].copy()
        
        # Driver summary card
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
                <h2 style='color: #10B981; margin: 0.5rem 0;'>${d_paid:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: #94A3B8; margin: 0; font-size: 0.875rem; text-transform: uppercase;'>Kutilmoqda</p>
                <h2 style='color: #EF4444; margin: 0.5rem 0;'>${d_pending:,.2f}</h2>
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
        
        # Data table with improved configuration
        st.dataframe(
            df_driver,
            column_order=("ID", "Status", "Marshrut", "Vaqt", "Kutilgan", "Tolangan", "Farq", "Yuklar (Trips)", "Yuklar (Inv)"),
            hide_index=True,
            use_container_width=True,
            height=400,
            column_config={
                "ID": st.column_config.TextColumn("ID", width="small"),
                "Status": st.column_config.TextColumn("Status", width="medium"),
                "Marshrut": st.column_config.TextColumn("Marshrut", width="large"),
                "Vaqt": st.column_config.TextColumn("Vaqt", width="medium"),
                "Kutilgan": st.column_config.NumberColumn("Kutilgan", format="$%.2f"),
                "Tolangan": st.column_config.NumberColumn("To'langan", format="$%.2f"),
                "Farq": st.column_config.NumberColumn("Farq", format="$%.2f"),
            }
        )
        
        # Status legend
        with st.expander("ℹ️ Statuslar Ma'nosi"):
            st.markdown("""
            <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;'>
                <div>
                    <span class='status-badge status-paid'>PAID</span>
                    <p style='margin: 0.5rem 0 0 0; color: #CBD5E0; font-size: 0.875rem;'>Muvaffaqiyatli to'langan yuklar</p>
                </div>
                <div>
                    <span class='status-badge status-unpaid'>UNPAID</span>
                    <p style='margin: 0.5rem 0 0 0; color: #CBD5E0; font-size: 0.875rem;'>Hali to'lanmagan yuklar</p>
                </div>
                <div>
                    <span class='status-badge status-canceled'>CANCELED (PAID)</span>
                    <p style='margin: 0.5rem 0 0 0; color: #CBD5E0; font-size: 0.875rem;'>Bekor qilingan, lekin to'langan (TONU)</p>
                </div>
                <div>
                    <span class='status-badge status-canceled'>CANCELED (NO PAY)</span>
                    <p style='margin: 0.5rem 0 0 0; color: #CBD5E0; font-size: 0.875rem;'>Bekor qilingan, to'lanmagan</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def generate_txt_report(df):
    """Generate formatted text report"""
    lines = []
    lines.append("="*120)
    lines.append(f"PRO DRIVER PAYROLL REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("="*120)
    lines.append("")
    
    for driver in sorted(df['Driver'].unique()):
        d_df = df[df['Driver'] == driver]
        paid_sum = d_df['Tolangan'].sum()
        pending_sum = d_df[d_df['Status'] == 'Unpaid']['Kutilgan'].sum()
        
        lines.append(f"\n{'='*120}")
        lines.append(f"👤 HAYDOVCHI: {driver}")
        lines.append(f"   💰 Jami To'landi: ${paid_sum:,.2f}")
        lines.append(f"   ⏳ Kutilmoqda: ${pending_sum:,.2f}")
        lines.append(f"{'='*120}")
        
        # Header
        lines.append(f"{'ID':<16} {'Status':<20} {'Marshrut':<30} {'Kutilgan':<12} {'To\'langan':<12} {'Farq':<10}")
        lines.append("-" * 120)
        
        for _, row in d_df.iterrows():
            route_short = (row['Marshrut'][:27] + '...') if len(row['Marshrut']) > 30 else row['Marshrut']
            lines.append(
                f"{row['ID']:<16} {row['Status']:<20} {route_short:<30} "
                f"${row['Kutilgan']:<11,.2f} ${row['Tolangan']:<11,.2f} ${row['Farq']:<9,.2f}"
            )
        
        lines.append("")
    
    lines.append("\n" + "="*120)
    lines.append(f"UMUMIY JAMI TO'LANGAN: ${df['Tolangan'].sum():,.2f}")
    lines.append(f"UMUMIY KUTILMOQDA: ${df[df['Status'] == 'Unpaid']['Kutilgan'].sum():,.2f}")
    lines.append("="*120)
    
    return "\n".join(lines)

# ==============================================================================
# 5. MAIN APPLICATION
# ==============================================================================

def main():
    """Main application logic"""
    
    # Render UI components
    render_hero_header()
    trips_file, invoice_file = render_sidebar()
    
    # Check if files are uploaded
    if not trips_file or not invoice_file:
        st.markdown("""
        <div style='text-align: center; padding: 100px 20px; color: #6B7280;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>📤</div>
            <h2 style='color: #94A3B8; margin-bottom: 1rem;'>Xush Kelibsiz!</h2>
            <p style='font-size: 1.1rem; color: #64748B;'>
                Ishni boshlash uchun chap paneldan <strong>Trips</strong> va <strong>Invoice</strong> fayllarini yuklang
            </p>
            <div style='margin-top: 2rem; padding: 1.5rem; background: rgba(102, 126, 234, 0.1); 
                        border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.2); max-width: 600px; margin: 2rem auto;'>
                <h4 style='color: #818CF8; margin-bottom: 1rem;'>🎯 Xususiyatlar:</h4>
                <ul style='text-align: left; color: #CBD5E0; line-height: 1.8;'>
                    <li>📊 Avtomatik ma'lumotlar tahlili</li>
                    <li>🔄 Ko'p haydovchili yuklar boshqaruvi</li>
                    <li>💰 Real-time to'lovlar nazorati</li>
                    <li>📈 Professional hisobotlar</li>
                    <li>🎨 Zamonaviy va qulay interfeys</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Parse files with progress indication
    if 'trips_data' not in st.session_state:
        with st.spinner("🔄 Ma'lumotlar tahlil qilinmoqda..."):
            progress_bar = st.progress(0)
            progress_bar.progress(30)
            
            trips_content = trips_file.getvalue().decode("utf-8")
            t_parser = TripsParser(trips_content)
            data, multi = t_parser.parse()
            
            progress_bar.progress(60)
            
            st.session_state['trips_data'] = data
            st.session_state['multi_driver_trips'] = multi
            
            progress_bar.progress(100)
            time.sleep(0.3)
            progress_bar.empty()
            
            st.success("✅ Trips fayli muvaffaqiyatli o'qildi!")
    
    if 'invoice_data' not in st.session_state:
        with st.spinner("💰 Invoice ma'lumotlari o'qilmoqda..."):
            progress_bar = st.progress(0)
            progress_bar.progress(30)
            
            invoice_content = invoice_file.getvalue().decode("utf-8")
            i_parser = InvoiceParser(invoice_content)
            data, total = i_parser.parse()
            
            progress_bar.progress(60)
            
            st.session_state['invoice_data'] = data
            st.session_state['invoice_total'] = total
            
            progress_bar.progress(100)
            time.sleep(0.3)
            progress_bar.empty()
            
            st.success("✅ Invoice fayli muvaffaqiyatli o'qildi!")
    
    # Get data from session state
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
        route = trips_data[t_id].get('route', 'Noma\'lum marshrut')
        ids_to_resolve.append({
            'id': t_id,
            'reason': 'Multi-Driver',
            'options': drvs,
            'route': route
        })
    
    # Paid but no driver
    for t_id, t_info in trips_data.items():
        inv_info = invoice_data.get(t_id)
        is_paid = inv_info and inv_info['paid_amount'] > 0
        is_unknown = t_info['drivers'] == ["UNKNOWN"]
        
        if is_paid and is_unknown:
            if t_id not in unique_conflicts:
                route = t_info.get('route', 'Noma\'lum marshrut')
                ids_to_resolve.append({
                    'id': t_id,
                    'reason': 'Paid (No Driver)',
                    'options': sorted_drivers_list,
                    'route': route
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
                    'route': item['route'],
                    'time': "Invoice Date"
                }
                ids_to_resolve.append({
                    'id': item['id'],
                    'reason': 'Qo\'shimcha To\'lov (Extra/Dispute)',
                    'options': sorted_drivers_list,
                    'route': item['route']
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
        route = t_info.get('route', '')
        time_info = t_info.get('time', '')
        
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
                "Marshrut": route,
                "Vaqt": time_info,
                "Kutilgan": expected,
                "Tolangan": paid,
                "Farq": diff,
                "Yuklar (Trips)": loads_str,
                "Yuklar (Inv)": inv_loads
            })
    
    df_main = pd.DataFrame(report_rows)
    
    if not df_main.empty:
        # Render metrics dashboard
        render_metrics_dashboard(df_main, st.session_state['invoice_total'])
        
        st.markdown("---")
        
        # Render driver report
        render_driver_report(df_main)
        
        st.markdown("---")
        
        # Download section
        st.markdown("### 📥 Hisobotni Yuklab Olish")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 TXT Hisobot", use_container_width=True, type="primary"):
                txt_report = generate_txt_report(df_main)
                st.download_button(
                    label="⬇️ TXT ni Yuklab Olish",
                    data=txt_report,
                    file_name=f"payroll_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col2:
            if st.button("📊 Excel Hisobot", use_container_width=True, type="secondary"):
                # Excel export would go here
                st.info("Excel export funksiyasi tez orada qo'shiladi!")
    else:
        st.info("Ma'lumotlar topilmadi")

# ==============================================================================
# 6. RUN APPLICATION
# ==============================================================================

if __name__ == "__main__":
    main()