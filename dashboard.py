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
        min-height: 280px;
        overflow: visible;
        transition: all 0.3s ease;
    }
    .perspective-box.expanded {
        min-height: 600px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%, #445587 100%);
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
        margin-bottom: 1rem;
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
    .kpi-card.selected {
        background: rgba(255,255,255,0.3);
        border: 2px solid rgba(255,255,255,0.8);
        transform: scale(1.05);
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
    .kpi-details {
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.2);
        animation: slideDown 0.3s ease-out;
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
    .subdivision-tabs {
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    .subdivision-tab {
        padding: 0.4rem 0.8rem;
        background: rgba(255,255,255,0.2);
        border-radius: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 11px;
        color: white;
        border: 1px solid rgba(255,255,255,0.3);
    }
    .subdivision-tab.active {
        background: rgba(255,255,255,0.4);
        border: 1px solid rgba(255,255,255,0.6);
        font-weight: bold;
    }
    .subdivision-tab:hover {
        background: rgba(255,255,255,0.3);
    }
    .close-details {
        position: absolute;
        top: 10px;
        right: 15px;
        background: rgba(255,255,255,0.2);
        border: none;
        color: white;
        cursor: pointer;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .close-details:hover {
        background: rgba(255,255,255,0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for KPI expansion
if 'expanded_kpi' not in st.session_state:
    st.session_state.expanded_kpi = {}
if 'selected_subdivision' not in st.session_state:
    st.session_state.selected_subdivision = {}

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

def create_kpi_card_html(title, value, change, unit="", kpi_id="", is_inverse=False, is_selected=False):
    """Create HTML for KPI card with click handler"""
    change_class = "positive-change" if (change > 0 and not is_inverse) or (change < 0 and is_inverse) else "negative-change"
    sign = "+" if change > 0 else ""
    selected_class = "selected" if is_selected else ""
    
    return f"""
    <div class="kpi-card {selected_class}" data-kpi="{kpi_id}">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}{unit}</div>
        <div class="kpi-change {change_class}">{sign}{change:.1f}% vs LY</div>
    </div>
    """

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

def create_kpi_details_section(kpi_name, subdivisions, data_dict, selected_bu, selected_month, perspective_key):
    """Create the details section for expanded KPI"""
    
    # Get or set default subdivision
    subdivision_key = f"{perspective_key}_{kpi_name}"
    if subdivision_key not in st.session_state.selected_subdivision:
        st.session_state.selected_subdivision[subdivision_key] = subdivisions[0]
    
    details_html = f"""
    <div class="kpi-details">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: white;">📊 {kpi_name} Analysis</h4>
        </div>
    """
    
    # Add subdivision tabs if more than one
    if len(subdivisions) > 1:
        tabs_html = '<div class="subdivision-tabs">'
        for subdiv in subdivisions:
            active_class = "active" if subdiv == st.session_state.selected_subdivision[subdivision_key] else ""
            tabs_html += f'<div class="subdivision-tab {active_class}" data-subdivision="{subdiv}">{subdiv}</div>'
        tabs_html += '</div>'
        details_html += tabs_html
    
    details_html += '<div id="chart-container"></div></div>'
    
    return details_html

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
    st.markdown("### 💰 Financial")
    
    # Create buttons for financial KPIs
    fin_cols = st.columns(5)
    financial_kpis = ['revenue', 'revenue_target', 'gross_margin', 'cost_project', 'ar_days']
    financial_values = [f"${total_revenue/1000:.1f}M", f"{revenue_vs_target:.0f}%", f"{avg_gross_margin:.0f}%", f"${avg_cost_per_project:.0f}K", f"{avg_ar_days:.0f}"]
    financial_changes = [12.5, -3.0, 3.2, 5.1, -3.0]
    
    for i, (kpi_id, value, change) in enumerate(zip(financial_kpis, financial_values, financial_changes)):
        with fin_cols[i]:
            kpi_name, subdivisions = kpi_mappings['financial'][kpi_id]
            if st.button(f"{kpi_name}\n{value}", key=f"fin_{kpi_id}", help=f"Click to analyze {kpi_name}"):
                # Toggle expansion
                if st.session_state.expanded_kpi.get('financial') == kpi_id:
                    st.session_state.expanded_kpi['financial'] = None
                else:
                    st.session_state.expanded_kpi['financial'] = kpi_id
                st.rerun()
    
    # Show details if expanded
    if st.session_state.expanded_kpi.get('customer'):
        expanded_kpi = st.session_state.expanded_kpi['customer']
        kpi_name, subdivisions = kpi_mappings['customer'][expanded_kpi]
        
        st.markdown("---")
        st.markdown(f"#### 📊 {kpi_name} Analysis")
        
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
        
        if st.button("❌ Close", key=f"close_cust_{expanded_kpi}"):
            st.session_state.expanded_kpi['customer'] = None
            st.rerun()
    
    st.markdown("---")
    
    # Employee perspective
    st.markdown("### 👔 Employee Fulfillment")
    
    # Create buttons for employee KPIs
    emp_cols = st.columns(4)
    employee_kpis = ['engagement', 'attrition', 'training', 'overtime']
    employee_values = [f"{avg_engagement:.1f}/10", f"{avg_attrition:.1f}%", f"{avg_training:.0f}", f"{avg_overtime:.1f}h"]
    employee_changes = [0.4, -1.1, 5.0, 0.5]
    
    for i, (kpi_id, value, change) in enumerate(zip(employee_kpis, employee_values, employee_changes)):
        with emp_cols[i]:
            kpi_name, subdivisions = kpi_mappings['employee'][kpi_id]
            if st.button(f"{kpi_name}\n{value}", key=f"emp_{kpi_id}", help=f"Click to analyze {kpi_name}"):
                # Toggle expansion
                if st.session_state.expanded_kpi.get('employee') == kpi_id:
                    st.session_state.expanded_kpi['employee'] = None
                else:
                    st.session_state.expanded_kpi['employee'] = kpi_id
                st.rerun()
    
    # Show details if expanded
    if st.session_state.expanded_kpi.get('employee'):
        expanded_kpi = st.session_state.expanded_kpi['employee']
        kpi_name, subdivisions = kpi_mappings['employee'][expanded_kpi]
        
        st.markdown("---")
        st.markdown(f"#### 📊 {kpi_name} Analysis")
        
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
        
        if st.button("❌ Close", key=f"close_emp_{expanded_kpi}"):
            st.session_state.expanded_kpi['employee'] = None
            st.rerun()

# Clear all expansions button
st.markdown("---")
col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
with col_clear2:
    if st.button("🔄 Clear All Expansions", type="secondary", help="Close all expanded KPI details"):
        st.session_state.expanded_kpi = {}
        st.rerun()

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
)()
    
    # Show details if expanded
    if st.session_state.expanded_kpi.get('financial'):
        expanded_kpi = st.session_state.expanded_kpi['financial']
        kpi_name, subdivisions = kpi_mappings['financial'][expanded_kpi]
        
        st.markdown("---")
        st.markdown(f"#### 📊 {kpi_name} Analysis")
        
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
        
        if st.button("❌ Close", key=f"close_fin_{expanded_kpi}"):
            st.session_state.expanded_kpi['financial'] = None
            st.rerun()
    
    st.markdown("---")
    
    # Quality perspective
    st.markdown("### 🛠️ Quality Metrics")
    
    # Create buttons for quality KPIs
    qual_cols = st.columns(4)
    quality_kpis = ['defect_rate', 'uptime', 'rework_rate', 'resolution']
    quality_values = [f"{avg_defect_rate:.1f}%", f"{avg_uptime:.2f}%", f"{avg_rework:.1f}%", f"{avg_resolution:.1f}%"]
    quality_changes = [-0.3, 0.1, -0.5, 1.2]
    
    for i, (kpi_id, value, change) in enumerate(zip(quality_kpis, quality_values, quality_changes)):
        with qual_cols[i]:
            kpi_name, subdivisions = kpi_mappings['quality'][kpi_id]
            if st.button(f"{kpi_name}\n{value}", key=f"qual_{kpi_id}", help=f"Click to analyze {kpi_name}"):
                # Toggle expansion
                if st.session_state.expanded_kpi.get('quality') == kpi_id:
                    st.session_state.expanded_kpi['quality'] = None
                else:
                    st.session_state.expanded_kpi['quality'] = kpi_id
                st.rerun()
    
    # Show details if expanded
    if st.session_state.expanded_kpi.get('quality'):
        expanded_kpi = st.session_state.expanded_kpi['quality']
        kpi_name, subdivisions = kpi_mappings['quality'][expanded_kpi]
        
        st.markdown("---")
        st.markdown(f"#### 📊 {kpi_name} Analysis")
        
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
        
        if st.button("❌ Close", key=f"close_qual_{expanded_kpi}"):
            st.session_state.expanded_kpi['quality'] = None
            st.rerun()

with col2:
    # Customer & Service perspective
    st.markdown("### 👥 Customer & Service")
    
    # Create buttons for customer KPIs
    cust_cols = st.columns(5)
    customer_kpis = ['csat', 'nps', 'sla', 'response_time', 'retention']
    customer_values = [f"{avg_csat:.1f}/5", f"+{avg_nps:.0f}", f"{avg_sla:.0f}%", f"{avg_response:.1f}h", f"{avg_retention:.0f}%"]
    customer_changes = [2.3, 4.2, 2.1, -3.2, -2.1]
    
    for i, (kpi_id, value, change) in enumerate(zip(customer_kpis, customer_values, customer_changes)):
        with cust_cols[i]:
            kpi_name, subdivisions = kpi_mappings['customer'][kpi_id]
            if st.button(f"{kpi_name}\n{value}", key=f"cust_{kpi_id}", help=f"Click to analyze {kpi_name}"):
                # Toggle expansion
                if st.session_state.expanded_kpi.get('customer') == kpi_id:
                    st.session_state.expanded_kpi['customer'] = None
                else:
                    st.session_state.expanded_kpi['customer'] = kpi_id
                st.rerun
