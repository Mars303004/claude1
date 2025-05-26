import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
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
    /* ... (keep all previous CSS styles) ... */
    .kpi-card {
        /* tambahkan properti ini */
        pointer-events: auto !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_kpi' not in st.session_state:
    st.session_state.selected_kpi = None

# Data Generation (gunakan fungsi generate_dummy_data yang sudah diperbaiki sebelumnya)
@st.cache_data
def generate_dummy_data():
    """Generate comprehensive dummy data for the dashboard"""
    
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    bus = ['BU1', 'BU2', 'BU3']
    subdivisions = ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']
    
    data = {}
    
    # Financial Data
    financial_data = []
    for bu in bus:
        for month in months:
            for subdiv in subdivisions:
                revenue = random.randint(800, 1500) if subdiv in ['PRODEV', 'PD1', 'PD2'] else random.randint(200, 600)
                financial_data.append({
                    'BU': bu,
                    'Month': month,
                    'Subdivision': subdiv,
                    'Revenue': revenue,
                    'Target': revenue * random.uniform(0.8, 1.2),
                    'Gross_Margin': random.uniform(25, 45),
                    'Cost_per_Project': random.randint(300, 600),
                    'AR_Days': random.randint(25, 40)
                })
    
    # Customer & Service Data
    customer_data = []
    for bu in bus:
        for month in months:
            for subdiv in ['PRODEV', 'PD1', 'PD2', 'DOCS']:
                customer_data.append({
                    'BU': bu,
                    'Month': month,
                    'Subdivision': subdiv,
                    'CSAT': random.uniform(3.8, 4.5),
                    'NPS': random.randint(35, 55),
                    'SLA_Achievement': random.uniform(85, 98),
                    'Avg_Response_Time': random.uniform(1.5, 4.0),
                    'Retention_Rate': random.uniform(88, 96)
                })
    
    # Quality Data
    quality_data = []
    for bu in bus:
        for month in months:
            subdivs = ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS']
            for subdiv in subdivs:
                quality_data.append({
                    'BU': bu,
                    'Month': month,
                    'Subdivision': subdiv,
                    'Defect_Rate': random.uniform(0.5, 3.0),
                    'System_Uptime': random.uniform(98.5, 99.9),
                    'Rework_Rate': random.uniform(2.0, 8.0),
                    'Resolution_Success': random.uniform(94, 99),
                    'Code_Review_Coverage': random.uniform(75, 95)
                })
    
    # Employee Data
    employee_data = []
    for bu in bus:
        for month in months:
            employee_data.append({
                'BU': bu,
                'Month': month,
                'Subdivision': 'CHAPTER',
                'Engagement_Score': random.uniform(7.0, 8.5),
                'Attrition_Rate': random.uniform(5, 12),
                'Training_Hours': random.randint(35, 55),
                'Overtime_per_FTE': random.uniform(2.0, 4.5),
                'Promotion_Rate': random.uniform(8, 15)
            })
    
    data['financial'] = pd.DataFrame(financial_data)
    data['customer'] = pd.DataFrame(customer_data)
    data['quality'] = pd.DataFrame(quality_data)
    data['employee'] = pd.DataFrame(employee_data)
    
    return data

# KPI Card Component (diubah menggunakan button)
def create_kpi_card(title, value, change, unit="", kpi_id="", is_inverse=False):
    change_class = "positive-change" if (change > 0 and not is_inverse) or (change < 0 and is_inverse) else "negative-change"
    sign = "+" if change > 0 else ""
    
    return st.button(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}{unit}</div>
            <div class="kpi-change {change_class}">{sign}{change:.1f}% vs LY</div>
        </div>
        """,
        key=f"btn_{kpi_id}",
        on_click=lambda: st.session_state.update(selected_kpi=kpi_id),
        unsafe_allow_html=True
    )

def create_perspective_box(title, icon, kpi_cards):
    return f"""
    <div class="perspective-box">
        <div class="perspective-title">{icon} {title}</div>
        <div class="kpi-grid">
            {"".join(kpi_cards)}
        </div>
    </div>
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
    selected_month = st.selectbox(
        "📅 Select Month",
        ['January', 'February', 'March', 'April', 'May', 'June']
    )
    selected_bu = st.radio(
        "🏢 Select Business Unit",
        ['BU1', 'BU2', 'BU3']
    )
    if st.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.rerun()

# Main Content
st.markdown(f"# 📊 {selected_bu} Performance")
st.markdown(f"**Selected Period:** {selected_month}")

# KPI Boxes
col1, col2 = st.columns(2)

with col1:
    financial_cards = [
        create_kpi_card("Revenue", "$1.5", 12.5, "M", "revenue"),
        create_kpi_card("Revenue vs Target", "98", -3.0, "%", "revenue_target"),
        create_kpi_card("Gross Margin", "32", 3.2, "%", "gross_margin"),
        create_kpi_card("Cost/Project", "$450", 5.1, "K", "cost_project"),
        create_kpi_card("AR Days", "35", -3.0, "", "ar_days", True)
    ]
    st.markdown(create_perspective_box("Financial", "💰", financial_cards), unsafe_allow_html=True)
    
    quality_cards = [
        create_kpi_card("Defect Rate", "1.2", -0.3, "%", "defect_rate", True),
        create_kpi_card("System Uptime", "99.8", 0.1, "%", "uptime"),
        create_kpi_card("Rework Rate", "3.1", -0.5, "%", "rework_rate", True),
        create_kpi_card("Resolution", "97.5", 1.2, "%", "resolution")
    ]
    st.markdown(create_perspective_box("Quality Metrics", "🛠️", quality_cards), unsafe_allow_html=True)

with col2:
    customer_cards = [
        create_kpi_card("CSAT", "4.2", 2.3, "/5", "csat"),
        create_kpi_card("NPS", "+48", 4.2, "", "nps"),
        create_kpi_card("SLA", "95", 2.1, "%", "sla"),
        create_kpi_card("Response Time", "2.4", -3.2, "h", "response_time", True),
        create_kpi_card("Retention", "92", -2.1, "%", "retention")
    ]
    st.markdown(create_perspective_box("Customer & Service", "👥", customer_cards), unsafe_allow_html=True)
    
    employee_cards = [
        create_kpi_card("Engagement", "8.1", 0.4, "/10", "engagement"),
        create_kpi_card("Attrition", "9.2", -1.1, "%", "attrition", True),
        create_kpi_card("Training", "45", 5.0, "h", "training"),
        create_kpi_card("Overtime", "3.2", 0.5, "h", "overtime")
    ]
    st.markdown(create_perspective_box("Employee Fulfillment", "👔", employee_cards), unsafe_allow_html=True)

# Handle expander
if st.session_state.selected_kpi:
    kpi_info = kpi_mapping.get(st.session_state.selected_kpi)
    if kpi_info:
        with st.expander(f"📈 Detailed Analysis: {kpi_info['name']}", expanded=True):
            selected_subdivision = st.selectbox(
                "Select Subdivision:",
                kpi_info['subdivisions'],
                key="subdivision_select"
            )
            
            chart = create_chart_for_kpi(
                kpi_info['name'], 
                selected_subdivision, 
                data, 
                selected_bu, 
                selected_month
            )
            st.plotly_chart(chart, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
📊 IT Company Performance Dashboard | Last Updated: Real-time | 
<span style='color: #00C851;'>●</span> System Status: Online
</div>
""", unsafe_allow_html=True)
