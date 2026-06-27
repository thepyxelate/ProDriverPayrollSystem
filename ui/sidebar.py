# ui/sidebar.py
import streamlit as st

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
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
            
        return trips_file, invoice_file