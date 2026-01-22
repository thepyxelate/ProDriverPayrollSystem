import streamlit as st
import re
import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO, BytesIO
from datetime import datetime
from collections import defaultdict

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Pro Driver Payroll System",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. ADVANCED GLASSMORPHISM STYLING (PREMIUM EFFECT)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    * { font-family: 'Outfit', sans-serif; }
    
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #141E30);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #ffffff;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1.5rem;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Mini Stats Card */
    .mini-stat {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .mini-stat:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(0, 210, 255, 0.5);
        transform: scale(1.02);
    }
    
    .mini-stat-label {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .mini-stat-value {
        color: #00d2ff;
        font-size: 1.8rem;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
    }
    
    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    div[data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.9rem;
    }
    
    div[data-testid="stMetricValue"] {
        color: #fff !important;
        font-size: 1.8rem;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    
    /* Hero Title */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    /* Custom Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0, 210, 255, 0.5);
    }
    
    /* DataFrame Styling */
    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 15px;
        padding: 10px;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255, 255, 255, 0.02);
        padding: 10px;
        border-radius: 20px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 15px;
        color: #aaa;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.1);
        color: #fff;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Progress Bar */
    .custom-progress {
        background: rgba(255, 255, 255, 0.1);
        height: 8px;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .custom-progress-fill {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
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
    """Format currency as requested: 9120,18"""
    try:
        if pd.isna(value):
            return "0,00"
        s = f"{value:.2f}"
        return s.replace('.', ',')
    except:
        return "0,00"

def normalize_name(name):
    return name.strip().upper()

class TripsParser:
    def __init__(self, file_content):
        self.content = file_content
        self.trips_data = {}

    def parse(self):
        lines = self.content.splitlines()
        
        current_ids = []
        current_pay = 0.0
        current_drivers = []
        current_loads = "?"
        is_rejected = False
        is_canceled = False
        temp_locations = []
        temp_times = []

        def save_block():
            nonlocal current_ids, current_pay, current_drivers, current_loads, is_canceled, is_rejected
            nonlocal temp_locations, temp_times
            
            if current_ids:
                drvs = current_drivers if current_drivers else ["UNKNOWN"]
                pay = current_pay

                if is_rejected:
                    status = "Rejected"
                elif is_canceled:
                    status = "Canceled"
                else:
                    status = "Active"

                # status = "Canceled" if is_canceled else "Active"
                
                
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
            is_rejected = False
            temp_locations = []
            temp_times = []

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
# 4. ENHANCED VISUALIZATION COMPONENTS
# ==============================================================================

def render_advanced_charts(df):
    """Render beautiful and interactive analytics"""
    
    # --- CHART 1: TOP EARNERS (Only Paid Amount) ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💰 Top 15 Haydovchilar - Jami Daromad")
    
    driver_earnings = df.groupby('Driver')['Tolangan'].sum().reset_index()
    driver_earnings = driver_earnings[driver_earnings['Driver'] != "UNKNOWN"]
    driver_earnings = driver_earnings.sort_values('Tolangan', ascending=False).head(15)
    
    fig_earnings = px.bar(
        driver_earnings,
        x='Tolangan',
        y='Driver',
        orientation='h',
        text='Tolangan',
        color='Tolangan',
        color_continuous_scale=['#3a7bd5', '#00d2ff', '#00fff2']
    )
    
    fig_earnings.update_traces(
        texttemplate='%{text:,.2f}',
        textposition='outside'
    )
    
    fig_earnings.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(autorange="reversed", title=""),
        xaxis=dict(title="To'langan Summa", showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        coloraxis_showscale=False,
        font=dict(size=12)
    )
    st.plotly_chart(fig_earnings, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- CHART 2 & 3: TWO COLUMN LAYOUT ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 O'rtacha Trip Daromadi")
        
        # Average earnings per trip by driver (top 10)
        driver_trip_avg = df.groupby('Driver').agg(
            avg_earning=('Tolangan', 'mean'),
            trip_count=('ID', 'count')
        ).reset_index()
        driver_trip_avg = driver_trip_avg[driver_trip_avg['Driver'] != "UNKNOWN"]
        driver_trip_avg = driver_trip_avg.sort_values('avg_earning', ascending=False).head(10)
        
        fig_avg = go.Figure()
        fig_avg.add_trace(go.Bar(
            x=driver_trip_avg['Driver'],
            y=driver_trip_avg['avg_earning'],
            marker_color='#ff9068',
            text=driver_trip_avg['avg_earning'].round(2),
            texttemplate='%{text}',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Avg: %{y:,.2f}<extra></extra>'
        ))
        
        fig_avg.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(title="", tickangle=-45),
            yaxis=dict(title="O'rtacha Daromad", showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False
        )
        st.plotly_chart(fig_avg, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🏆 Eng Ko'p Tripli Haydovchilar")
        
        trip_counts = df['Driver'].value_counts().reset_index().head(10)
        trip_counts.columns = ['Driver', 'Trip Count']
        trip_counts = trip_counts[trip_counts['Driver'] != "UNKNOWN"]
        
        fig_trips = px.bar(
            trip_counts,
            x='Trip Count',
            y='Driver',
            orientation='h',
            text='Trip Count',
            color='Trip Count',
            color_continuous_scale=['#667eea', '#764ba2', '#f093fb']
        )
        
        fig_trips.update_traces(
            texttemplate='%{text}',
            textposition='outside'
        )
        
        fig_trips.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(autorange="reversed", title=""),
            xaxis=dict(title="Trip Soni", showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_trips, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- CHART 4: TOP ROUTES (Most Profitable) ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🗺️ Eng Daromadli Yo'nalishlar (Top 10)")
    
    # Create route column by combining start and end
    df_routes = df.copy()
    df_routes['Route'] = df_routes['Start Location'].str[:15] + " → " + df_routes['End Location'].str[:15]
    route_earnings = df_routes.groupby('Route')['Tolangan'].sum().reset_index()
    route_earnings = route_earnings.sort_values('Tolangan', ascending=False).head(10)
    
    fig_routes = px.bar(
        route_earnings,
        x='Route',
        y='Tolangan',
        text='Tolangan',
        color='Tolangan',
        color_continuous_scale=['#fc4a1a', '#f7b733']
    )
    
    fig_routes.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='outside'
    )
    
    fig_routes.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(title="", tickangle=-45),
        yaxis=dict(title="Daromad", showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_routes, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_driver_statistics(df, driver_name):
    """Render detailed statistics for selected driver"""
    
    if driver_name == "All":
        return
    
    driver_df = df[df['Driver'] == driver_name]
    
    if driver_df.empty:
        st.warning("Bu haydovchi uchun ma'lumot topilmadi")
        return
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0 1rem 0;">
        <h2 style="background: linear-gradient(to right, #00d2ff, #fff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            👤 {driver_name} - Batafsil Statistika
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # MINI STATS ROW
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_earned = driver_df['Tolangan'].sum()
    total_trips = len(driver_df)
    avg_per_trip = total_earned / total_trips if total_trips > 0 else 0
    paid_trips = len(driver_df[driver_df['Tolangan'] > 0])
    unpaid_trips = len(driver_df[driver_df['Status'] == 'Unpaid'])
    
    
    with col1:
        st.markdown(f"""
        <div class="mini-stat">
            <div class="mini-stat-label">Jami Daromad</div>
            <div class="mini-stat-value">{format_currency(total_earned)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="mini-stat">
            <div class="mini-stat-label">Jami Triplar</div>
            <div class="mini-stat-value">{total_trips}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="mini-stat">
            <div class="mini-stat-label">O'rtacha/Trip</div>
            <div class="mini-stat-value">{format_currency(avg_per_trip)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="mini-stat">
            <div class="mini-stat-label">To'langan</div>
            <div class="mini-stat-value" style="color: #10B981;">{paid_trips}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="mini-stat">
            <div class="mini-stat-label">Kutilmoqda</div>
            <div class="mini-stat-value" style="color: #EF4444;">{unpaid_trips}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # DRIVER SPECIFIC CHARTS
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📈 Status Bo'yicha Taqsimot")
        
        status_dist = driver_df['Status'].value_counts().reset_index()
        status_dist.columns = ['Status', 'Count']
        
        fig_status = px.pie(
            status_dist,
            values='Count',
            names='Status',
            hole=0.5,
            color_discrete_sequence=['#00d2ff', '#ff9068', '#10B981', '#EF4444']
        )
        
        fig_status.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
            legend=dict(orientation="h", y=-0.1)
        )
        st.plotly_chart(fig_status, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_b:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 💵 Daromad Taqsimoti")
        
        # Histogram of earnings
        fig_hist = px.histogram(
            driver_df,
            x='Tolangan',
            nbins=20,
            color_discrete_sequence=['#667eea']
        )
        
        fig_hist.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(title="Daromad", showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title="Trip Soni", showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # PROGRESS BAR - COMPLETION RATE
    completion_rate = (paid_trips / total_trips * 100) if total_trips > 0 else 0
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 🎯 To'lovlar Bajarilish Darajasi")
    st.markdown(f"""
    <div class="custom-progress">
        <div class="custom-progress-fill" style="width: {completion_rate}%;"></div>
    </div>
    <p style="text-align: center; color: #aaa; margin-top: 10px;">{completion_rate:.1f}% ({paid_trips} / {total_trips})</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 5. UI COMPONENTS
# ==============================================================================

def render_hero_header():
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 class="hero-title">🚚 Pro Driver Payroll</h1>
        <p style="color: #a0a0a0; font-size: 1.1rem;">Professional Accounting & Analytics System</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="background: rgba(255,255,255,0.1); width: 80px; height: 80px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(10px);">
                <span style="font-size: 30px;">5️⃣</span>
            </div>
            <h3 style="margin-top: 1rem; color: #fff;">Payroll Version 5</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📂 Data Source")
        trips_file = st.file_uploader("📋 Trips File (.txt)", type=['txt'], key="trips")
        invoice_file = st.file_uploader("💰 Invoice File (.txt)", type=['txt'], key="inv")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Yangilash"):
            st.session_state.clear()
            st.rerun()
            
        return trips_file, invoice_file

def render_assignment_section(ids_to_resolve, trips_data, invoice_data, sorted_drivers_list):
    if not ids_to_resolve:
        return
    
    st.markdown(f"""
    <div style="background: rgba(255, 153, 0, 0.1); border-left: 4px solid #ff9900; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
        <h4 style="margin: 0; color: #ff9900;">⚠️ Diqqat Talab: {len(ids_to_resolve)} ta yuk</h4>
        <p style="margin: 5px 0 0 0; color: #ccc; font-size: 0.9rem;">Iltimos, ushbu yuklarni haydovchilarga to'g'ri biriktiring.</p>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, item in enumerate(ids_to_resolve):
        col = cols[i % 3]
        with col:
            with st.container():
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 10px;">
                    <strong style="color: #00d2ff;">{item['id']}</strong><br>
                    <span style="font-size: 0.8rem; color: #888;">{item['reason']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                selected = st.selectbox(
                    "Driver", 
                    options=item['options'], 
                    key=f"sel_{item['id']}", 
                    label_visibility="collapsed"
                )
                
                if st.button("Assign", key=f"btn_{item['id']}", use_container_width=True):
                    st.session_state['trips_data'][item['id']]['drivers'] = [selected]
                    st.rerun()

def generate_txt_report(df):
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
        
        lines.append(f"{'ID':<16} {'Start Location':<30} {'Start Time':<25} {'End Location':<30} {'End Time':<25} {'Kutilgan':<12} {'To\'langan':<12} {'Farq':<10}")
        lines.append("-" * 160)
        
        for _, row in d_df.iterrows():
            start_loc = (row['Start Location'][:27] + '...') if len(row['Start Location']) > 30 else row['Start Location']
            end_loc = (row['End Location'][:27] + '...') if len(row['End Location']) > 30 else row['End Location']
            start_time = (row['Start Time'][:22] + '...') if len(row['Start Time']) > 25 else row['Start Time']
            end_time = (row['End Time'][:22] + '...') if len(row['End Time']) > 25 else row['End Time']
            
            kut = format_currency(row['Kutilgan']) if isinstance(row['Kutilgan'], (int, float)) else str(row['Kutilgan'])
            tol = format_currency(row['Tolangan']) if isinstance(row['Tolangan'], (int, float)) else str(row['Tolangan'])
            far = format_currency(row['Farq']) if isinstance(row['Farq'], (int, float)) else str(row['Farq'])
            
            lines.append(
                f"{row['ID']:<16} {start_loc:<30} {start_time:<25} {end_loc:<30} {end_time:<25} "
                f"{kut:<12} {tol:<12} {far:<10}"
            )
        lines.append("")
    
    lines.append("\n" + "="*160)
    lines.append(f"UMUMIY JAMI TO'LANGAN: {format_currency(df['Tolangan'].sum())}")
    lines.append(f"UMUMIY KUTILMOQDA: {format_currency(df[df['Status'] == 'Unpaid']['Kutilgan'].sum())}")
    lines.append("="*160)
    return "\n".join(lines)

def generate_excel_report(df):
    output = BytesIO()
    try:
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            header_format = workbook.add_format({'bold': True, 'bg_color': '#4472C4', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
            currency_format = workbook.add_format({'num_format': '0.00', 'border': 1})
            text_format = workbook.add_format({'border': 1, 'align': 'left'})
            total_format = workbook.add_format({'bold': True, 'font_size': 14 ,'bg_color': "#4444C4", 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
            totalgross_format = workbook.add_format({'bold': True,  'align': 'left'})
            
            summary_data = []
            for driver in sorted(df['Driver'].unique()):
                d_df = df[df['Driver'] == driver]
                summary_data.append({
                    'Driver': driver,
                    'Total Paid': d_df['Tolangan'].sum(),
                    'Total Pending': d_df[d_df['Status'] == 'Unpaid']['Kutilgan'].sum(),
                    'Total Trips': len(d_df)
                })
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False, startrow=1)
            
            ws = writer.sheets['Summary']
            for i, col in enumerate(summary_df.columns):
                ws.write(1, i, col, header_format)
            ws.set_column('A:A', 25)
            ws.set_column('B:C', 15,)
            
            for driver in sorted(df['Driver'].unique()):
                d_df = df[df['Driver'] == driver].copy()
                export_df = d_df[['ID', 'Start Location', 'Start Time', 'End Location', 'End Time', 'Kutilgan', 'Tolangan', 'Farq', ]]
                sheet_name = driver.replace('/', '-')[:31]
                ws = workbook.add_worksheet(sheet_name)

                # 1. Sarlavha
                ws.write(1, 0, f'Driver: {driver}', workbook.add_format({'bold': True, 'font_size': 14}))
                
                # 2. Jadval sarlavhalarini yozish
                headers = export_df.columns.values
                for i, h in enumerate(headers):
                    ws.write(2, i, h, header_format)
                #(Row by Row)
                for i, row in enumerate(export_df.itertuples(index=False)):
                    ws.write(i+3, 0, row[0], text_format)
                    ws.write(i+3, 1, row[1], text_format)
                    ws.write(i+3, 2, row[2], text_format)
                    ws.write(i+3, 3, row[3], text_format)
                    ws.write(i+3, 4, row[4], text_format)
                    ws.write(i+3, 5, row[5], currency_format)
                    ws.write(i+3, 6, row[6], currency_format)
                    ws.write(i+3, 7, row[7], currency_format)
                # YANGI LOGIKA
                last_row = len(d_df) + 3 # Ma'lumotlardan keyingi qatorni aniqlaymiz
    
                # Jami summani hisoblaymiz
                total_tolangan = d_df['Tolangan'].sum()

                # A dan E gacha bo'lgan kataklarni birlashtirib "TOTAL GROSS:" deb yozamiz
                ws.merge_range(last_row, 4, last_row, 5, 'TOTAL GROSS:', totalgross_format)

                # Hisoblangan summalarni tegishli ustunlarga (F, G, H) yozamiz
                ws.write(last_row, 6, total_tolangan, total_format) # G ustuni

                

                # --- YANGI LOGIKA TUGADI ---
                
                # Set column widths
                ws.set_column('A:A', 16)
                ws.set_column('B:B', 30)
                ws.set_column('C:C', 25)
                ws.set_column('D:D', 30)
                ws.set_column('E:E', 25)
                ws.set_column('F:H', 15)
        output.seek(0)
        return output
    except Exception as e:
        st.error(f"Excel xatosi: {e}") # Bu xatoni ekranga chiqaradi
        return None

# ==============================================================================
# 6. MAIN APPLICATION
# ==============================================================================

def main():
    render_hero_header()
    trips_file, invoice_file = render_sidebar()
    
    if not trips_file or not invoice_file:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 4rem 2rem;">
            <div style="font-size: 5rem; margin-bottom: 1rem;">🚀</div>
            <h2 style="background: linear-gradient(to right, #fff, #aaa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Tizimga Xush Kelibsiz!</h2>
            <p style="color: #bbb; max-width: 600px; margin: 0 auto;">
                Boshlash uchun chap menyudan Trips va Invoice fayllarini yuklang. Tizim avtomatik ravishda tahlil qiladi va ajoyib hisobotlarni taqdim etadi.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Process Files
    if 'trips_data' not in st.session_state:
        with st.spinner("🔄 AI Tahlil qilmoqda..."):
            t_parser = TripsParser(trips_file.getvalue().decode("utf-8"))
            st.session_state['trips_data'] = t_parser.parse()
            
    if 'invoice_data' not in st.session_state:
        with st.spinner("💰 Moliyaviy hisoblanmoqda..."):
            i_parser = InvoiceParser(invoice_file.getvalue().decode("utf-8"))
            data, total = i_parser.parse()
            st.session_state['invoice_data'] = data
            st.session_state['invoice_total'] = total
    
    # Data Processing for Display
    trips_data = st.session_state['trips_data']
    invoice_data = st.session_state['invoice_data']
    
    # Conflict Resolution Logic
    all_known_drivers = set()
    for t in trips_data.values():
        for d in t['drivers']:
            if d != "UNKNOWN": all_known_drivers.add(d)
    sorted_drivers = sorted(list(all_known_drivers))
    
    ids_to_resolve = []
    
    # Multi-driver
    for t_id, t_info in trips_data.items():
        if len(t_info['drivers']) > 1:
            ids_to_resolve.append({'id': t_id, 'reason': 'Multi-Driver', 'options': t_info['drivers']})
            
    # Paid No Driver
    for t_id, t_info in trips_data.items():
        inv = invoice_data.get(t_id)
        if inv and inv['paid_amount'] > 0 and t_info['drivers'] == ["UNKNOWN"]:
            if not any(x['id'] == t_id for x in ids_to_resolve):
                ids_to_resolve.append({'id': t_id, 'reason': 'Paid (No Driver)', 'options': sorted_drivers})

    # Extra Pay
    processed = set(trips_data.keys())
    for i_id, i_info in invoice_data.items():
        if i_id not in processed:
            if i_id not in st.session_state['trips_data']:
                st.session_state['trips_data'][i_id] = {
                    'drivers': ["UNKNOWN"], 'expected_pay': 0.0, 'status': "Extra/Dispute",
                    'loads_str': "-", 'start_location': i_info.get('route', ''),
                    'end_location': "", 'start_time': "", 'end_time': ""
                }
                ids_to_resolve.append({'id': i_id, 'reason': 'Extra Pay', 'options': sorted_drivers})

    # Render Conflict Resolver
    render_assignment_section(ids_to_resolve, st.session_state['trips_data'], invoice_data, sorted_drivers)
    
    # Prepare Main DataFrame
    rows = []
    for t_id, t_info in st.session_state['trips_data'].items():
        drivers = t_info['drivers']
        inv = invoice_data.get(t_id)
        paid = inv['paid_amount'] if inv else 0.0
        
        status = t_info['status']
        if status == "Extra/Dispute": final_status = "Extra Pay"
        elif status == "Canceled": final_status = "Canceled (Paid)" if paid > 0 else "Canceled (No Pay)"
        else: final_status = "Paid" if paid > 0 else "Unpaid"
        
        expected = t_info['expected_pay']
        diff = paid - expected if final_status != "Canceled (No Pay)" else 0.0
        if final_status == "Canceled (No Pay)": expected = 0.0
        
        for d in drivers:
            if d == "UNKNOWN" and paid == 0 and status == "Canceled": continue
            rows.append({
                "Driver": d, "ID": t_id, "Status": final_status,
                "Start Location": t_info.get('start_location', ''), "Start Time": t_info.get('start_time', ''),
                "End Location": t_info.get('end_location', ''), "End Time": t_info.get('end_time', ''),
                "Kutilgan": expected, "Tolangan": paid, "Farq": diff,
                "Yuklar (Trips)": t_info['loads_str'], "Yuklar (Inv)": len(inv['items']) if inv else 0
            })
            
    df = pd.DataFrame(rows)
    
    if not df.empty:
        # TABS LAYOUT
        tab_analytics, tab_data = st.tabs(["📊 Smart Analytics", "📋 Data & Export"])
        
        with tab_analytics:
            # Top Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            paid_total = df['Tolangan'].sum()
            inv_total = st.session_state['invoice_total']
            
            with col1: st.metric("Jami To'langan", format_currency(paid_total))
            with col2: st.metric("Invoice Jami", format_currency(inv_total))
            with col3: st.metric("Farq", format_currency(paid_total - inv_total))
            with col4: st.metric("Yuklar Soni", len(df))
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # ADVANCED GRAPHS
            render_advanced_charts(df)
            
        with tab_data:
            # Driver Filter
            drivers = ["All"] + sorted(list(df['Driver'].unique()))
            sel_driver = st.selectbox("🔍 Haydovchini tanlang", drivers, key="driver_select")
            
            # SHOW DRIVER STATISTICS IF SPECIFIC DRIVER SELECTED
            if sel_driver != "All":
                render_driver_statistics(df, sel_driver)
                st.markdown("---")
            
            display_df = df if sel_driver == "All" else df[df['Driver'] == sel_driver]
            
            # Formatted Table
            show_df = display_df.copy()
            for c in ['Kutilgan', 'Tolangan', 'Farq']:
                show_df[c] = show_df[c].apply(format_currency)
                
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Ma'lumotlar Jadvali")
            st.dataframe(
                show_df,
                column_order=("ID", "Start Location", "Start Time", "End Location", "End Time", "Kutilgan", "Tolangan", "Farq", "Status"),
                hide_index=True,
                use_container_width=True,
                height=500
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                txt = generate_txt_report(df)
                st.download_button("📄 TXT Yuklab Olish", txt, f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", "text/plain", use_container_width=True, type="primary")
            with c2:
                xlsx = generate_excel_report(df)
                if xlsx:
                    st.download_button("📊 Excel Yuklab Olish", xlsx, f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True, type="primary")
                else:
                    st.warning("Excel moduli topilmadi (pip install xlsxwriter)")

if __name__ == "__main__":
    main()
