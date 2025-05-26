import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
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
        overflow: hidden;
        transition: all 0.3s ease-in-out;
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_kpi' not in st.session_state:
    st.session_state.selected_kpi = None
if 'selected_subdivision' not in st.session_state:
    st.session_state.selected_subdivision = None

# Data Generation
@st.cache_data
def generate_dummy_data():
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    bus = ['BU1', 'BU2', 'BU3']
    subdivisions = ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']
    data = {}
    
    financial_data = []
    customer_data = []
    quality_data = []
    employee_data = []

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
            for subdiv in ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS']:
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
            for subdiv in ['CHAPTER']:
                employee_data.append({
                    'BU': bu,
                    'Month': month,
                    'Subdivision': subdiv,
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

# Create KPI Card HTML
def create_kpi_card(kpi_id, title, value, change, unit="", is_inverse=False):
    change_class = "positive-change" if (change > 0 and not is_inverse) or (change < 0 and is_inverse) else "negative-change"
    sign = "+" if change > 0 else ""
    if st.button(f"{title}\n{value}{unit}\n{sign}{change:.1f}% vs LY", key=kpi_id):
        st.session_state.selected_kpi = kpi_id
        st.rerun()

# Create Perspective Box with optional expandable content
def create_perspective_box(title, icon, kpi_cards_func, perspective_key):
    st.markdown(f"<div class='perspective-box'>", unsafe_allow_html=True)
    st.markdown(f"<div class='perspective-title'>{icon} {title}</div>", unsafe_allow_html=True)
    cols = st.columns(len(kpi_cards_func))
    for i, card in enumerate(kpi_cards_func):
        with cols[i]:
            card()
    st.markdown("</div>", unsafe_allow_html=True)

    # Expanded Analysis Section
    if st.session_state.selected_kpi and st.session_state.selected_kpi.startswith(perspective_key):
        kpi_name = st.session_state.selected_kpi
        subdivision_mapping = {
            "revenue": ["PRODEV", "PD1", "PD2", "DOCS", "ITS", "CHAPTER"],
            "revenue_target": ["PRODEV", "PD1", "PD2", "DOCS", "ITS", "CHAPTER"],
            "csat": ["PRODEV", "PD1", "PD2", "DOCS"],
            "nps": ["PRODEV", "PD1", "PD2", "DOCS"],
            "defect_rate": ["PRODEV", "PD1", "PD2", "DOCS", "ITS"],
            "uptime": ["PRODEV", "PD1", "PD2", "DOCS", "ITS"],
            "engagement": ["CHAPTER"],
            "attrition": ["CHAPTER"]
        }

        subdivisions = subdivision_mapping.get(kpi_name, [])
        selected_subdivision = st.selectbox("Select Subdivision:", subdivisions, key=f"subdiv_{kpi_name}")
        
        if selected_subdivision:
            try:
                fig = create_chart_for_kpi(kpi_name, selected_subdivision, data, selected_bu, selected_month)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating chart: {e}")

# Chart Creation Function
def create_chart_for_kpi(kpi_name, subdivision, data_dict, selected_bu, selected_month):
    if kpi_name == "revenue":
        df = data_dict['financial'][(data_dict['financial']['BU'] == selected_bu) &
                                    (data_dict['financial']['Subdivision'] == subdivision)]
        return px.line(df, x='Month', y='Revenue', title=f'Revenue Trend - {subdivision}')
    elif kpi_name == "revenue_target":
        df = data_dict['financial'][(data_dict['financial']['BU'] == selected_bu) &
                                    (data_dict['financial']['Subdivision'] == subdivision)]
        return px.bar(df, x='Month', y=['Revenue', 'Target'], title=f'Revenue vs Target - {subdivision}')
    elif kpi_name == "csat":
        df = data_dict['customer'][(data_dict['customer']['BU'] == selected_bu) &
                                   (data_dict['customer']['Subdivision'] == subdivision)]
        return px.line(df, x='Month', y='CSAT', title=f'CSAT Trend - {subdivision}')
    elif kpi_name == "nps":
        df = data_dict['customer'][(data_dict['customer']['BU'] == selected_bu) &
                                   (data_dict['customer']['Subdivision'] == subdivision)]
        return px.bar(df, x='Month', y='NPS', title=f'NPS Trend - {subdivision}')
    elif kpi_name == "defect_rate":
        df = data_dict['quality'][(data_dict['quality']['BU'] == selected_bu) &
                                  (data_dict['quality']['Subdivision'] == subdivision)]
        return px.area(df, x='Month', y='Defect_Rate', title=f'Defect Rate Trend - {subdivision}')
    elif kpi_name == "uptime":
        df = data_dict['quality'][(data_dict['quality']['BU'] == selected_bu) &
                                  (data_dict['quality']['Subdivision'] == subdivision)]
        uptime = df['System_Uptime'].mean()
        downtime = 100 - uptime
        return go.Figure(data=[go.Pie(labels=['Uptime', 'Downtime'], values=[uptime, downtime], hole=0.4)])
    elif kpi_name == "engagement":
        df = data_dict['employee'][(data_dict['employee']['BU'] == selected_bu) &
                                   (data_dict['employee']['Subdivision'] == subdivision)]
        return px.line(df, x='Month', y='Engagement_Score', title=f'Engagement Score - {subdivision}')
    elif kpi_name == "attrition":
        df = data_dict['employee'][(data_dict['employee']['BU'] == selected_bu) &
                                   (data_dict['employee']['Subdivision'] == subdivision)]
        return px.bar(df, x='Month', y='Attrition_Rate', title=f'Attrition Rate - {subdivision}')
    return go.Figure()

# Load data
data = generate_dummy_data()

# Sidebar
with st.sidebar:
    selected_month = st.selectbox("📅 Select Month", ['January', 'February', 'March', 'April', 'May', 'June'], index=0)
    selected_bu = st.radio("🏢 Select Business Unit", ['BU1', 'BU2', 'BU3'], index=0)
    if st.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.rerun()

# Main Content
st.markdown(f"# 📊 {selected_bu} Performance")
st.markdown(f"**Selected Period:** {selected_month}")

# Financial Perspective
def render_financial_cards():
    total_revenue = data['financial'][data['financial']['Month'] == selected_month]['Revenue'].sum()
    create_kpi_card("revenue", "Revenue", f"${total_revenue/1000:.1f}", 12.5, "M")
    create_kpi_card("revenue_target", "Revenue vs Target", "+95%", -3.0, "%")

create_perspective_box("Financial", "💰", render_financial_cards, "revenue")

# Customer & Service Perspective
def render_customer_cards():
    avg_csat = data['customer'][data['customer']['Month'] == selected_month]['CSAT'].mean()
    create_kpi_card("csat", "CSAT", f"{avg_csat:.1f}", 2.3, "/5")
    create_kpi_card("nps", "NPS", "+45", 4.2, "")

create_perspective_box("Customer & Service", "👥", render_customer_cards, "csat")

# Quality Metrics Perspective
def render_quality_cards():
    avg_defect = data['quality'][data['quality']['Month'] == selected_month]['Defect_Rate'].mean()
    create_kpi_card("defect_rate", "Defect Rate", f"{avg_defect:.1f}", -0.3, "%", True)
    avg_uptime = data['quality'][data['quality']['Month'] == selected_month]['System_Uptime'].mean()
    create_kpi_card("uptime", "System Uptime", f"{avg_uptime:.2f}", 0.1, "%")

create_perspective_box("Quality Metrics", "🛠️", render_quality_cards, "defect_rate")

# Employee Fulfillment Perspective
def render_employee_cards():
    avg_engagement = data['employee'][data['employee']['Month'] == selected_month]['Engagement_Score'].mean()
    create_kpi_card("engagement", "Engagement", f"{avg_engagement:.1f}", 0.4, "/10")
    avg_attrition = data['employee'][data['employee']['Month'] == selected_month]['Attrition_Rate'].mean()
    create_kpi_card("attrition", "Attrition", f"{avg_attrition:.1f}", -1.1, "%", True)

create_perspective_box("Employee Fulfillment", "👔", render_employee_cards, "engagement")

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center; color:#666;'>Dashboard by IT Analytics Team | Last Updated: Real-time</div>", unsafe_allow_html=True)
