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

# Custom CSS for better styling and compact layout
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
        cursor: pointer;
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
    .close-btn {
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 24px;
        cursor: pointer;
        color: #666;
    }
    .subdivision-tabs {
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    .subdivision-tab {
        padding: 0.5rem 1rem;
        background: #f0f2f6;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 12px;
    }
    .subdivision-tab.active {
        background: #4f46e5;
        color: white;
    }
    .subdivision-tab:hover {
        background: #e0e7ff;
    }
    .subdivision-tab.active:hover {
        background: #3730a3;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for popup management
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = False
if 'selected_kpi' not in st.session_state:
    st.session_state.selected_kpi = None
if 'selected_subdivision' not in st.session_state:
    st.session_state.selected_subdivision = None

# Data Generation Functions
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

def create_kpi_card_html(title, value, change, unit="", kpi_id="", is_inverse=False):
    """Create HTML for KPI card with click handler"""
    change_class = "positive-change" if (change > 0 and not is_inverse) or (change < 0 and is_inverse) else "negative-change"
    sign = "+" if change > 0 else ""
    return f"""
    <div class="kpi-card" onclick="handleKPIClick('{kpi_id}')">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}{unit}</div>
        <div class="kpi-change {change_class}">{sign}{change:.1f}% vs LY</div>
    </div>
    """

def create_perspective_box(title, icon, kpi_cards_html, kpi_key, available_subdivisions):
    """Create a perspective box containing KPI cards and expandable chart"""
    return f"""
    <div class="perspective-box">
        <div class="perspective-title">{icon} {title}</div>
        <div class="kpi-grid">
            {kpi_cards_html}
        </div>
        <div style="margin-top: 1rem;">
            <details>
                <summary style="color:white; font-weight:bold;">📈 Expand Detailed Analysis</summary>
                <div style="background:#fff; color:#000; padding:1rem; border-radius:10px; margin-top:0.5rem;">
                    <label style="font-size:12px; color:#ccc;">Select Subdivision:</label>
                    <select id="subdivision-{kpi_key}" style="width:100%; padding:0.5rem; border-radius:8px; border:none;">
                        {''.join([f'<option value="{sub}">{sub}</option>' for sub in available_subdivisions])}
                    </select>
                    <div id="chart-container-{kpi_key}" style="height:400px; margin-top:1rem;"></div>
                </div>
            </details>
        </div>
    </div>
    """

def get_available_subdivisions(kpi_name):
    """Get list of available subdivisions for a given KPI"""
    mapping = {
        "revenue": ["PRODEV", "PD1", "PD2", "DOCS", "ITS", "CHAPTER"],
        "revenue_target": ["PRODEV", "PD1", "PD2", "DOCS", "ITS", "CHAPTER"],
        "csat": ["PRODEV", "PD1", "PD2", "DOCS"],
        "nps": ["PRODEV", "PD1", "PD2", "DOCS"],
        "defect_rate": ["PRODEV", "PD1", "PD2", "DOCS", "ITS"],
        "uptime": ["PRODEV", "PD1", "PD2", "DOCS", "ITS"],
        "engagement": ["CHAPTER"],
        "attrition": ["CHAPTER"]
    }
    return mapping.get(kpi_name, [])

def create_chart_for_kpi(kpi_name, subdivision, data_dict, selected_bu, selected_month):
    """Create appropriate chart for selected KPI and subdivision"""
    if kpi_name == "Revenue":
        filtered_data = data_dict['financial'][(data_dict['financial']['BU'] == selected_bu) & 
                                             (data_dict['financial']['Subdivision'] == subdivision)]
        monthly_data = data_dict['financial'][(data_dict['financial']['BU'] == selected_bu) & 
                                            (data_dict['financial']['Subdivision'] == subdivision)]
        fig = px.line(monthly_data, x='Month', y='Revenue', 
                     title=f'{kpi_name} Trend - {subdivision}',
                     markers=True)
        fig.update_layout(height=400)
        return fig
    elif kpi_name == "Revenue vs Target":
        filtered_data = data_dict['financial'][(data_dict['financial']['BU'] == selected_bu) & 
                                             (data_dict['financial']['Subdivision'] == subdivision)]
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = (filtered_data['Revenue'].iloc[0] / filtered_data['Target'].iloc[0]) * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"{kpi_name} - {subdivision}"},
            gauge = {'axis': {'range': [None, 120]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 100], 'color': "gray"}],
                    'threshold': {'line': {'color': "red", 'width': 4},
                                'thickness': 0.75, 'value': 100}}))
        fig.update_layout(height=400)
        return fig
    elif kpi_name in ["CSAT", "NPS"]:
        filtered_data = data_dict['customer'][(data_dict['customer']['BU'] == selected_bu) & 
                                            (data_dict['customer']['Subdivision'] == subdivision)]
        monthly_data = data_dict['customer'][(data_dict['customer']['BU'] == selected_bu) & 
                                           (data_dict['customer']['Subdivision'] == subdivision)]
        column = 'CSAT' if kpi_name == 'CSAT' else 'NPS'
        fig = px.bar(monthly_data, x='Month', y=column,
                    title=f'{kpi_name} Trend - {subdivision}')
        fig.update_layout(height=400)
        return fig
    elif kpi_name == "Defect Rate":
        filtered_data = data_dict['quality'][(data_dict['quality']['BU'] == selected_bu) & 
                                           (data_dict['quality']['Subdivision'] == subdivision)]
        monthly_data = data_dict['quality'][(data_dict['quality']['BU'] == selected_bu) & 
                                          (data_dict['quality']['Subdivision'] == subdivision)]
        fig = px.area(monthly_data, x='Month', y='Defect_Rate',
                     title=f'{kpi_name} Trend - {subdivision}')
        fig.update_layout(height=400)
        return fig
    elif kpi_name == "System Uptime":
        filtered_data = data_dict['quality'][(data_dict['quality']['BU'] == selected_bu) & 
                                           (data_dict['quality']['Subdivision'] == subdivision)]
        uptime = filtered_data['System_Uptime'].iloc[0]
        downtime = 100 - uptime
        fig = go.Figure(data=[go.Pie(labels=['Uptime', 'Downtime'], 
                                   values=[uptime, downtime],
                                   hole=.3)])
        fig.update_layout(title=f'{kpi_name} - {subdivision}', height=400)
        return fig
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3, 4, 5], y=[1, 4, 2, 3, 5], mode='lines+markers'))
        fig.update_layout(title=f'{kpi_name} - {subdivision}', height=400)
        return fig

# Load data
data = generate_dummy_data()

# Sidebar
with st.sidebar:
    st.markdown("## 🎛️ IT Company Dashboard")
    # Month selection
    selected_month = st.selectbox(
        "📅 Select Month",
        ['January', 'February', 'March', 'April', 'May', 'June'],
        index=0
    )
    # Business Unit selection
    selected_bu = st.radio(
        "🏢 Select Business Unit",
        ['BU1', 'BU2', 'BU3'],
        index=0
    )
    # Refresh button
    if st.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("---")
    if st.button("➡️ Go to Advanced Dashboard", type="secondary"):
        st.info("Advanced Dashboard would open here!")

# Main Header
st.markdown(f"# 📊 {selected_bu} Performance")
st.markdown(f"**Selected Period:** {selected_month}")

# Filter data for selected BU and month
financial_filtered = data['financial'][(data['financial']['BU'] == selected_bu) & 
                                     (data['financial']['Month'] == selected_month)]
customer_filtered = data['customer'][(data['customer']['BU'] == selected_bu) & 
                                   (data['customer']['Month'] == selected_month)]
quality_filtered = data['quality'][(data['quality']['BU'] == selected_bu) & 
                                 (data['quality']['Month'] == selected_month)]
employee_filtered = data['employee'][(data['employee']['BU'] == selected_bu) & 
                                   (data['employee']['Month'] == selected_month)]

# Calculate aggregated values
total_revenue = financial_filtered['Revenue'].sum()
revenue_vs_target = ((total_revenue / financial_filtered['Target'].sum()) - 1) * 100 if not financial_filtered.empty else 0
avg_gross_margin = financial_filtered['Gross_Margin'].mean() if not financial_filtered.empty else 0
avg_cost_per_project = financial_filtered['Cost_per_Project'].mean() if not financial_filtered.empty else 0
avg_ar_days = financial_filtered['AR_Days'].mean() if not financial_filtered.empty else 0
avg_csat = customer_filtered['CSAT'].mean() if not customer_filtered.empty else 0
avg_nps = customer_filtered['NPS'].mean() if not customer_filtered.empty else 0
avg_sla = customer_filtered['SLA_Achievement'].mean() if not customer_filtered.empty else 0
avg_response = customer_filtered['Avg_Response_Time'].mean() if not customer_filtered.empty else 0
avg_retention = customer_filtered['Retention_Rate'].mean() if not customer_filtered.empty else 0
avg_defect_rate = quality_filtered['Defect_Rate'].mean() if not quality_filtered.empty else 0
avg_uptime = quality_filtered['System_Uptime'].mean() if not quality_filtered.empty else 0
avg_rework = quality_filtered['Rework_Rate'].mean() if not quality_filtered.empty else 0
avg_resolution = quality_filtered['Resolution_Success'].mean() if not quality_filtered.empty else 0
avg_engagement = employee_filtered['Engagement_Score'].mean() if not employee_filtered.empty else 0
avg_attrition = employee_filtered['Attrition_Rate'].mean() if not employee_filtered.empty else 0
avg_training = employee_filtered['Training_Hours'].mean() if not employee_filtered.empty else 0
avg_overtime = employee_filtered['Overtime_per_FTE'].mean() if not employee_filtered.empty else 0

# Create KPI cards HTML
financial_kpis = (
    create_kpi_card_html("Revenue", f"${total_revenue/1000:.1f}", 12.5, "M", "revenue") +
    create_kpi_card_html("Revenue vs Target", f"{revenue_vs_target:.0f}", -3.0, "%", "revenue_target") +
    create_kpi_card_html("Gross Margin", f"{avg_gross_margin:.0f}", 3.2, "%", "gross_margin") +
    create_kpi_card_html("Cost per Project", f"${avg_cost_per_project:.0f}", 5.1, "K", "cost_project") +
    create_kpi_card_html("AR Days", f"{avg_ar_days:.0f}", -3.0, "", "ar_days", True)
)
customer_kpis = (
    create_kpi_card_html("CSAT", f"{avg_csat:.1f}", 2.3, "/5", "csat") +
    create_kpi_card_html("NPS", f"+{avg_nps:.0f}", 4.2, "", "nps") +
    create_kpi_card_html("SLA Achievement", f"{avg_sla:.0f}", 2.1, "%", "sla") +
    create_kpi_card_html("Avg Response Time", f"{avg_response:.1f}", -3.2, "h", "response_time", True) +
    create_kpi_card_html("Retention Rate", f"{avg_retention:.0f}", -2.1, "%", "retention")
)
quality_kpis = (
    create_kpi_card_html("Defect Rate", f"{avg_defect_rate:.1f}", -0.3, "%", "defect_rate", True) +
    create_kpi_card_html("System Uptime", f"{avg_uptime:.2f}", 0.1, "%", "uptime") +
    create_kpi_card_html("Rework Rate", f"{avg_rework:.1f}", -0.5, "%", "rework_rate", True) +
    create_kpi_card_html("Resolution Success", f"{avg_resolution:.1f}", 1.2, "%", "resolution")
)
employee_kpis = (
    create_kpi_card_html("Engagement Score", f"{avg_engagement:.1f}", 0.4, "/10", "engagement") +
    create_kpi_card_html("Attrition Rate", f"{avg_attrition:.1f}", -1.1, "%", "attrition", True) +
    create_kpi_card_html("Training Hours/Emp", f"{avg_training:.0f}", 5.0, "", "training") +
    create_kpi_card_html("Overtime per FTE", f"{avg_overtime:.1f}", 0.5, "h", "overtime")
)

# 2x2 Grid Layout
col1, col2 = st.columns(2)

with col1:
    st.markdown(create_perspective_box("Financial", "💰", financial_kpis, "revenue", get_available_subdivisions("revenue")), unsafe_allow_html=True)
    st.markdown(create_perspective_box("Quality Metrics", "🛠️", quality_kpis, "defect_rate", get_available_subdivisions("defect_rate")), unsafe_allow_html=True)

with col2:
    st.markdown(create_perspective_box("Customer & Service", "👥", customer_kpis, "csat", get_available_subdivisions("csat")), unsafe_allow_html=True)
    st.markdown(create_perspective_box("Employee Fulfillment", "👔", employee_kpis, "engagement", get_available_subdivisions("engagement")), unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 12px;'>
    📊 IT Company Performance Dashboard | Last Updated: Real-time | 
    <span style='color: #00C851;'>●</span> System Status: Online
    </div>
    """, 
    unsafe_allow_html=True
)
