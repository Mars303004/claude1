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

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .positive-change {
        color: #00C851 !important;
        font-weight: bold;
    }
    .negative-change {
        color: #FF4444 !important;
        font-weight: bold;
    }
    .neutral-change {
        color: #33b5e5 !important;
        font-weight: bold;
    }
    .section-header {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 8px 16px;
    }
</style>
""", unsafe_allow_html=True)

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
            subdivs = ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS'] if random.choice([True, False]) else ['PRODEV', 'PD1', 'PD2', 'DOCS']
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

def format_change(value, is_inverse=False):
    """Format change values with proper colors"""
    if value == 0:
        return f'<span class="neutral-change">0%</span>'
    
    if is_inverse:  # For metrics where lower is better (like AR Days, Defect Rate)
        color_class = "positive-change" if value < 0 else "negative-change"
    else:  # For metrics where higher is better
        color_class = "positive-change" if value > 0 else "negative-change"
    
    sign = "+" if value > 0 else ""
    return f'<span class="{color_class}">{sign}{value:.1f}% vs LY</span>'

def create_kpi_card(title, value, change=None, unit="", is_inverse=False):
    """Create a styled KPI card"""
    change_html = ""
    if change is not None:
        change_html = f"<br>{format_change(change, is_inverse)}"
    
    return f"""
    <div class="metric-card">
        <h4 style="margin: 0; font-size: 14px; opacity: 0.9;">{title}</h4>
        <h2 style="margin: 5px 0; font-size: 28px;">{value}{unit}</h2>
        {change_html}
    </div>
    """

def create_radar_chart(data, categories, values, title):
    """Create a radar chart for performance overview"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Performance',
        line_color='#4f46e5',
        fillcolor='rgba(79, 70, 229, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=False,
        title=title,
        height=300,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    
    return fig

# Load data
data = generate_dummy_data()

# Sidebar
st.sidebar.markdown("## 🎛️ IT Company Dashboard")

# Month selection
selected_month = st.sidebar.selectbox(
    "📅 Select Month",
    ['January', 'February', 'March', 'April', 'May', 'June'],
    index=0
)

# Business Unit selection
selected_bu = st.sidebar.radio(
    "🏢 Select Business Unit",
    ['BU1', 'BU2', 'BU3'],
    index=0
)

# Refresh button
if st.sidebar.button("🔄 Refresh Data", type="primary"):
    st.cache_data.clear()
    st.rerun()

# Advanced Dashboard button
st.sidebar.markdown("---")
if st.sidebar.button("➡️ Go to Advanced Dashboard", type="secondary"):
    st.info("Advanced Dashboard would open here!")

# Main Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title(f"📊 {selected_bu} Performance")
with col2:
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

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Financial Section
    st.markdown('<div class="section-header"><h3>💰 Financial</h3></div>', unsafe_allow_html=True)
    
    # Financial KPIs
    fin_cols = st.columns(5)
    
    total_revenue = financial_filtered['Revenue'].sum()
    revenue_vs_target = ((total_revenue / financial_filtered['Target'].sum()) - 1) * 100
    avg_gross_margin = financial_filtered['Gross_Margin'].mean()
    avg_cost_per_project = financial_filtered['Cost_per_Project'].mean()
    avg_ar_days = financial_filtered['AR_Days'].mean()
    
    with fin_cols[0]:
        st.markdown(create_kpi_card("Revenue", f"${total_revenue/1000:.1f}", 12.5, "M"), unsafe_allow_html=True)
    
    with fin_cols[1]:
        st.markdown(create_kpi_card("Revenue vs Target", f"{revenue_vs_target:.0f}", -3.0, "%"), unsafe_allow_html=True)
    
    with fin_cols[2]:
        st.markdown(create_kpi_card("Gross Margin", f"{avg_gross_margin:.0f}", 3.2, "%"), unsafe_allow_html=True)
    
    with fin_cols[3]:
        st.markdown(create_kpi_card("Cost per Project", f"${avg_cost_per_project:.0f}", 5.1, "K"), unsafe_allow_html=True)
    
    with fin_cols[4]:
        st.markdown(create_kpi_card("AR Days", f"{avg_ar_days:.0f}", -3.0, "", True), unsafe_allow_html=True)
    
    # Revenue by Subdivision Chart
    st.subheader("Revenue by Subdivision")
    revenue_chart = px.bar(
        financial_filtered,
        x='Subdivision',
        y='Revenue',
        color='Subdivision',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    revenue_chart.update_layout(height=250, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(revenue_chart, use_container_width=True)
    
    # Customer & Service Section
    st.markdown('<div class="section-header"><h3>👥 Customer & Service</h3></div>', unsafe_allow_html=True)
    
    # Customer KPIs
    cust_cols = st.columns(5)
    
    avg_csat = customer_filtered['CSAT'].mean()
    avg_nps = customer_filtered['NPS'].mean()
    avg_sla = customer_filtered['SLA_Achievement'].mean()
    avg_response = customer_filtered['Avg_Response_Time'].mean()
    avg_retention = customer_filtered['Retention_Rate'].mean()
    
    with cust_cols[0]:
        st.markdown(create_kpi_card("CSAT", f"{avg_csat:.1f}", 2.3, "/5"), unsafe_allow_html=True)
    
    with cust_cols[1]:
        st.markdown(create_kpi_card("NPS", f"+{avg_nps:.0f}", 4.2), unsafe_allow_html=True)
    
    with cust_cols[2]:
        st.markdown(create_kpi_card("SLA Achievement", f"{avg_sla:.0f}", 2.1, "%"), unsafe_allow_html=True)
    
    with cust_cols[3]:
        st.markdown(create_kpi_card("Avg Response Time", f"{avg_response:.1f}", -3.2, "h", True), unsafe_allow_html=True)
    
    with cust_cols[4]:
        st.markdown(create_kpi_card("Retention Rate", f"{avg_retention:.0f}", -2.1, "%"), unsafe_allow_html=True)
    
    # Customer Satisfaction Trends
    st.subheader("Customer Satisfaction Trends")
    
    # Generate trend data for the chart
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    csat_trend = [4.1, 4.2, 4.15, 4.25, 4.3, avg_csat]
    nps_trend = [38, 40, 42, 45, 43, avg_nps]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=months, y=csat_trend, name="CSAT", line=dict(color='#00C851', width=3)),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=months, y=nps_trend, name="NPS", line=dict(color='#33b5e5', width=3)),
        secondary_y=True,
    )
    
    fig.update_yaxes(title_text="CSAT (Scale 1-5)", secondary_y=False)
    fig.update_yaxes(title_text="NPS", secondary_y=True)
    fig.update_layout(height=250, margin=dict(t=20, b=20, l=20, r=20))
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Performance Overview Radar Chart
    st.markdown('<div class="section-header"><h3>📈 Performance Overview</h3></div>', unsafe_allow_html=True)
    
    # Calculate performance scores
    perf_categories = ['Employee Engagement', 'Client Margin', 'Quality (Low Defects)', 'CSAT', 'SLA Achievement']
    
    # Normalize values to 0-5 scale
    engagement_score = employee_filtered['Engagement_Score'].mean() * 0.6 if not employee_filtered.empty else 4.2
    margin_score = (avg_gross_margin / 10) if not financial_filtered.empty else 3.8
    quality_score = 5 - (quality_filtered['Defect_Rate'].mean() if not quality_filtered.empty else 1.2)
    csat_score = avg_csat if not customer_filtered.empty else 4.1
    sla_score = (avg_sla / 20) if not customer_filtered.empty else 4.5
    
    perf_values = [engagement_score, margin_score, quality_score, csat_score, sla_score]
    
    radar_fig = create_radar_chart(None, perf_categories, perf_values, "")
    st.plotly_chart(radar_fig, use_container_width=True)
    
    # Quality Metrics
    st.markdown('<div class="section-header"><h3>🛠️ Quality Metrics</h3></div>', unsafe_allow_html=True)
    
    if not quality_filtered.empty:
        avg_defect_rate = quality_filtered['Defect_Rate'].mean()
        avg_uptime = quality_filtered['System_Uptime'].mean()
        avg_rework = quality_filtered['Rework_Rate'].mean()
        avg_resolution = quality_filtered['Resolution_Success'].mean()
    else:
        avg_defect_rate, avg_uptime, avg_rework, avg_resolution = 1.2, 99.95, 3.8, 97.2
    
    st.markdown(create_kpi_card("Defect Rate", f"{avg_defect_rate:.1f}", -0.3, "%", True), unsafe_allow_html=True)
    st.markdown(create_kpi_card("System Uptime", f"{avg_uptime:.2f}", 0.1, "%"), unsafe_allow_html=True)
    st.markdown(create_kpi_card("Rework Rate", f"{avg_rework:.1f}", -0.5, "%", True), unsafe_allow_html=True)
    st.markdown(create_kpi_card("Resolution Success", f"{avg_resolution:.1f}", 1.2, "%"), unsafe_allow_html=True)
    
    # Employee Fulfillment
    st.markdown('<div class="section-header"><h3>👔 Employee Fulfillment</h3></div>', unsafe_allow_html=True)
    
    if not employee_filtered.empty:
        avg_engagement = employee_filtered['Engagement_Score'].mean()
        avg_attrition = employee_filtered['Attrition_Rate'].mean()
        avg_training = employee_filtered['Training_Hours'].mean()
        avg_overtime = employee_filtered['Overtime_per_FTE'].mean()
    else:
        avg_engagement, avg_attrition, avg_training, avg_overtime = 7.8, 8.2, 42, 3.2
    
    st.markdown(create_kpi_card("Engagement Score", f"{avg_engagement:.1f}", 0.4, "/10"), unsafe_allow_html=True)
    st.markdown(create_kpi_card("Attrition Rate", f"{avg_attrition:.1f}", -1.1, "%", True), unsafe_allow_html=True)
    st.markdown(create_kpi_card("Training Hours/Emp", f"{avg_training:.0f}", 5.0), unsafe_allow_html=True)
    st.markdown(create_kpi_card("Overtime per FTE", f"{avg_overtime:.1f}", 0.5, "h"), unsafe_allow_html=True)

# Interactive KPI Details Section
st.markdown("---")
st.markdown('<div class="section-header"><h3>🔍 Detailed Analysis</h3></div>', unsafe_allow_html=True)

# Tabs for different perspectives
tab1, tab2, tab3, tab4 = st.tabs(["💰 Financial Details", "👥 Customer Details", "🛠️ Quality Details", "👔 Employee Details"])

with tab1:
    if not financial_filtered.empty:
        st.markdown("**Subdivision Performance:**")
        
        subdivision_tabs = st.tabs(financial_filtered['Subdivision'].unique().tolist())
        
        for i, subdiv in enumerate(financial_filtered['Subdivision'].unique()):
            with subdivision_tabs[i]:
                subdiv_data = financial_filtered[financial_filtered['Subdivision'] == subdiv]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Revenue", f"${subdiv_data['Revenue'].iloc[0]/1000:.1f}M")
                with col2:
                    target_pct = (subdiv_data['Revenue'].iloc[0] / subdiv_data['Target'].iloc[0]) * 100
                    st.metric("vs Target", f"{target_pct:.1f}%")
                with col3:
                    st.metric("Gross Margin", f"{subdiv_data['Gross_Margin'].iloc[0]:.1f}%")

with tab2:
    if not customer_filtered.empty:
        st.markdown("**Customer Metrics by Subdivision:**")
        
        subdivision_tabs = st.tabs(customer_filtered['Subdivision'].unique().tolist())
        
        for i, subdiv in enumerate(customer_filtered['Subdivision'].unique()):
            with subdivision_tabs[i]:
                subdiv_data = customer_filtered[customer_filtered['Subdivision'] == subdiv]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("CSAT", f"{subdiv_data['CSAT'].iloc[0]:.2f}/5")
                with col2:
                    st.metric("NPS", f"+{subdiv_data['NPS'].iloc[0]:.0f}")
                with col3:
                    st.metric("SLA Achievement", f"{subdiv_data['SLA_Achievement'].iloc[0]:.1f}%")

with tab3:
    if not quality_filtered.empty:
        st.markdown("**Quality Metrics by Subdivision:**")
        
        subdivision_tabs = st.tabs(quality_filtered['Subdivision'].unique().tolist())
        
        for i, subdiv in enumerate(quality_filtered['Subdivision'].unique()):
            with subdivision_tabs[i]:
                subdiv_data = quality_filtered[quality_filtered['Subdivision'] == subdiv]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Defect Rate", f"{subdiv_data['Defect_Rate'].iloc[0]:.2f}%")
                with col2:
                    st.metric("System Uptime", f"{subdiv_data['System_Uptime'].iloc[0]:.2f}%")
                with col3:
                    st.metric("Resolution Success", f"{subdiv_data['Resolution_Success'].iloc[0]:.1f}%")

with tab4:
    if not employee_filtered.empty:
        st.markdown("**Employee Metrics (CHAPTER):**")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Engagement", f"{employee_filtered['Engagement_Score'].iloc[0]:.1f}/10")
        with col2:
            st.metric("Attrition Rate", f"{employee_filtered['Attrition_Rate'].iloc[0]:.1f}%")
        with col3:
            st.metric("Training Hours", f"{employee_filtered['Training_Hours'].iloc[0]:.0f}")
        with col4:
            st.metric("Overtime/FTE", f"{employee_filtered['Overtime_per_FTE'].iloc[0]:.1f}h")

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
