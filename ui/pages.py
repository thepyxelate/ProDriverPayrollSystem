# ui/pages.py
import streamlit as st
import pandas as pd

from ui.components import (
    glass_card, render_top_earners, render_rpm_chart, render_mini_stat
)
from core.calculator import compute_driver_stats
from utils.helpers import format_currency

def render_analytics_tab(df: pd.DataFrame, invoice_total: float):
    """Analytics tab - grafiklar va metrikalar"""
    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    paid_total = df['Tolangan'].sum()
    
    with col1:
        st.metric("Jami To'langan", format_currency(paid_total))
    with col2:
        st.metric("Invoice Jami", format_currency(invoice_total))
    with col3:
        st.metric("Farq", format_currency(paid_total - invoice_total))
    with col4:
        st.metric("Yuklar Soni", len(df))
    
    # Average RPM
    has_rpm = 'RPM' in df.columns and df['RPM'].sum() > 0
    avg_rpm = df['RPM'].mean() if has_rpm else 0
    with col5:
        st.metric("Oʻrtacha RPM", f"{avg_rpm:.2f}" if has_rpm else "N/A")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grafiklar
    with glass_card("💰 Top 15 Haydovchilar - Jami Daromad"):
       render_top_earners(df)
    
    # Qo'shimcha grafiklar (o'rtacha daromad, trip soni, yo'nalishlar - hozircha qisqartirildi)
    # Bu yerda oldingi kodlardagi 2-4-chi grafiklarni qo'shishingiz mumkin
    
    # RPM chart
    with glass_card("📈 Oʻrtacha RPM (Milega To'g'ri Keladigan Daromad) - Top 15"):
        render_rpm_chart(df)


def render_data_tab(df: pd.DataFrame):
    """Data & Export tab"""
    drivers = ["All"] + sorted(list(df['Driver'].unique()))
    sel_driver = st.selectbox("🔍 Haydovchini tanlang", drivers, key="driver_select")
    
    if sel_driver != "All":
        stats = compute_driver_stats(df, sel_driver)# ui/pages.py
def render_data_tab(df: pd.DataFrame):
    """Data & Export tab"""
    drivers = ["All"] + sorted(list(df['Driver'].unique()))
    sel_driver = st.selectbox("🔍 Haydovchini tanlang", drivers, key="driver_select")
    
    if sel_driver != "All":
        stats = compute_driver_stats(df, sel_driver)
        if stats:
            # Haydovchi statistikasi - ustunlar soni: RPM va Miles mavjudligiga qarab
            col_count = 5  # default: Jami Daromad, Jami Triplar, To'langan, Kutilmoqda, Progress
            if stats['has_rpm']:
                col_count += 1
            if stats['has_miles']:
                col_count += 1  # Jami Miles uchun
            
            cols = st.columns(col_count)
            idx = 0
            
            with cols[idx]:
                render_mini_stat("Jami Daromad", format_currency(stats['total_earned']))
            idx += 1
            
            with cols[idx]:
                render_mini_stat("Jami Triplar", stats['total_trips'])
            idx += 1
            
            # Eski "O'rtacha/Trip" o'rniga "Jami Miles" (agar mavjud bo'lsa)
            if stats['has_miles']:
                with cols[idx]:
                    render_mini_stat("Jami Miles", f"{stats['total_miles']:.0f}", "#60A5FA")
                idx += 1
            
            with cols[idx]:
                render_mini_stat("To'langan", stats['paid_trips'], "#10B981")
            idx += 1
            
            with cols[idx]:
                render_mini_stat("Kutilmoqda", stats['unpaid_trips'], "#EF4444")
            idx += 1
            
            if stats['has_rpm']:
                with cols[idx]:
                    render_mini_stat("Oʻrtacha RPM", f"{stats['avg_rpm']:.2f}", "#FBBF24")
                idx += 1
            
            # Progress bar
            st.markdown(f"""
            <div class="glass-card">
                <h4>🎯 To'lovlar Bajarilish Darajasi</h4>
                <div class="custom-progress">
                    <div class="custom-progress-fill" style="width: {stats['completion_rate']:.1f}%;"></div>
                </div>
                <p style="text-align: center; color: #aaa; margin-top: 10px;">{stats['completion_rate']:.1f}% ({stats['paid_trips']} / {stats['total_trips']})</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("---")
    
    # Jadval qismi o'zgarishsiz
    display_df = df if sel_driver == "All" else df[df['Driver'] == sel_driver]
    show_df = display_df.copy()
    for c in ['Kutilgan', 'Tolangan', 'Farq']:
        show_df[c] = show_df[c].apply(format_currency)
    
    col_order = ["ID", "Start Location", "Start Time", "End Location", "End Time", "Kutilgan", "Tolangan", "Farq", "Status"]
    if 'RPM' in df.columns and df['RPM'].sum() > 0:
        col_order.insert(8, "RPM")
    if 'Miles' in df.columns and df['Miles'].sum() > 0:
        col_order.insert(9, "Miles")
    
    with glass_card("📊 Ma'lumotlar Jadvali"):
        st.dataframe(
            show_df,
            column_order=col_order,
            hide_index=True,
            use_container_width=True,
            height=500
        )