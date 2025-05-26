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
    .kpi-card-link {
        text-decoration: none !important;
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = False
if 'selected_kpi_id' not in st.session_state:
    st.session_state.selected_kpi_id = None

# Handle query parameters
query_params = st.query_params.
if 'kpi' in query_params and query_params['kpi']:
    st.session_state.selected_kpi_id = query_params['kpi'][0]
    st.session_state.show_popup = True

# Data Generation
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

def create_perspective_box(title, icon, kpi_cards_html):
    return f"""
    <div class="perspective-box">
        <div class="perspective-title">{icon} {title}</div>
        <div class="kpi-grid">
            {kpi_cards_html}
        </div>
    </div>
    """

# Chart Creation
def create_chart_for_kpi(kpi_name, subdivision, data_dict, selected_bu, selected_month):
    try:
        if kpi_name == "Revenue":
            filtered_data = data_dict['financial'][(data_dict['financial']['BU'] == selected_bu) & 
                                                 (data_dict['financial']['Subdivision'] == subdivision)]
            fig = px.line(filtered_data, x='Month', y='Revenue', 
                         title=f'{kpi_name} Trend - {subdivision}',
                         markers=True)
        
        elif kpi_name == "Revenue vs Target":
            filtered_data = data_dict['financial'][(data_dict['financial']['BU'] == selected_bu) & 
                                                 (data_dict['financial']['Subdivision'] == subdivision)]
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = (filtered_data['Revenue'].mean() / filtered_data['Target'].mean()) * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': f"{kpi_name} - {subdivision}"},
                gauge = {'axis': {'range': [None, 120]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 100], 'color': "gray"}],
                        'threshold': {'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75, 'value': 100}}))
        
        elif kpi_name in ["CSAT", "NPS"]:
            filtered_data = data_dict['customer'][(data_dict['customer']['BU'] == selected_bu) & 
                                                (data_dict['customer']['Subdivision'] == subdivision)]
            column = 'CSAT' if kpi_name == 'CSAT' else 'NPS'
            fig = px.bar(filtered_data, x='Month', y=column,
                        title=f'{kpi_name} Trend - {subdivision}')
        
        elif kpi_name == "Defect Rate":
            filtered_data = data_dict['quality'][(data_dict['quality']['BU'] == selected_bu) & 
                                               (data_dict['quality']['Subdivision'] == subdivision)]
            fig = px.area(filtered_data, x='Month', y='Defect_Rate',
                         title=f'{kpi_name} Trend - {subdivision}')
        
        elif kpi_name == "System Uptime":
            filtered_data = data_dict['quality'][(data_dict['quality']['BU'] == selected_bu) & 
                                               (data_dict['quality']['Subdivision'] == subdivision)]
            uptime = filtered_data['System_Uptime'].mean()
            fig = go.Figure(data=[go.Pie(labels=['Uptime', 'Downtime'], 
                                       values=[uptime, 100-uptime],
                                       hole=.3)])
            fig.update_layout(title=f'{kpi_name} - {subdivision}')
        
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 3, 2], mode='lines+markers'))
            fig.update_layout(title=f'{kpi_name} - {subdivision}')

        fig.update_layout(height=400, margin=dict(t=40, b=20, l=20, r=20))
        return fig
    
    except Exception as e:
        st.error(f"Chart error: {str(e)}")
        return go.Figure()

# KPI Mapping
kpi_mapping = {
    'revenue': {'name': 'Revenue', 'subdivisions': ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']},
    'revenue_target': {'name': 'Revenue vs Target', 'subdivisions': ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']},
    'gross_margin': {'name': 'Gross Margin', 'subdivisions': ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']},
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
        ['January', 'February', 'March', 'April', 'May', 'June'],
        index=0
    )
    selected_bu = st.radio(
        "🏢 Select Business Unit",
        ['BU1', 'BU2', 'BU3'],
        index=0
    )
    if st.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.rerun()

# Main Content
st.markdown(f"# 📊 {selected_bu} Performance")
st.markdown(f"**Selected Period:** {selected_month}")

# Filter Data
financial_filtered = data['financial'][(data['financial']['BU'] == selected_bu) & 
                                     (data['financial']['Month'] == selected_month)]
customer_filtered = data['customer'][(data['customer']['BU'] == selected_bu) & 
                                   (data['customer']['Month'] == selected_month)]
quality_filtered = data['quality'][(data['quality']['BU'] == selected_bu) & 
                                 (data['quality']['Month'] == selected_month)]
employee_filtered = data['employee'][(data['employee']['BU'] == selected_bu) & 
                                   (data['employee']['Month'] == selected_month)]

# Calculate KPIs
total_revenue = financial_filtered['Revenue'].sum()
avg_gross_margin = financial_filtered['Gross_Margin'].mean()
avg_csat = customer_filtered['CSAT'].mean()
avg_defect_rate = quality_filtered['Defect_Rate'].mean()
avg_engagement = employee_filtered['Engagement_Score'].mean()

# KPI Boxes
col1, col2 = st.columns(2)

with col1:
    financial_box = create_perspective_box("Financial", "💰", 
        create_kpi_card_html("Revenue", f"${total_revenue/1000:.1f}", 8.5, "M", "revenue") +
        create_kpi_card_html("Revenue vs Target", f"{(total_revenue/financial_filtered['Target'].sum()*100):.0f}", 2.3, "%", "revenue_target") +
        create_kpi_card_html("Gross Margin", f"{avg_gross_margin:.0f}", 1.2, "%", "gross_margin") +
        create_kpi_card_html("Cost/Project", f"${financial_filtered['Cost_per_Project'].mean():.0f}", -1.5, "K", "cost_project", True) +
        create_kpi_card_html("AR Days", f"{financial_filtered['AR_Days'].mean():.0f}", -2.1, "", "ar_days", True)
    )
    st.markdown(financial_box, unsafe_allow_html=True)

    quality_box = create_perspective_box("Quality Metrics", "🛠️",
        create_kpi_card_html("Defect Rate", f"{avg_defect_rate:.1f}", -0.8, "%", "defect_rate", True) +
        create_kpi_card_html("System Uptime", f"{quality_filtered['System_Uptime'].mean():.1f}", 0.2, "%", "uptime") +
        create_kpi_card_html("Rework Rate", f"{quality_filtered['Rework_Rate'].mean():.1f}", -1.2, "%", "rework_rate", True) +
        create_kpi_card_html("Resolution", f"{quality_filtered['Resolution_Success'].mean():.0f}", 2.5, "%", "resolution")
    )
    st.markdown(quality_box, unsafe_allow_html=True)

with col2:
    customer_box = create_perspective_box("Customer & Service", "👥",
        create_kpi_card_html("CSAT", f"{avg_csat:.1f}", 1.5, "/5", "csat") +
        create_kpi_card_html("NPS", f"+{customer_filtered['NPS'].mean():.0f}", 3.2, "", "nps") +
        create_kpi_card_html("SLA", f"{customer_filtered['SLA_Achievement'].mean():.0f}", 1.8, "%", "sla") +
        create_kpi_card_html("Response Time", f"{customer_filtered['Avg_Response_Time'].mean():.1f}", -2.3, "h", "response_time", True) +
        create_kpi_card_html("Retention", f"{customer_filtered['Retention_Rate'].mean():.0f}", -0.7, "%", "retention")
    )
    st.markdown(customer_box, unsafe_allow_html=True)

    employee_box = create_perspective_box("Employee Fulfillment", "👔",
        create_kpi_card_html("Engagement", f"{avg_engagement:.1f}", 0.6, "/10", "engagement") +
        create_kpi_card_html("Attrition", f"{employee_filtered['Attrition_Rate'].mean():.1f}", -1.4, "%", "attrition", True) +
        create_kpi_card_html("Training", f"{employee_filtered['Training_Hours'].mean():.0f}", 5.2, "h", "training") +
        create_kpi_card_html("Overtime", f"{employee_filtered['Overtime_per_FTE'].mean():.1f}", 0.9, "h", "overtime")
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
