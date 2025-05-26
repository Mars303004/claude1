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
    .kpi-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 10px;
        color: white;
        padding: 15px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 12px;
        text-align: center;
        min-height: 80px;
        width: 100%;
    }
    .kpi-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        color: white;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-title {
        font-size: 14px;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    .metric-change {
        font-size: 12px;
        margin-top: 0.5rem;
    }
    .positive-change {
        color: #00ff88 !important;
    }
    .negative-change {
        color: #ff6b6b !important;
    }
    .analysis-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        color: white;
        animation: slideDown 0.4s ease-out;
    }
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .subdivision-selector {
        margin: 1rem 0;
    }
    .close-button {
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        margin-top: 1rem;
    }
    .close-button:hover {
        background: rgba(255,255,255,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for KPI expansion
if 'expanded_kpi' not in st.session_state:
    st.session_state.expanded_kpi = {}

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

def create_chart_for_kpi(kpi_name, subdivision, data_dict, selected_bu, selected_month):
    """Create appropriate chart for selected KPI and subdivision"""
    
    if kpi_name == "Revenue":
        monthly_data = data_dict['financial'][(data_dict['financial']['BU'] == selected_bu) & 
                                            (data_dict['financial']['Subdivision'] == subdivision)]
        
        fig = px.line(monthly_data, x='Month', y='Revenue', 
                     title=f'{kpi_name} Trend - {subdivision}',
                     markers=True, height=300)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=14
        )
        return fig
        
    elif kpi_name == "Revenue vs Target":
        filtered_data = data_dict['financial'][(data_dict['financial']['BU'] == selected_bu) & 
                                             (data_dict['financial']['Month'] == selected_month) &
                                             (data_dict['financial']['Subdivision'] == subdivision)]
        
        if not filtered_data.empty:
            value = (filtered_data['Revenue'].iloc[0] / filtered_data['Target'].iloc[0]) * 100
        else:
            value = 85
            
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"{kpi_name} - {subdivision}", 'font': {'color': 'white', 'size': 14}},
            gauge = {'axis': {'range': [None, 120]},
                    'bar': {'color': "#00ff88"},
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(255,255,255,0.1)"},
                        {'range': [50, 100], 'color': "rgba(255,255,255,0.2)"}],
                    'threshold': {'line': {'color': "red", 'width': 4},
                                'thickness': 0.75, 'value': 100}}))
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        return fig
        
    elif kpi_name in ["CSAT", "NPS"]:
        monthly_data = data_dict['customer'][(data_dict['customer']['BU'] == selected_bu) & 
                                           (data_dict['customer']['Subdivision'] == subdivision)]
        
        column = 'CSAT' if kpi_name == 'CSAT' else 'NPS'
        fig = px.bar(monthly_data, x='Month', y=column,
                    title=f'{kpi_name} Trend - {subdivision}', height=300)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=14
        )
        return fig
        
    elif kpi_name == "Defect Rate":
        monthly_data = data_dict['quality'][(data_dict['quality']['BU'] == selected_bu) & 
                                          (data_dict['quality']['Subdivision'] == subdivision)]
        
        fig = px.area(monthly_data, x='Month', y='Defect_Rate',
                     title=f'{kpi_name} Trend - {subdivision}', height=300)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=14
        )
        return fig
        
    elif kpi_name == "System Uptime":
        filtered_data = data_dict['quality'][(data_dict['quality']['BU'] == selected_bu) & 
                                           (data_dict['quality']['Month'] == selected_month) &
                                           (data_dict['quality']['Subdivision'] == subdivision)]
        
        if not filtered_data.empty:
            uptime = filtered_data['System_Uptime'].iloc[0]
        else:
            uptime = 99.2
            
        downtime = 100 - uptime
        
        fig = go.Figure(data=[go.Pie(labels=['Uptime', 'Downtime'], 
                                   values=[uptime, downtime],
                                   hole=.3,
                                   marker_colors=['#00ff88', '#ff6b6b'])])
        fig.update_layout(
            title={'text': f'{kpi_name} - {subdivision}', 'font': {'color': 'white', 'size': 14}}, 
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        return fig
        
    elif kpi_name in ["Gross Margin", "SLA Achievement", "Retention Rate", "Resolution Success", "Engagement Score", "Training Hours/Emp"]:
        # For different KPIs, get the right data source and column
        if kpi_name == "Gross Margin":
            monthly_data = data_dict['financial'][(data_dict['financial']['BU'] == selected_bu) & 
                                                (data_dict['financial']['Subdivision'] == subdivision)]
            column = 'Gross_Margin'
        elif kpi_name == "SLA Achievement":
            monthly_data = data_dict['customer'][(data_dict['customer']['BU'] == selected_bu) & 
                                               (data_dict['customer']['Subdivision'] == subdivision)]
            column = 'SLA_Achievement'
        elif kpi_name == "Retention Rate":
            monthly_data = data_dict['customer'][(data_dict['customer']['BU'] == selected_bu) & 
                                               (data_dict['customer']['Subdivision'] == subdivision)]
            column = 'Retention_Rate'
        elif kpi_name == "Resolution Success":
            monthly_data = data_dict['quality'][(data_dict['quality']['BU'] == selected_bu) & 
                                              (data_dict['quality']['Subdivision'] == subdivision)]
            column = 'Resolution_Success'
        elif kpi_name == "Engagement Score":
            monthly_data = data_dict['employee'][(data_dict['employee']['BU'] == selected_bu) & 
                                               (data_dict['employee']['Subdivision'] == subdivision)]
            column = 'Engagement_Score'
        elif kpi_name == "Training Hours/Emp":
            monthly_data = data_dict['employee'][(data_dict['employee']['BU'] == selected_bu) & 
                                               (data_dict['employee']['Subdivision'] == subdivision)]
            column = 'Training_Hours'
        
        fig = px.line(monthly_data, x='Month', y=column,
                     title=f'{kpi_name} Trend - {subdivision}', 
                     markers=True, height=300)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=14
        )
        return fig
        
    else:
        # Default chart for other KPIs
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3, 4, 5], y=[1, 4, 2, 3, 5], 
                               mode='lines+markers', line_color='#00ff88'))
        fig.update_layout(
            title={'text': f'{kpi_name} - {subdivision}', 'font': {'color': 'white', 'size': 14}}, 
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
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
st.markdown(f"# 📊 {selected_bu} Performance Dashboard")
st.markdown(f"**Selected Period:** {selected_month}")
st.markdown("---")

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
total_target = financial_filtered['Target'].sum()
revenue_vs_target = ((total_revenue / total_target) - 1) * 100 if total_target > 0 else 0
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

# Define KPI mappings
kpi_mappings = {
    'financial': {
        'revenue': ('Revenue', ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']),
        'revenue_target': ('Revenue vs Target', ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']),
        'gross_margin': ('Gross Margin', ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']),
        'cost_project': ('Cost per Project', ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']),
        'ar_days': ('AR Days', ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER'])
    },
    'customer': {
        'csat': ('CSAT', ['PRODEV', 'PD1', 'PD2', 'DOCS']),
        'nps': ('NPS', ['PRODEV', 'PD1', 'PD2', 'DOCS']),
        'sla': ('SLA Achievement', ['PRODEV', 'PD1', 'PD2', 'DOCS']),
        'response_time': ('Avg Response Time', ['PRODEV', 'PD1', 'PD2', 'DOCS']),
        'retention': ('Retention Rate', ['PRODEV', 'PD1', 'PD2', 'DOCS'])
    },
    'quality': {
        'defect_rate': ('Defect Rate', ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS']),
        'uptime': ('System Uptime', ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS']),
        'rework_rate': ('Rework Rate', ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS']),
        'resolution': ('Resolution Success', ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS'])
    },
    'employee': {
        'engagement': ('Engagement Score', ['CHAPTER']),
        'attrition': ('Attrition Rate', ['CHAPTER']),
        'training': ('Training Hours/Emp', ['CHAPTER']),
        'overtime': ('Overtime per FTE', ['CHAPTER'])
    }
}

# 2x2 Grid Layout
col1, col2 = st.columns(2)

with col1:
    # Financial perspective
    st.markdown("### 💰 Financial Performance")
    
    # Financial KPI metrics
    fin_col1, fin_col2, fin_col3 = st.columns(3)
    
    with fin_col1:
        if st.button(f"Revenue\n${total_revenue/1000:.1f}M", key="fin_revenue", help="Click to analyze Revenue"):
            if st.session_state.expanded_kpi.get('financial') == 'revenue':
                st.session_state.expanded_kpi['financial'] = None
            else:
                st.session_state.expanded_kpi['financial'] = 'revenue'
            st.rerun()
    
    with fin_col2:
        if st.button(f"Rev vs Target\n{revenue_vs_target:.1f}%", key="fin_target", help="Click to analyze Revenue vs Target"):
            if st.session_state.expanded_kpi.get('financial') == 'revenue_target':
                st.session_state.expanded_kpi['financial'] = None
            else:
                st.session_state.expanded_kpi['financial'] = 'revenue_target'
            st.rerun()
    
    with fin_col3:
        if st.button(f"Gross Margin\n{avg_gross_margin:.1f}%", key="fin_margin", help="Click to analyze Gross Margin"):
            if st.session_state.expanded_kpi.get('financial') == 'gross_margin':
                st.session_state.expanded_kpi['financial'] = None
            else:
                st.session_state.expanded_kpi['financial'] = 'gross_margin'
            st.rerun()
    
    fin_col4, fin_col5 = st.columns(2)
    
    with fin_col4:
        if st.button(f"Cost/Project\n${avg_cost_per_project:.0f}K", key="fin_cost", help="Click to analyze Cost per Project"):
            if st.session_state.expanded_kpi.get('financial') == 'cost_project':
                st.session_state.expanded_kpi['financial'] = None
            else:
                st.session_state.expanded_kpi['financial'] = 'cost_project'
            st.rerun()
    
    with fin_col5:
        if st.button(f"AR Days\n{avg_ar_days:.0f}", key="fin_ar", help="Click to analyze AR Days"):
            if st.session_state.expanded_kpi.get('financial') == 'ar_days':
                st.session_state.expanded_kpi['financial'] = None
            else:
                st.session_state.expanded_kpi['financial'] = 'ar_days'
            st.rerun()
    
    # Show expanded analysis for Financial
    if st.session_state.expanded_kpi.get('financial'):
        expanded_kpi = st.session_state.expanded_kpi['financial']
        kpi_name, subdivisions = kpi_mappings['financial'][expanded_kpi]
        
        with st.container():
            st.markdown(f"""
                <div class="analysis-container">
                    <h4>📊 {kpi_name} Analysis</h4>
                </div>
            """, unsafe_allow_html=True)
            
            # Subdivision selector
            if len(subdivisions) > 1:
                selected_subdivision = st.selectbox(
                    "Select Subdivision:",
                    subdivisions,
                    key=f"fin_subdiv_{expanded_kpi}"
                )
            else:
                selected_subdivision = subdivisions[0]
                st.info(f"Subdivision: {selected_subdivision}")
            
            # Create and display chart
            try:
                chart = create_chart_for_kpi(kpi_name, selected_subdivision, data, selected_bu, selected_month)
                st.plotly_chart(chart, use_container_width=True, key=f"fin_chart_{expanded_kpi}")
            except Exception as e:
                st.error(f"Error creating chart: {str(e)}")
            
            if st.button("❌ Close Analysis", key=f"close_fin_{expanded_kpi}"):
                st.session_state.expanded_kpi['financial'] = None
                st.rerun()
    
    st.markdown("---")
    
    # Employee perspective
    st.markdown("### 👔 Employee & Learning")
    
    emp_col1, emp_col2 = st.columns(2)
    
    with emp_col1:
        if st.button(f"Engagement\n{avg_engagement:.1f}/10", key="emp_engagement", help="Click to analyze Engagement Score"):
            if st.session_state.expanded_kpi.get('employee') == 'engagement':
                st.session_state.expanded_kpi['employee'] = None
            else:
                st.session_state.expanded_kpi['employee'] = 'engagement'
            st.rerun()
        
        if st.button(f"Training Hrs\n{avg_training:.0f}", key="emp_training", help="Click to analyze Training Hours"):
            if st.session_state.expanded_kpi.get('employee') == 'training':
                st.session_state.expanded_kpi['employee'] = None
            else:
                st.session_state.expanded_kpi['employee'] = 'training'
            st.rerun()
    
    with emp_col2:
        if st.button(f"Attrition\n{avg_attrition:.1f}%", key="emp_attrition", help="Click to analyze Attrition Rate"):
            if st.session_state.expanded_kpi.get('employee') == 'attrition':
                st.session_state.expanded_kpi['employee'] = None
            else:
                st.session_state.expanded_kpi['employee'] = 'attrition'
            st.rerun()
        
        if st.button(f"Overtime\n{avg_overtime:.1f}h", key="emp_overtime", help="Click to analyze Overtime per FTE"):
            if st.session_state.expanded_kpi.get('employee') == 'overtime':
                st.session_state.expanded_kpi['employee'] = None
            else:
                st.session_state.expanded_kpi['employee'] = 'overtime'
            st.rerun()
    
    # Show expanded analysis for Employee
    if st.session_state.expanded_kpi.get('employee'):
        expanded_kpi = st.session_state.expanded_kpi['employee']
        kpi_name, subdivisions = kpi_mappings['employee'][expanded_kpi]
        
        with st.container():
            st.markdown(f"""
                <div class="analysis-container">
                    <h4>📊 {kpi_name} Analysis</h4>
                </div>
            """, unsafe_allow_html=True)
            
            # Subdivision selector
            if len(subdivisions) > 1:
                selected_subdivision = st.selectbox(
                    "Select Subdivision:",
                    subdivisions,
                    key=f"emp_subdiv_{expanded_kpi}"
                )
            else:
                selected_subdivision = subdivisions[0]
                st.info(f"Subdivision: {selected_subdivision}")
            
            # Create and display chart
            try:
                chart = create_chart_for_kpi(kpi_name, selected_subdivision, data, selected_bu, selected_month)
                st.plotly_chart(chart, use_container_width=True, key=f"emp_chart_{expanded_kpi}")
            except Exception as e:
                st.error(f"Error creating chart: {str(e)}")
            
            if st.button("❌ Close Analysis", key=f"close_emp_{expanded_kpi}"):
                st.session_state.expanded_kpi['employee'] = None
                st.rerun()

with col2:
    # Customer & Service perspective
    st.markdown("### 👥 Customer & Service")
    
    cust_col1, cust_col2, cust_col3 = st.columns(3)
    
    with cust_col1:
        if st.button(f"CSAT\n{avg_csat:.1f}/5", key="cust_csat", help="Click to analyze CSAT"):
            if st.session_state.expanded_kpi.get('customer') == 'csat':
                st.session_state.expanded_kpi['customer'] = None
            else:
                st.session_state.expanded_kpi['customer'] = 'csat'
            st.rerun()
    
    with cust_col2:
        if st.button(f"NPS\n+{avg_nps:.0f}", key="cust_nps", help="Click to analyze NPS"):
            if st.session_state.expanded_kpi.get('customer') == 'nps':
                st.session_state.expanded_kpi['customer'] = None
            else:
                st.session_state.expanded_kpi['customer'] = 'nps'
            st.rerun()
    
    with cust_col3:
        if st.button(f"SLA\n{avg_sla:.0f}%", key="cust_sla", help="Click to analyze SLA Achievement"):
            if st.session_state.expanded_kpi.get('customer') == 'sla':
                st.session_state.expanded_kpi['customer'] = None
            else:
                st.session_state.expanded_kpi['customer'] = 'sla'
            st.rerun()
    
    cust_col4, cust_col5 = st.columns(2)
    
    with cust_col4:
        if st.button(f"Response Time\n{avg_response:.1f}h", key="cust_response", help="Click to analyze Response Time"):
            if st.session_state.expanded_kpi.get('customer') == 'response_time':
                st.session_state.expanded_kpi['customer'] = None
            else:
                st.session_state.expanded_kpi['customer'] = 'response_time'
            st.rerun()
    
    with cust_col5:
        if st.button(f"Retention\n{avg_retention:.0f}%", key="cust_retention", help="Click to analyze Retention Rate"):
            if st.session_state.expanded_kpi.get('customer') == 'retention':
                st.session_state.expanded_kpi['customer'] = None
            else:
                st.session_state.expanded_kpi['customer'] = 'retention'
            st.rerun()
    
    # Show expanded analysis for Customer
    if st.session_state.expanded_kpi.get('customer'):
        expanded_kpi = st.session_state.expanded_kpi['customer']
        kpi_name, subdivisions = kpi_mappings['customer'][expanded_kpi]
        
        with st.container():
            st.markdown(f"""
                <div class="analysis-container">
                    <h4>📊 {kpi_name} Analysis</h4>
                </div>
            """, unsafe_allow_html=True)
            
            # Subdivision selector
            if len(subdivisions) > 1:
                selected_subdivision = st.selectbox(
                    "Select Subdivision:",
                    subdivisions,
                    key=f"cust_subdiv_{expanded_kpi}"
                )
            else:
                selected_subdivision = subdivisions[0]
                st.info(f"Subdivision: {selected_subdivision}")
            
            # Create and display chart
            try:
                chart = create_chart_for_kpi(kpi_name, selected_subdivision, data, selected_bu, selected_month)
                st.plotly_chart(chart, use_container_width=True, key=f"cust_chart_{expanded_kpi}")
            except Exception as e:
                st.error(f"Error creating chart: {str(e)}")
            
            if st.button("❌ Close Analysis", key=f"close_cust_{expanded_kpi}"):
                st.session_state.expanded_kpi['customer'] = None
                st.rerun()
    
    st.markdown("---")
    
    # Quality & Process perspective
    st.markdown("### ⚙️ Quality & Process")
    
    qual_col1, qual_col2 = st.columns(2)
    
    with qual_col1:
        if st.button(f"Defect Rate\n{avg_defect_rate:.1f}%", key="qual_defect", help="Click to analyze Defect Rate"):
            if st.session_state.expanded_kpi.get('quality') == 'defect_rate':
                st.session_state.expanded_kpi['quality'] = None
            else:
                st.session_state.expanded_kpi['quality'] = 'defect_rate'
            st.rerun()
        
        if st.button(f"Rework Rate\n{avg_rework:.1f}%", key="qual_rework", help="Click to analyze Rework Rate"):
            if st.session_state.expanded_kpi.get('quality') == 'rework_rate':
                st.session_state.expanded_kpi['quality'] = None
            else:
                st.session_state.expanded_kpi['quality'] = 'rework_rate'
            st.rerun()
    
    with qual_col2:
        if st.button(f"System Uptime\n{avg_uptime:.1f}%", key="qual_uptime", help="Click to analyze System Uptime"):
            if st.session_state.expanded_kpi.get('quality') == 'uptime':
                st.session_state.expanded_kpi['quality'] = None
            else:
                st.session_state.expanded_kpi['quality'] = 'uptime'
            st.rerun()
        
        if st.button(f"Resolution Success\n{avg_resolution:.0f}%", key="qual_resolution", help="Click to analyze Resolution Success"):
            if st.session_state.expanded_kpi.get('quality') == 'resolution':
                st.session_state.expanded_kpi['quality'] = None
            else:
                st.session_state.expanded_kpi['quality'] = 'resolution'
            st.rerun()
    
    # Show expanded analysis for Quality
    if st.session_state.expanded_kpi.get('quality'):
        expanded_kpi = st.session_state.expanded_kpi['quality']
        kpi_name, subdivisions = kpi_mappings['quality'][expanded_kpi]
        
        with st.container():
            st.markdown(f"""
                <div class="analysis-container">
                    <h4>📊 {kpi_name} Analysis</h4>
                </div>
            """, unsafe_allow_html=True)
            
            # Subdivision selector
            if len(subdivisions) > 1:
                selected_subdivision = st.selectbox(
                    "Select Subdivision:",
                    subdivisions,
                    key=f"qual_subdiv_{expanded_kpi}"
                )
            else:
                selected_subdivision = subdivisions[0]
                st.info(f"Subdivision: {selected_subdivision}")
            
            # Create and display chart
            try:
                chart = create_chart_for_kpi(kpi_name, selected_subdivision, data, selected_bu, selected_month)
                st.plotly_chart(chart, use_container_width=True, key=f"qual_chart_{expanded_kpi}")
            except Exception as e:
                st.error(f"Error creating chart: {str(e)}")
            
            if st.button("❌ Close Analysis", key=f"close_qual_{expanded_kpi}"):
                st.session_state.expanded_kpi['quality'] = None
                st.rerun()

# Footer
st.markdown("---")
st.markdown("### 📈 Key Insights & Actions")

# Summary insights based on the data
col_insight1, col_insight2, col_insight3 = st.columns(3)

with col_insight1:
    st.markdown("""
    **💰 Financial Health**
    - Revenue tracking vs targets
    - Margin optimization opportunities
    - Cost control measures
    """)

with col_insight2:
    st.markdown("""
    **👥 Customer Excellence**
    - High satisfaction scores
    - Strong retention rates
    - Quick response times
    """)

with col_insight3:
    st.markdown("""
    **⚙️ Operational Excellence**
    - Quality metrics monitoring
    - Process improvements
    - System reliability focus
    """)
