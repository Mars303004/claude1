import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="IT Company Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    .perspective-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem;
        color: white;
        height: 280px;
        overflow: hidden;
    }
    .perspective-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 0.8rem;
        text-align: center;
        border-bottom: 2px solid rgba(255,255,255,0.3);
        padding-bottom: 0.5rem;
    }
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 0.5rem;
        height: calc(100% - 60px);
    }
    .kpi-card {
        background: rgba(255,255,255,0.15);
        border-radius: 8px;
        padding: 0.5rem;
        text-align: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 80px;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        background: rgba(255,255,255,0.25);
        cursor: pointer;
    }
    .kpi-title {
        font-size: 10px;
        opacity: 0.9;
        margin-bottom: 0.2rem;
    }
    .kpi-value {
        font-size: 16px;
        font-weight: bold;
        margin: 0.1rem 0;
    }
    .kpi-change {
        font-size: 9px;
        margin-top: 0.1rem;
    }
    .positive-change {
        color: #00ff88 !important;
    }
    .negative-change {
        color: #ff6b6b !important;
    }
    .popup-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.7);
        z-index: 1000;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .popup-content {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        max-width: 80%;
        max-height: 80%;
        overflow: auto;
        position: relative;
    }
    .kpi-card-link {
        text-decoration: none !important;
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = False
if 'selected_kpi' not in st.session_state:
    st.session_state.selected_kpi = None

# Handle query parameters
query_params = st.experimental_get_query_params()
if 'kpi' in query_params and query_params['kpi']:
    st.session_state.selected_kpi_id = query_params['kpi'][0]
    st.session_state.show_popup = True

# Data Generation
@st.cache_data
def generate_dummy_data():
    # ... (same data generation code as previous)
    return data

# KPI Card Component
def create_kpi_card_html(title, value, change, unit="", kpi_id="", is_inverse=False):
    change_class = "positive-change" if (change > 0 and not is_inverse) or (change < 0 and is_inverse) else "negative-change"
    sign = "+" if change > 0 else ""
    
    return f"""
    <a href="?kpi={kpi_id}" class="kpi-card-link">
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}{unit}</div>
            <div class="kpi-change {change_class}">{sign}{change:.1f}% vs LY</div>
        </div>
    </a>
    """

# Chart Creation
def create_chart_for_kpi(kpi_name, subdivision, data_dict, selected_bu, selected_month):
    # ... (same chart creation code as previous)
    return fig

# KPI Mapping
kpi_mapping = {
    'revenue': {'name': 'Revenue', 'subdivisions': ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']},
    'revenue_target': {'name': 'Revenue vs Target', 'subdivisions': ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']},
    'csat': {'name': 'CSAT', 'subdivisions': ['PRODEV', 'PD1', 'PD2', 'DOCS']},
    'nps': {'name': 'NPS', 'subdivisions': ['PRODEV', 'PD1', 'PD2', 'DOCS']},
    'defect_rate': {'name': 'Defect Rate', 'subdivisions': ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS']},
    'uptime': {'name': 'System Uptime', 'subdivisions': ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS']},
    'engagement': {'name': 'Engagement Score', 'subdivisions': ['CHAPTER']},
    'attrition': {'name': 'Attrition Rate', 'subdivisions': ['CHAPTER']}
}

# Load Data
data = generate_dummy_data()

# Sidebar
with st.sidebar:
    st.markdown("## 🎛️ IT Company Dashboard")
    selected_month = st.selectbox("📅 Select Month", ['January', 'February', 'March', 'April', 'May', 'June'])
    selected_bu = st.radio("🏢 Select Business Unit", ['BU1', 'BU2', 'BU3'])
    if st.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.rerun()

# Main Content
st.markdown(f"# 📊 {selected_bu} Performance")
st.markdown(f"**Selected Period:** {selected_month}")

# KPI Boxes
col1, col2 = st.columns(2)

with col1:
    financial_box = create_perspective_box("Financial", "💰", 
        create_kpi_card_html("Revenue", f"${1500/1000:.1f}", 12.5, "M", "revenue") +
        create_kpi_card_html("Revenue vs Target", "98", -3.0, "%", "revenue_target") +
        create_kpi_card_html("Gross Margin", "32", 3.2, "%", "gross_margin") +
        create_kpi_card_html("Cost per Project", "$450", 5.1, "K", "cost_project") +
        create_kpi_card_html("AR Days", "35", -3.0, "", "ar_days", True)
    )
    st.markdown(financial_box, unsafe_allow_html=True)

    quality_box = create_perspective_box("Quality Metrics", "🛠️",
        create_kpi_card_html("Defect Rate", "1.2", -0.3, "%", "defect_rate", True) +
        create_kpi_card_html("System Uptime", "99.8", 0.1, "%", "uptime") +
        create_kpi_card_html("Rework Rate", "3.1", -0.5, "%", "rework_rate", True) +
        create_kpi_card_html("Resolution Success", "97.5", 1.2, "%", "resolution")
    )
    st.markdown(quality_box, unsafe_allow_html=True)

with col2:
    customer_box = create_perspective_box("Customer & Service", "👥",
        create_kpi_card_html("CSAT", "4.2", 2.3, "/5", "csat") +
        create_kpi_card_html("NPS", "+48", 4.2, "", "nps") +
        create_kpi_card_html("SLA Achievement", "95", 2.1, "%", "sla") +
        create_kpi_card_html("Avg Response Time", "2.4", -3.2, "h", "response_time", True) +
        create_kpi_card_html("Retention Rate", "92", -2.1, "%", "retention")
    )
    st.markdown(customer_box, unsafe_allow_html=True)

    employee_box = create_perspective_box("Employee Fulfillment", "👔",
        create_kpi_card_html("Engagement Score", "8.1", 0.4, "/10", "engagement") +
        create_kpi_card_html("Attrition Rate", "9.2", -1.1, "%", "attrition", True) +
        create_kpi_card_html("Training Hours/Emp", "45", 5.0, "", "training") +
        create_kpi_card_html("Overtime per FTE", "3.2", 0.5, "h", "overtime")
    )
    st.markdown(employee_box, unsafe_allow_html=True)

# Popup Handling
if st.session_state.show_popup and 'selected_kpi_id' in st.session_state:
    kpi_id = st.session_state.selected_kpi_id
    kpi_info = kpi_mapping.get(kpi_id)
    
    if kpi_info:
        st.markdown("---")
        st.markdown(f"### 📈 Detailed Analysis: {kpi_info['name']}")
        
        selected_subdivision = st.selectbox(
            "Select Subdivision:",
            kpi_info['subdivisions'],
            key="subdivision_select"
        )
        
        try:
            chart = create_chart_for_kpi(
                kpi_info['name'], 
                selected_subdivision, 
                data, 
                selected_bu, 
                selected_month
            )
            st.plotly_chart(chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")
        
        if st.button("❌ Close Analysis", key="close_popup"):
            st.session_state.show_popup = False
            st.session_state.selected_kpi_id = None
            st.experimental_set_query_params()
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
📊 IT Company Performance Dashboard | Last Updated: Real-time | 
<span style='color: #00C851;'>●</span> System Status: Online
</div>
""", unsafe_allow_html=True)
