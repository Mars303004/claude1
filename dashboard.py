# KPI Dashboard - Responsive Modular Version

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# Page config
st.set_page_config(
    page_title="KPI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Breakpoints
st.markdown("""
<style>
@media screen and (max-width: 768px) {
    .kpi-card { font-size: 14px !important; }
    .kpi-card h3 { font-size: 12px !important; }
}
@media screen and (min-width: 769px) {
    .kpi-card { font-size: 16px !important; }
    .kpi-card h3 { font-size: 14px !important; }
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_bu' not in st.session_state:
    st.session_state.selected_bu = 'BU1'
if 'selected_month' not in st.session_state:
    st.session_state.selected_month = 'January'

# Dummy data generator (safe)
def generate_kpi():
    return {
        'value': random.randint(80, 120),
        'unit': '%',
        'change': random.randint(-10, 10)
    }

# Create KPI card
def create_kpi_card(title, data):
    value = data['value']
    unit = data['unit']
    change = data['change']
    if change > 0:
        icon, color = '📈', '#4caf50'
        change_str = f"+{change}%"
    elif change < 0:
        icon, color = '📉', '#f44336'
        change_str = f"{change}%"
    else:
        icon, color = '➡️', '#757575'
        change_str = "0%"

    html = f"""
    <div class="kpi-card" style="
        background:white; border-radius:12px; padding:20px;
        box-shadow:0 2px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
    ">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>{title}</div>
            <div style="background:{color};color:white;padding:4px 8px;border-radius:8px;font-size:12px;">{icon} {change_str}</div>
        </div>
        <h3 style="margin:10px 0;">{value}{unit}</h3>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Filters")
    month = st.selectbox("Select Month", ['January', 'February', 'March'])
    bu = st.radio("Business Unit", ['BU1', 'BU2', 'BU3'])
    if month != st.session_state.selected_month or bu != st.session_state.selected_bu:
        st.session_state.selected_month = month
        st.session_state.selected_bu = bu
        st.rerun()

# Main Title
st.markdown("""
<div style="
    background:linear-gradient(to right,#667eea,#764ba2);
    color:white;padding:20px;border-radius:10px;text-align:center;
">
    <h1 style="margin:0;">KPI Dashboard - {}</h1>
    <p style="margin:0;">{}</p>
</div>
""".format(st.session_state.selected_bu, st.session_state.selected_month), unsafe_allow_html=True)

# Responsive layout
is_mobile = st.columns(1)[0]._width <= 400

# Display KPIs
section_title = st.markdown("### 📊 Financial")

cols = st.columns(1 if is_mobile else 3)
kpi_titles = ['Revenue vs Target', 'Gross Margin', 'Cost per Project']

for idx, title in enumerate(kpi_titles):
    with cols[idx % len(cols)]:
        data = generate_kpi()
        create_kpi_card(title, data)
