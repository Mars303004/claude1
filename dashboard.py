import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    .stButton>button {
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.15) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        padding: 0.5rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
        background: rgba(255,255,255,0.25) !important;
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
    .positive {
        color: #00ff88 !important;
    }
    .negative {
        color: #ff6b6b !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_kpi' not in st.session_state:
    st.session_state.selected_kpi = None

# Data Generation
@st.cache_data
def generate_dummy_data():
    """Generate comprehensive dummy data for the dashboard"""
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    bus = ['BU1', 'BU2', 'BU3']
    
    data = {
        'financial': pd.DataFrame(),
        'customer': pd.DataFrame(),
        'quality': pd.DataFrame(),
        'employee': pd.DataFrame()
    }
    
    # Financial Data
    financial_data = []
    for bu in bus:
        for month in months:
            for subdiv in ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']:
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
    data['financial'] = pd.DataFrame(financial_data)
    
    # Customer Data
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
                    'Avg_Response_Time': random.uniform(1.5, 4.0)
                })
    data['customer'] = pd.DataFrame(customer_data)
    
    # Quality Data
    quality_data = []
    for bu in bus:
        for month in months:
            for subdiv in ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS']:
                quality_data.append({
                    'BU': bu,
                    'Month': month,
                    'Subdivision': subdiv,
                    'Defect_Rate': random.uniform(0.5, 3.0),
                    'System_Uptime': random.uniform(98.5, 99.9),
                    'Rework_Rate': random.uniform(2.0, 8.0)
                })
    data['quality'] = pd.DataFrame(quality_data)
    
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
                'Training_Hours': random.randint(35, 55)
            })
    data['employee'] = pd.DataFrame(employee_data)
    
    return data

# KPI Card Component
def create_kpi_card(title, value, change, unit="", kpi_id="", is_inverse=False):
    change_class = "positive" if (change > 0 and not is_inverse) or (change < 0 and is_inverse) else "negative"
    sign = "+" if change > 0 else ""
    
    return st.button(
        f"**{title}**  \n{value}{unit}  \n`{sign}{change:.1f}%` vs LY",
        key=f"btn_{kpi_id}",
        on_click=lambda: st.session_state.update(selected_kpi=kpi_id),
    )

def create_perspective_box(title, icon, *kpi_cards):
    return f"""
    <div class="perspective-box">
        <div class="perspective-title">{icon} {title}</div>
        <div class="kpi-grid">
            {"".join([f'<div class="kpi-item">{card}</div>' for card in kpi_cards])}
        </div>
    </div>
    """

# Chart Creation
def create_chart_for_kpi(kpi_name, subdivision, data_dict, selected_bu, selected_month):
    try:
        if kpi_name == "Revenue":
            df = data_dict['financial']
            filtered = df[(df['BU'] == selected_bu) & (df['Subdivision'] == subdivision)]
            fig = px.line(filtered, x='Month', y='Revenue', title=f'Revenue Trend - {subdivision}')
        
        elif kpi_name == "CSAT":
            df = data_dict['customer']
            filtered = df[(df['BU'] == selected_bu) & (df['Subdivision'] == subdivision)]
            fig = px.bar(filtered, x='Month', y='CSAT', title=f'CSAT Trend - {subdivision}')
        
        elif kpi_name == "Defect Rate":
            df = data_dict['quality']
            filtered = df[(df['BU'] == selected_bu) & (df['Subdivision'] == subdivision)]
            fig = px.area(filtered, x='Month', y='Defect_Rate', title=f'Defect Rate Trend - {subdivision}')
        
        else:
            fig = px.scatter(title="Default Chart")
        
        fig.update_layout(height=400, margin=dict(t=40, b=20, l=20, r=20))
        return fig
    
    except Exception as e:
        return px.scatter(title="Data Not Available")

# KPI Mapping
kpi_mapping = {
    'revenue': {'name': 'Revenue', 'subdivisions': ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']},
    'csat': {'name': 'CSAT', 'subdivisions': ['PRODEV', 'PD1', 'PD2', 'DOCS']},
    'defect_rate': {'name': 'Defect Rate', 'subdivisions': ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS']},
    'engagement': {'name': 'Engagement Score', 'subdivisions': ['CHAPTER']}
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
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# Main Content
st.markdown(f"# 📊 {selected_bu} Performance")
st.markdown(f"**Selected Period:** {selected_month}")

# KPI Boxes
col1, col2 = st.columns(2)

with col1:
    # Financial Perspective
    with st.container():
        st.markdown(create_perspective_box(
            "Financial", "💰",
            create_kpi_card("Revenue", "$1.5", 8.5, "M", "revenue"),
            create_kpi_card("Target", "98%", 2.3, "", "revenue_target"),
            create_kpi_card("Margin", "32%", 1.2, "", "gross_margin"),
            create_kpi_card("Cost", "$450K", -1.5, "", "cost_project", True),
            create_kpi_card("AR Days", "35", -2.1, "", "ar_days", True)
        ), unsafe_allow_html=True)

# Quality Perspective
    quality_box = create_perspective_box(
        "Quality", "🛠️",
        create_kpi_card("Defect", "1.2%", -0.8, "", "defect_rate", True),
        create_kpi_card("Uptime", "99.8%", 0.2, "", "uptime"),
        create_kpi_card("Rework", "3.1%", -1.2, "", "rework_rate", True),
        create_kpi_card("Resolution", "97%", 2.5, "", "resolution")
    )
    st.markdown(quality_box, unsafe_allow_html=True)

with col2:
    # Customer Perspective
    customer_box = create_perspective_box(
        "Customer", "👥",
        create_kpi_card("CSAT", "4.2", 1.5, "/5", "csat"),
        create_kpi_card("NPS", "+48", 3.2, "", "nps"),
        create_kpi_card("SLA", "95%", 1.8, "", "sla"),
        create_kpi_card("Response", "2.4h", -2.3, "", "response_time", True),
        create_kpi_card("Retention", "92%", -0.7, "", "retention")
    )
    st.markdown(customer_box, unsafe_allow_html=True)
    
    # Employee Perspective
    employee_box = create_perspective_box(
        "Employee", "👔",
        create_kpi_card("Engagement", "8.1", 0.6, "/10", "engagement"),
        create_kpi_card("Attrition", "9.2%", -1.4, "", "attrition", True),
        create_kpi_card("Training", "45h", 5.2, "", "training"),
        create_kpi_card("Overtime", "3.2h", 0.9, "", "overtime")
    )
    st.markdown(employee_box, unsafe_allow_html=True)

# Expander Section
if st.session_state.selected_kpi:
    kpi_info = kpi_mapping.get(st.session_state.selected_kpi)
    if kpi_info:
        with st.expander(f"📈 {kpi_info['name']} Analysis", expanded=True):
            selected_subdivision = st.selectbox(
                "Select Subdivision:",
                kpi_info['subdivisions'],
                key="subdiv_select"
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
📊 IT Company Performance Dashboard | Real-time Data | v1.0
</div>
""", unsafe_allow_html=True)
