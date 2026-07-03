# ui/components.py
from contextlib import contextmanager
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.helpers import format_currency

@contextmanager
def glass_card(title: str = None):
    """Glassmorphism kartasi - kontekst menejer sifatida"""
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if title:
            st.markdown(f"### {title}")
        yield  # Bu yerda blok ichidagi kontent chiqariladi
        st.markdown('</div>', unsafe_allow_html=True)


def render_top_earners(df: pd.DataFrame):
    """Top 15 daromadli haydovchilar"""
    driver_earnings = df.groupby('Driver')['Tolangan'].sum().reset_index()
    driver_earnings = driver_earnings[driver_earnings['Driver'] != "UNKNOWN"]
    driver_earnings = driver_earnings.sort_values('Tolangan', ascending=False).head(15)
    
    fig = px.bar(
        driver_earnings,
        x='Tolangan',
        y='Driver',
        orientation='h',
        text='Tolangan',
        color='Tolangan',
        color_continuous_scale=['#3a7bd5', '#00d2ff', '#00fff2']
    )
    fig.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
    fig.update_layout(
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
    st.plotly_chart(fig, use_container_width=True)


def render_rpm_chart(df: pd.DataFrame):
    """Top 15 haydovchi bo'yicha o'rtacha RPM"""
    if 'RPM' not in df.columns or df['RPM'].sum() == 0:
        st.info("💡 RPM (Rate Per Mile) ko'rsatish uchun Trips faylida '$X.XX/mi' qatori bo'lishi kerak.")
        return
    
    driver_avg_rpm = df.groupby('Driver')['RPM'].mean().reset_index()
    driver_avg_rpm = driver_avg_rpm[driver_avg_rpm['Driver'] != "UNKNOWN"]
    driver_avg_rpm = driver_avg_rpm.sort_values('RPM', ascending=False).head(15)
    
    if driver_avg_rpm.empty:
        st.info("RPM ma'lumotlari mavjud emas.")
        return
    
    fig = px.bar(
        driver_avg_rpm,
        x='RPM',
        y='Driver',
        orientation='h',
        text='RPM',
        color='RPM',
        color_continuous_scale=['#f093fb', '#4facfe', '#00f2fe']
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(autorange="reversed", title=""),
        xaxis=dict(title="RPM ($/mil)", showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig, use_container_width=True)


def render_mini_stat(label: str, value, color: str = "#00d2ff"):
    """Mini-stat kartasi"""
    st.markdown(f"""
    <div class="mini-stat">
        <div class="mini-stat-label">{label}</div>
        <div class="mini-stat-value" style="color: {color};">{value}</div>
    </div>
    """, unsafe_allow_html=True)