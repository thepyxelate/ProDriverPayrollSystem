# app.py
import streamlit as st

# =============================================================================
# 1. SAHIFA SOZLAMALARI
# =============================================================================
st.set_page_config(
    page_title="Pro Driver Payroll System",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# 2. STIL (GLASSMORPHISM) - oldingi CSS ni shu yerga qo'yamiz
# =============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Outfit', sans-serif; }
    
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
    
    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 15px;
        padding: 10px;
    }
    
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
    
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
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

# =============================================================================
# 3. IMPORTS (loyiha ichidagi modullardan)
# =============================================================================
from ui.sidebar import render_sidebar
from core.parsers import TripsParser, InvoiceParser
from core.calculator import build_dataframe
from core.exporter import generate_txt_report, generate_excel_report
from ui.pages import render_analytics_tab, render_data_tab
from datetime import datetime

# =============================================================================
# 4. ASOSIY FUNKSIYALAR
# =============================================================================
def render_hero_header():
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 class="hero-title">🚚 Pro Driver Payroll</h1>
        <p style="color: #a0a0a0; font-size: 1.1rem;">Professional Accounting & Analytics System</p>
    </div>
    """, unsafe_allow_html=True)

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
                    st.session_state['trips_data'][item['id']].drivers = [selected]
                    st.rerun()

# =============================================================================
# 5. MAIN
# =============================================================================
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
    
    # Parse trips
    if 'trips_data' not in st.session_state:
        with st.spinner("🔄 AI Tahlil qilmoqda..."):
            parser = TripsParser(trips_file.getvalue().decode("utf-8"))
            st.session_state['trips_data'] = parser.parse()
    
    # Parse invoice
    if 'invoice_data' not in st.session_state:
        with st.spinner("💰 Moliyaviy hisoblanmoqda..."):
            parser = InvoiceParser(invoice_file.getvalue().decode("utf-8"))
            data, total = parser.parse()
            st.session_state['invoice_data'] = data
            st.session_state['invoice_total'] = total
    
    trips_data = st.session_state['trips_data']
    invoice_data = st.session_state['invoice_data']
    
    # Resolve conflicts
    all_known_drivers = set()
    for t in trips_data.values():
        for d in t.drivers:
            if d != "UNKNOWN":
                all_known_drivers.add(d)
    sorted_drivers = sorted(list(all_known_drivers))
    
    ids_to_resolve = []
    
    # Multi-driver
    for t_id, trip in trips_data.items():
        if len(trip.drivers) > 1:
            ids_to_resolve.append({'id': t_id, 'reason': 'Multi-Driver', 'options': trip.drivers})
    
    # Paid No Driver
    for t_id, trip in trips_data.items():
        inv = invoice_data.get(t_id)
        if inv and inv.paid_amount > 0 and trip.drivers == ["UNKNOWN"]:
            if not any(x['id'] == t_id for x in ids_to_resolve):
                ids_to_resolve.append({'id': t_id, 'reason': 'Paid (No Driver)', 'options': sorted_drivers})
    
    # Extra Pay
    processed = set(trips_data.keys())
    for i_id, inv in invoice_data.items():
        if i_id not in processed and i_id not in trips_data:
            from core.models import Trip
            trips_data[i_id] = Trip(
                id=i_id,
                drivers=["UNKNOWN"],
                expected_pay=0.0,
                status="Extra/Dispute",
                loads_str="-",
                start_location=inv.route,
                end_location="",
                start_time="",
                end_time="",
                rpm=0.0
            )
            ids_to_resolve.append({'id': i_id, 'reason': 'Extra Pay', 'options': sorted_drivers})
    
    render_assignment_section(ids_to_resolve, trips_data, invoice_data, sorted_drivers)
    
    # Build DataFrame
    df = build_dataframe(trips_data, invoice_data)
    
    if not df.empty:
        tab_analytics, tab_data = st.tabs(["📊 Smart Analytics", "📋 Data & Export"])
        
        with tab_analytics:
            render_analytics_tab(df, st.session_state['invoice_total'])
        
        with tab_data:
            render_data_tab(df)
            
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