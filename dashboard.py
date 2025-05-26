import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(
    page_title="KPI Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'selected_bu' not in st.session_state:
    st.session_state.selected_bu = 'BU1'
if 'selected_month' not in st.session_state:
    st.session_state.selected_month = 'January'

# Sample data structure for KPIs
def generate_kpi_data():
    """Generate sample KPI data for different BUs and subdivisions"""
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    bus = ['BU1', 'BU2', 'BU3']
    subdivisions = ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']
    kpi_data = {}
    for bu in bus:
        kpi_data[bu] = {}
        for month in months:
            kpi_data[bu][month] = {
                'Financial': {
                    'Revenue': {
                        'value': random.randint(25, 45) / 10,  # 2.5M - 4.5M
                        'unit': 'M',
                        'change': random.randint(-15, 25),
                        'subdivisions': {sub: random.randint(20, 80) for sub in subdivisions}
                    },
                    'Revenue vs Target': {
                        'value': random.randint(85, 105),
                        'unit': '%',
                        'change': random.randint(-5, 15),
                        'target': 100
                    },
                    'Gross Margin': {
                        'value': random.randint(30, 45),
                        'unit': '%',
                        'change': random.randint(-8, 12)
                    },
                    'Cost per Project': {
                        'value': random.randint(35, 55),
                        'unit': 'K',
                        'change': random.randint(-20, 10)
                    },
                    'AR Days': {
                        'value': random.randint(25, 40),
                        'unit': 'days',
                        'change': random.randint(-10, 15)
                    }
                },
                'Customer & Service': {
                    'CSAT': {
                        'value': random.randint(40, 48) / 10,  # 4.0 - 4.8
                        'unit': '/5',
                        'change': random.randint(-5, 15),
                        'subdivisions': {sub: random.randint(35, 50) / 10 for sub in subdivisions}
                    },
                    'NPS': {
                        'value': random.randint(35, 55),
                        'unit': '',
                        'change': random.randint(-10, 20)
                    },
                    'SLA Achievement': {
                        'value': random.randint(85, 98),
                        'unit': '%',
                        'change': random.randint(-5, 10)
                    },
                    'Avg Response Time': {
                        'value': random.randint(18, 30) / 10,  # 1.8h - 3.0h
                        'unit': 'h',
                        'change': random.randint(-25, 5)
                    },
                    'Retention Rate': {
                        'value': random.randint(88, 96),
                        'unit': '%',
                        'change': random.randint(-3, 8)
                    }
                },
                'Quality Metrics': {
                    'System Uptime': {
                        'value': random.randint(9950, 9999) / 100,  # 99.50% - 99.99%
                        'unit': '%',
                        'change': random.randint(-2, 5),
                        'subdivisions': {sub: random.randint(9900, 9999) / 100 for sub in subdivisions}
                    },
                    'Defect Rate': {
                        'value': random.randint(8, 18) / 10,  # 0.8% - 1.8%
                        'unit': '%',
                        'change': random.randint(-30, 10)
                    },
                    'Rework Rate': {
                        'value': random.randint(25, 45) / 10,  # 2.5% - 4.5%
                        'unit': '%',
                        'change': random.randint(-20, 15)
                    },
                    'Resolution Success': {
                        'value': random.randint(94, 99),
                        'unit': '%',
                        'change': random.randint(-3, 8)
                    },
                    'Code Review Coverage': {
                        'value': random.randint(85, 95),
                        'unit': '%',
                        'change': random.randint(-5, 10)
                    }
                },
                'Employee Fulfillment': {
                    'Engagement Score': {
                        'value': random.randint(70, 85) / 10,  # 7.0 - 8.5
                        'unit': '/10',
                        'change': random.randint(-8, 15),
                        'subdivisions': {sub: random.randint(65, 90) / 10 for sub in subdivisions}
                    },
                    'Attrition Rate': {
                        'value': random.randint(6, 12),
                        'unit': '%',
                        'change': random.randint(-20, 10)
                    },
                    'Training Hours': {
                        'value': random.randint(35, 55),
                        'unit': 'hrs',
                        'change': random.randint(-10, 25)
                    },
                    'Overtime per FTE': {
                        'value': random.randint(25, 40) / 10,  # 2.5h - 4.0h
                        'unit': 'h',
                        'change': random.randint(-15, 20)
                    },
                    'Internal Promotion Rate': {
                        'value': random.randint(8, 15),
                        'unit': '%',
                        'change': random.randint(-5, 20)
                    }
                }
            }
    return kpi_data

# Generate data
kpi_data = generate_kpi_data()

def create_kpi_metric(title, value, unit, change, icon="📊"):
    """Create a clean KPI metric display using Streamlit native components"""
    higher_better = [
        "Revenue", "Revenue vs Target", "Gross Margin", "CSAT", "NPS", "SLA Achievement",
        "Retention Rate", "System Uptime", "Resolution Success", "Code Review Coverage",
        "Engagement Score", "Training Hours/Emp", "Internal Promotion Rate"
    ]
    lower_better = [
        "Cost per Project", "AR Days", "Avg Response Time", "Defect Rate", "Rework Rate",
        "Attrition Rate", "Overtime per FTE"
    ]

    # Format the value display
    if isinstance(value, float):
        if unit in ['M', 'K']:
            display_value = f"${value:.1f}{unit}"
        elif unit == '%':
            display_value = f"{value:.1f}%"
        elif unit == '/5':
            display_value = f"{value:.1f}/5"
        elif unit == '/10':
            display_value = f"{value:.1f}/10"
        elif unit == 'h':
            display_value = f"{value:.1f}h"
        else:
            display_value = f"{value:.1f}{unit}"
    else:
        display_value = f"{value}{unit}"

    # Determine delta color based on KPI type
    if title in higher_better:
        if change > 0:
            delta_color = "normal"
        elif change < 0:
            delta_color = "inverse"
        else:
            delta_color = "off"
    elif title in lower_better:
        if change > 0:
            delta_color = "inverse"
        elif change < 0:
            delta_color = "normal"
        else:
            delta_color = "off"
    else:
        delta_color = "off"

    change_str = f"{change:+}%"

    # Use Streamlit's metric component
    st.metric(
        label=f"{icon} {title}",
        value=display_value,
        delta=change_str,
        delta_color=delta_color
    )

def create_subdivision_chart(kpi_name, subdivision_data, chart_type="bar"):
    """Create charts for subdivision data"""
    subdivisions = list(subdivision_data.keys())
    values = list(subdivision_data.values())
    if chart_type == "bar":
        fig = px.bar(
            x=subdivisions,
            y=values,
            title=f"{kpi_name} by Subdivision",
            color=values,
            color_continuous_scale="Blues"
        )
    elif chart_type == "pie":
        fig = px.pie(
            values=values,
            names=subdivisions,
            title=f"{kpi_name} Distribution by Subdivision"
        )
    else:  # line chart
        fig = px.line(
            x=subdivisions,
            y=values,
            title=f"{kpi_name} Trend by Subdivision",
            markers=True
        )
    fig.update_layout(
        height=400,
        showlegend=True if chart_type == "pie" else False
    )
    return fig

def create_radar_chart(bu, month):
    """Create radar chart for performance overview"""
    data = kpi_data[bu][month]
    # Extract key metrics for radar chart
    metrics = [
        'Revenue Performance',
        'Customer Satisfaction',
        'Quality Score',
        'Employee Engagement',
        'Operational Efficiency',
        'Cost Management'
    ]
    # Calculate normalized scores (0-100)
    scores = [
        min(100, data['Financial']['Revenue vs Target']['value']),
        data['Customer & Service']['CSAT']['value'] * 20,  # Convert 4.5/5 to 90/100
        data['Quality Metrics']['System Uptime']['value'],
        data['Employee Fulfillment']['Engagement Score']['value'] * 10,  # Convert 8.5/10 to 85/100
        100 - data['Quality Metrics']['Defect Rate']['value'] * 10,  # Invert defect rate
        100 - abs(data['Financial']['Cost per Project']['change'])  # Invert cost increase
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=metrics,
        fill='toself',
        name=f'{bu} Performance',
        line_color='#4472C4',
        fillcolor='rgba(68, 114, 196, 0.3)'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Performance Overview",
        height=350
    )
    return fig

# Main app layout
def main():
    # Header with animated gradient
    st.markdown(f"""
    <div style="
        background: linear-gradient(45deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradient-wave 8s ease infinite;
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    ">
        <style>
        @keyframes gradient-wave {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        </style>
        <h1 style="margin: 0; font-size: 32px; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">IT Company Dashboard</h1>
        <h2 style="margin: 10px 0 0 0; font-size: 24px; opacity: 0.95; font-weight: 500;">
            {st.session_state.selected_bu} Performance
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Create layout with sidebar and main content
    with st.sidebar:
        st.markdown("### Select Month")
        selected_month = st.selectbox(
            "Month",
            ['January', 'February', 'March', 'April', 'May', 'June'],
            index=['January', 'February', 'March', 'April', 'May', 'June'].index(st.session_state.selected_month)
        )
        st.markdown("### Select Business Unit")
        selected_bu = st.radio(
            "Business Unit",
            ['BU1', 'BU2', 'BU3'],
            index=['BU1', 'BU2', 'BU3'].index(st.session_state.selected_bu)
        )
        # Update session state
        if selected_month != st.session_state.selected_month or selected_bu != st.session_state.selected_bu:
            st.session_state.selected_month = selected_month
            st.session_state.selected_bu = selected_bu
            st.rerun()

    # Get current data
    current_data = kpi_data[st.session_state.selected_bu][st.session_state.selected_month]

    # Main layout
    col_left, col_right = st.columns([2, 1])
    with col_left:
       # --- Financial Section ---
       st.markdown("### 📊 Financial")
       fin_col1, fin_col2, fin_col3 = st.columns([1, 1, 1])
        
        with fin_col1:
            with st.container():
                st.markdown(
                    """
                    <style>
                        .kpi-box {
                            padding: 15px;
                            border-radius: 8px;
                            background-color: #f0f2f6;
                            margin-bottom: 10px;
                        }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                # Revenue vs Target
                target_data = current_data['Financial']['Revenue vs Target']
                st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
                create_kpi_metric("Revenue vs Target", target_data['value'], "%", target_data['change'], "🎯")
                with st.expander("🎯 Revenue vs Target Details", expanded=False):
                    st.markdown("**Subdivision Breakdown**")
                    tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                    with tab1:
                        st.metric("PRODEV Target Achievement", "98%", "3%")
                        fig = create_subdivision_chart("PRODEV Revenue vs Target", {"Jan": 95, "Feb": 97, "Mar": 96, "Apr": 98, "May": 99}, "line")
                        st.plotly_chart(fig, use_container_width=True, key="chart_target_prodev")
                    with tab2:
                        st.metric("PD1 Target Achievement", "89%", "2%")
                        fig = create_subdivision_chart("PD1 Revenue vs Target", {"Jan": 87, "Feb": 88, "Mar": 89, "Apr": 90, "May": 91}, "bar")
                        st.plotly_chart(fig, use_container_width=True, key="chart_target_pd1")
                    with tab3:
                        st.metric("PD2 Target Achievement", "92%", "1%")
                    with tab4:
                        st.metric("DOCS Target Achievement", "95%", "4%")
                st.markdown('</div>', unsafe_allow_html=True)
        
                # Cost per Project
                cost_data = current_data['Financial']['Cost per Project']
                st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
                create_kpi_metric("Cost per Project", cost_data['value'], "K", cost_data['change'], "💸")
                with st.expander("💸 Cost per Project Details", expanded=False):
                    st.markdown("**Cost Breakdown by Subdivision**")
                    tab1, tab2 = st.tabs(["PRODEV", "PD1"])
                    with tab1:
                        st.metric("PRODEV Cost", "$45K", "-5%")
                        fig = create_subdivision_chart("PRODEV Cost Trend", {"Jan": 48, "Feb": 47, "Mar": 45, "Apr": 44, "May": 42}, "line")
                        st.plotly_chart(fig, use_container_width=True, key="chart_cost_prodev")
                    with tab2:
                        st.metric("PD1 Cost", "$38K", "-2%")
                        fig = create_subdivision_chart("PD1 Cost Trend", {"Jan": 40, "Feb": 39, "Mar": 38, "Apr": 37, "May": 36}, "bar")
                        st.plotly_chart(fig, use_container_width=True, key="chart_cost_pd1")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with fin_col2:
            # Gross Margin
            margin_data = current_data['Financial']['Gross Margin']
            st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
            create_kpi_metric("Gross Margin", margin_data['value'], "%", margin_data['change'], "📊")
            with st.expander("📊 Gross Margin Details", expanded=False):
                st.markdown("**Margin Analysis by Subdivision**")
                tab1, tab2 = st.tabs(["PRODEV", "PD1"])
                with tab1:
                    st.metric("PRODEV Margin", "42%", "2%")
                    fig = create_subdivision_chart("PRODEV Margin Trend", {"Jan": 40, "Feb": 41, "Mar": 42, "Apr": 43, "May": 44}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_margin_prodev")
                with tab2:
                    st.metric("PD1 Margin", "38%", "1%")
                    fig = create_subdivision_chart("PD1 Margin Trend", {"Jan": 37, "Feb": 37, "Mar": 38, "Apr": 38, "May": 39}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_margin_pd1")
            st.markdown('</div>', unsafe_allow_html=True)
        
            # AR Days
            ar_data = current_data['Financial']['AR Days']
            st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
            create_kpi_metric("AR Days", ar_data['value'], "days", ar_data['change'], "📅")
            with st.expander("📅 AR Days Details", expanded=False):
                st.markdown("**AR Days by Subdivision**")
                tab1, tab2 = st.tabs(["PRODEV", "PD1"])
                with tab1:
                    st.metric("PRODEV AR Days", "28", "-3")
                    fig = create_subdivision_chart("PRODEV AR Days", {"Jan": 31, "Feb": 30, "Mar": 29, "Apr": 28, "May": 27}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_ar_prodev")
                with tab2:
                    st.metric("PD1 AR Days", "35", "-1")
                    fig = create_subdivision_chart("PD1 AR Days", {"Jan": 36, "Feb": 36, "Mar": 35, "Apr": 35, "May": 34}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_ar_pd1")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with fin_col3:
            # Revenue
            revenue_data = current_data['Financial']['Revenue']
            st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
            create_kpi_metric("Revenue", revenue_data['value'], "M", revenue_data['change'], "💰")
            with st.expander("💰 Revenue Details", expanded=False):
                st.markdown("**Revenue Breakdown by Subdivision**")
                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS", "ITS", "CHAPTER"])
                with tab1:
                    st.metric("PRODEV Revenue", f"${revenue_data['subdivisions']['PRODEV']}K", "5.2%")
                    fig = create_subdivision_chart("PRODEV Revenue", {"Jan": 45, "Feb": 52, "Mar": 48, "Apr": 55, "May": 60}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_revenue_prodev")
                with tab2:
                    st.metric("PD1 Revenue", f"${revenue_data['subdivisions']['PD1']}K", "3.1%")
                    fig = create_subdivision_chart("PD1 Revenue", {"Jan": 35, "Feb": 42, "Mar": 38, "Apr": 45, "May": 50}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_revenue_pd1")
                with tab3:
                    st.metric("PD2 Revenue", f"${revenue_data['subdivisions']['PD2']}K", "2.8%")
                with tab4:
                    st.metric("DOCS Revenue", f"${revenue_data['subdivisions']['DOCS']}K", "1.5%")
                with tab5:
                    st.metric("ITS Revenue", f"${revenue_data['subdivisions']['ITS']}K", "6.2%")
                with tab6:
                    st.metric("CHAPTER Revenue", f"${revenue_data['subdivisions']['CHAPTER']}K", "4.1%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        
        # --- Customer & Service Section ---
        st.markdown("### 👥 Customer & Service")
        cs_col1, cs_col2, cs_col3 = st.columns([1, 1, 1])
        
        with cs_col1:
            # NPS
            nps_data = current_data['Customer & Service']['NPS']
            st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
            create_kpi_metric("NPS", nps_data['value'], "", nps_data['change'], "📈")
            with st.expander("📈 NPS Details", expanded=False):
                st.markdown("**Net Promoter Score by Subdivision**")
                tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                with tab1:
                    st.metric("PRODEV NPS", "50", "+5")
                    fig = create_subdivision_chart("PRODEV NPS", {"Jan": 45, "Feb": 47, "Mar": 48, "Apr": 49, "May": 50}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_nps_prodev")
                with tab2:
                    st.metric("PD1 NPS", "40", "+3")
                    fig = create_subdivision_chart("PD1 NPS", {"Jan": 38, "Feb": 39, "Mar": 40, "Apr": 41, "May": 42}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_nps_pd1")
                with tab3:
                    st.metric("PD2 NPS", "45", "+2")
                with tab4:
                    st.metric("DOCS NPS", "38", "+4")
            st.markdown('</div>', unsafe_allow_html=True)
        
            # Avg Response Time
            response_data = current_data['Customer & Service']['Avg Response Time']
            st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
            create_kpi_metric("Avg Response Time", response_data['value'], "h", response_data['change'], "⏱️")
            with st.expander("⏱️ Avg Response Time Details", expanded=False):
                st.markdown("**Average Response Time by Subdivision**")
                tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                with tab1:
                    st.metric("PRODEV Avg Response", "2.5h", "-0.3h")
                    fig = create_subdivision_chart("PRODEV Response Time", {"Jan": 3.0, "Feb": 2.8, "Mar": 2.7, "Apr": 2.6, "May": 2.5}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_response_prodev")
                with tab2:
                    st.metric("PD1 Avg Response", "2.8h", "-0.2h")
                    fig = create_subdivision_chart("PD1 Response Time", {"Jan": 3.2, "Feb": 3.0, "Mar": 2.9, "Apr": 2.8, "May": 2.7}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_response_pd1")
                with tab3:
                    st.metric("PD2 Avg Response", "3.0h", "-0.1h")
                with tab4:
                    st.metric("DOCS Avg Response", "2.6h", "-0.3h")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # (Tambahkan Quality Metrics dan Employee Fulfillment dengan format yang sama seperti di atas)


        # Quality Metrics Section
        st.markdown("### 🎯 Quality Metrics")
        qm_col1, qm_col2, qm_col3 = st.columns([2, 1, 1])

        with qm_col1:
            # System Uptime
            uptime_data = current_data['Quality Metrics']['System Uptime']
            create_kpi_metric("System Uptime", uptime_data['value'], "%", uptime_data['change'], "⚡")
            with st.expander("⚡ System Uptime Details", expanded=False):
                st.markdown("**System Uptime by Subdivision**")
                chart_type = st.selectbox("Chart Type", ["bar", "pie", "line"], key="uptime_chart")
                fig = create_subdivision_chart("System Uptime", uptime_data['subdivisions'], chart_type)
                st.plotly_chart(fig, use_container_width=True)

        with qm_col2:
            # Defect Rate
            defect_data = current_data['Quality Metrics']['Defect Rate']
            create_kpi_metric("Defect Rate", defect_data['value'], "%", defect_data['change'], "🔍")
            with st.expander("🔍 Defect Rate Details", expanded=False):
                st.markdown("**Defect Rate by Subdivision**")
                tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                with tab1:
                    st.metric("PRODEV Defect Rate", "1.2%", "-0.2%")
                    fig = create_subdivision_chart("PRODEV Defect Rate", {"Jan": 1.5, "Feb": 1.4, "Mar": 1.3, "Apr": 1.2, "May": 1.1}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_defect_prodev")
                with tab2:
                    st.metric("PD1 Defect Rate", "1.4%", "-0.1%")
                    fig = create_subdivision_chart("PD1 Defect Rate", {"Jan": 1.6, "Feb": 1.5, "Mar": 1.4, "Apr": 1.4, "May": 1.3}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_defect_pd1")
                with tab3:
                    st.metric("PD2 Defect Rate", "1.5%", "0%")
                with tab4:
                    st.metric("DOCS Defect Rate", "1.3%", "-0.2%")

            # Rework Rate
            rework_data = current_data['Quality Metrics']['Rework Rate']
            create_kpi_metric("Rework Rate", rework_data['value'], "%", rework_data['change'], "🔄")
            with st.expander("🔄 Rework Rate Details", expanded=False):
                st.markdown("**Rework Rate by Subdivision**")
                tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                with tab1:
                    st.metric("PRODEV Rework Rate", "3.2%", "-0.3%")
                    fig = create_subdivision_chart("PRODEV Rework Rate", {"Jan": 3.8, "Feb": 3.6, "Mar": 3.4, "Apr": 3.3, "May": 3.2}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_rework_prodev")
                with tab2:
                    st.metric("PD1 Rework Rate", "3.5%", "-0.2%")
                    fig = create_subdivision_chart("PD1 Rework Rate", {"Jan": 3.9, "Feb": 3.8, "Mar": 3.6, "Apr": 3.5, "May": 3.4}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_rework_pd1")
                with tab3:
                    st.metric("PD2 Rework Rate", "3.8%", "-0.1%")
                with tab4:
                    st.metric("DOCS Rework Rate", "3.4%", "-0.2%")

        with qm_col3:
            # Resolution Success
            resolution_data = current_data['Quality Metrics']['Resolution Success']
            create_kpi_metric("Resolution Success", resolution_data['value'], "%", resolution_data['change'], "✅")
            with st.expander("✅ Resolution Success Details", expanded=False):
                st.markdown("**Resolution Success by Subdivision**")
                tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                with tab1:
                    st.metric("PRODEV Resolution", "97%", "+1%")
                    fig = create_subdivision_chart("PRODEV Resolution", {"Jan": 95, "Feb": 96, "Mar": 96, "Apr": 97, "May": 98}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_resolution_prodev")
                with tab2:
                    st.metric("PD1 Resolution", "95%", "+1%")
                    fig = create_subdivision_chart("PD1 Resolution", {"Jan": 94, "Feb": 94, "Mar": 95, "Apr": 95, "May": 96}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_resolution_pd1")
                with tab3:
                    st.metric("PD2 Resolution", "94%", "+1%")
                with tab4:
                    st.metric("DOCS Resolution", "96%", "+2%")

            # Code Review Coverage
            review_data = current_data['Quality Metrics']['Code Review Coverage']
            create_kpi_metric("Code Review Coverage", review_data['value'], "%", review_data['change'], "📝")
            with st.expander("📝 Code Review Coverage Details", expanded=False):
                st.markdown("**Code Review Coverage by Subdivision**")
                tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                with tab1:
                    st.metric("PRODEV Code Review", "92%", "+2%")
                    fig = create_subdivision_chart("PRODEV Code Review", {"Jan": 88, "Feb": 89, "Mar": 90, "Apr": 91, "May": 92}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_review_prodev")
                with tab2:
                    st.metric("PD1 Code Review", "90%", "+1%")
                    fig = create_subdivision_chart("PD1 Code Review", {"Jan": 87, "Feb": 88, "Mar": 89, "Apr": 89, "May": 90}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_review_pd1")
                with tab3:
                    st.metric("PD2 Code Review", "89%", "+1%")
                with tab4:
                    st.metric("DOCS Code Review", "91%", "+2%")

        # Employee Fulfillment Section
        st.markdown("### 👨‍💼 Employee Fulfillment")
        ef_col1, ef_col2, ef_col3 = st.columns([2, 1, 1])

        with ef_col1:
            # Engagement Score
            engagement_data = current_data['Employee Fulfillment']['Engagement Score']
            create_kpi_metric("Engagement Score", engagement_data['value'], "/10", engagement_data['change'], "👨‍💼")
            with st.expander("👨‍💼 Engagement Score Details", expanded=False):
                st.markdown("**Employee Engagement by Subdivision**")
                chart_type = st.selectbox("Chart Type", ["bar", "pie", "line"], key="engagement_chart")
                fig = create_subdivision_chart("Engagement Score", engagement_data['subdivisions'], chart_type)
                st.plotly_chart(fig, use_container_width=True)

        with ef_col2:
            # Attrition Rate
            attrition_data = current_data['Employee Fulfillment']['Attrition Rate']
            create_kpi_metric("Attrition Rate", attrition_data['value'], "%", attrition_data['change'], "📉")
            with st.expander("📉 Attrition Rate Details", expanded=False):
                st.markdown("**Attrition Rate by Subdivision**")
                tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                with tab1:
                    st.metric("PRODEV Attrition", "8%", "-1%")
                    fig = create_subdivision_chart("PRODEV Attrition", {"Jan": 10, "Feb": 9, "Mar": 9, "Apr": 8, "May": 8}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_attrition_prodev")
                with tab2:
                    st.metric("PD1 Attrition", "9%", "-1%")
                    fig = create_subdivision_chart("PD1 Attrition", {"Jan": 11, "Feb": 10, "Mar": 9, "Apr": 9, "May": 9}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_attrition_pd1")
                with tab3:
                    st.metric("PD2 Attrition", "10%", "0%")
                with tab4:
                    st.metric("DOCS Attrition", "7%", "-1%")

            # Training Hours
            training_data = current_data['Employee Fulfillment']['Training Hours']
            create_kpi_metric("Training Hours/Emp", training_data['value'], "hrs", training_data['change'], "📚")
            with st.expander("📚 Training Hours Details", expanded=False):
                st.markdown("**Training Hours per Employee by Subdivision**")
                tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                with tab1:
                    st.metric("PRODEV Training", "45 hrs", "+3 hrs")
                    fig = create_subdivision_chart("PRODEV Training", {"Jan": 38, "Feb": 40, "Mar": 42, "Apr": 44, "May": 45}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_training_prodev")
                with tab2:
                    st.metric("PD1 Training", "40 hrs", "+2 hrs")
                    fig = create_subdivision_chart("PD1 Training", {"Jan": 35, "Feb": 36, "Mar": 38, "Apr": 39, "May": 40}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_training_pd1")
                with tab3:
                    st.metric("PD2 Training", "38 hrs", "+1 hrs")
                with tab4:
                    st.metric("DOCS Training", "42 hrs", "+3 hrs")

        with ef_col3:
            # Overtime per FTE
            overtime_data = current_data['Employee Fulfillment']['Overtime per FTE']
            create_kpi_metric("Overtime per FTE", overtime_data['value'], "h", overtime_data['change'], "⏰")
            with st.expander("⏰ Overtime per FTE Details", expanded=False):
                st.markdown("**Overtime per FTE by Subdivision**")
                tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                with tab1:
                    st.metric("PRODEV Overtime", "3.0h", "-0.2h")
                    fig = create_subdivision_chart("PRODEV Overtime", {"Jan": 3.5, "Feb": 3.4, "Mar": 3.2, "Apr": 3.1, "May": 3.0}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_overtime_prodev")
                with tab2:
                    st.metric("PD1 Overtime", "3.2h", "-0.1h")
                    fig = create_subdivision_chart("PD1 Overtime", {"Jan": 3.6, "Feb": 3.5, "Mar": 3.4, "Apr": 3.3, "May": 3.2}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_overtime_pd1")
                with tab3:
                    st.metric("PD2 Overtime", "3.5h", "0h")
                with tab4:
                    st.metric("DOCS Overtime", "3.1h", "-0.2h")

            # Internal Promotion Rate
            promotion_data = current_data['Employee Fulfillment']['Internal Promotion Rate']
            create_kpi_metric("Internal Promotion Rate", promotion_data['value'], "%", promotion_data['change'], "🎖️")
            with st.expander("🎖️ Internal Promotion Rate Details", expanded=False):
                st.markdown("**Internal Promotion Rate by Subdivision**")
                tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                with tab1:
                    st.metric("PRODEV Promotion", "12%", "+1%")
                    fig = create_subdivision_chart("PRODEV Promotion Rate", {"Jan": 10, "Feb": 10, "Mar": 11, "Apr": 11, "May": 12}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_promotion_prodev")
                with tab2:
                    st.metric("PD1 Promotion", "10%", "+1%")
                    fig = create_subdivision_chart("PD1 Promotion Rate", {"Jan": 9, "Feb": 9, "Mar": 9, "Apr": 10, "May": 10}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_promotion_pd1")
                with tab3:
                    st.metric("PD2 Promotion", "9%", "+1%")
                with tab4:
                    st.metric("DOCS Promotion", "11%", "+2%")

    with col_right:
        # Performance Overview
        st.markdown("### 📈 Performance Overview")
        fig_radar = create_radar_chart(st.session_state.selected_bu, st.session_state.selected_month)
        st.plotly_chart(fig_radar, use_container_width=True)

if __name__ == "__main__":
    main()
