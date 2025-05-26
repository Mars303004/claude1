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
    higher_better = [
        "Revenue", "Revenue vs Target", "Gross Margin", "CSAT", "NPS", "SLA Achievement",
        "Retention Rate", "System Uptime", "Resolution Success", "Code Review Coverage",
        "Engagement Score", "Training Hours/Emp", "Internal Promotion Rate"
    ]
    lower_better = [
        "Cost per Project", "AR Days", "Avg Response Time", "Defect Rate", "Rework Rate",
        "Attrition Rate", "Overtime per FTE"
    ]

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

    st.metric(
        label=f"{icon} {title}",
        value=display_value,
        delta=change_str,
        delta_color=delta_color
    )

def create_subdivision_chart(kpi_name, subdivision_data, chart_type="bar"):
    subdivisions = list(subdivision_data.keys())
    values = list(subdivision_data.values())
    if chart_type == "bar":
        fig = px.bar(x=subdivisions, y=values, title=f"{kpi_name} by Subdivision", color=values, color_continuous_scale="Blues")
    elif chart_type == "pie":
        fig = px.pie(values=values, names=subdivisions, title=f"{kpi_name} Distribution by Subdivision")
    else:
        fig = px.line(x=subdivisions, y=values, title=f"{kpi_name} Trend by Subdivision", markers=True)
    fig.update_layout(height=400, showlegend=(chart_type == "pie"))
    return fig

def create_radar_chart(bu, month):
    data = kpi_data[bu][month]
    metrics = [
        'Revenue Performance', 'Customer Satisfaction', 'Quality Score',
        'Employee Engagement', 'Operational Efficiency', 'Cost Management'
    ]
    scores = [
        min(100, data['Financial']['Revenue vs Target']['value']),
        data['Customer & Service']['CSAT']['value'] * 20,
        data['Quality Metrics']['System Uptime']['value'],
        data['Employee Fulfillment']['Engagement Score']['value'] * 10,
        100 - data['Quality Metrics']['Defect Rate']['value'] * 10,
        100 - abs(data['Financial']['Cost per Project']['change'])
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=scores, theta=metrics, fill='toself'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=350, showlegend=False)
    return fig

# Main app layout
def main():
    # CSS for gray boxes
    st.markdown("""
    <style>
        .section-box {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

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

    # Sidebar
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
        if selected_month != st.session_state.selected_month or selected_bu != st.session_state.selected_bu:
            st.session_state.selected_month = selected_month
            st.session_state.selected_bu = selected_bu
            st.rerun()

    current_data = kpi_data[st.session_state.selected_bu][st.session_state.selected_month]

    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Financial Section
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown("### 📊 Financial")
        fin_col1, fin_col2, fin_col3 = st.columns([1, 1, 1])
        with fin_col1:
            target_data = current_data['Financial']['Revenue vs Target']
            create_kpi_metric("Revenue vs Target", target_data['value'], "%", target_data['change'], "🎯")
            with st.expander("💰 Revenue vs Target Details", expanded=False):
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

            cost_data = current_data['Financial']['Cost per Project']
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
        with fin_col2:
            margin_data = current_data['Financial']['Gross Margin']
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

            ar_data = current_data['Financial']['AR Days']
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
        with fin_col3:
            revenue_data = current_data['Financial']['Revenue']
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

        # Customer & Service Section
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown("### 👥 Customer & Service")
        cs_col1, cs_col2, cs_col3 = st.columns([1, 1, 1])
        with cs_col1:
            nps_data = current_data['Customer & Service']['NPS']
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

            response_data = current_data['Customer & Service']['Avg Response Time']
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
        with cs_col2:
            sla_data = current_data['Customer & Service']['SLA Achievement']
            create_kpi_metric("SLA Achievement", sla_data['value'], "%", sla_data['change'], "🎯")
            with st.expander("🎯 SLA Achievement Details", expanded=False):
                st.markdown("**SLA Achievement by Subdivision**")
                tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                with tab1:
                    st.metric("PRODEV SLA", "95%", "+2%")
                    fig = create_subdivision_chart("PRODEV SLA", {"Jan": 90, "Feb": 91, "Mar": 93, "Apr": 94, "May": 95}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_sla_prodev")
                with tab2:
                    st.metric("PD1 SLA", "92%", "+1%")
                    fig = create_subdivision_chart("PD1 SLA", {"Jan": 91, "Feb": 91, "Mar": 92, "Apr": 92, "May": 93}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_sla_pd1")
                with tab3:
                    st.metric("PD2 SLA", "90%", "+1%")
                with tab4:
                    st.metric("DOCS SLA", "93%", "+2%")

            retention_data = current_data['Customer & Service']['Retention Rate']
            create_kpi_metric("Retention Rate", retention_data['value'], "%", retention_data['change'], "🔒")
            with st.expander("🔒 Retention Rate Details", expanded=False):
                st.markdown("**Customer Retention by Subdivision**")
                tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                with tab1:
                    st.metric("PRODEV Retention", "94%", "+1%")
                    fig = create_subdivision_chart("PRODEV Retention Rate", {"Jan": 92, "Feb": 93, "Mar": 93, "Apr": 94, "May": 95}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_retention_prodev")
                with tab2:
                    st.metric("PD1 Retention", "91%", "+1%")
                    fig = create_subdivision_chart("PD1 Retention Rate", {"Jan": 90, "Feb": 90, "Mar": 91, "Apr": 91, "May": 92}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_retention_pd1")
                with tab3:
                    st.metric("PD2 Retention", "90%", "+1%")
                with tab4:
                    st.metric("DOCS Retention", "92%", "+2%")
        with cs_col3:
            csat_data = current_data['Customer & Service']['CSAT']
            create_kpi_metric("CSAT", csat_data['value'], "/5", csat_data['change'], "⭐")
            with st.expander("⭐ CSAT Details", expanded=False):
                st.markdown("**Customer Satisfaction by Subdivision**")
                tab1, tab2, tab3, tab4 = st.tabs(["PRODEV", "PD1", "PD2", "DOCS"])
                with tab1:
                    st.metric("PRODEV CSAT", f"{csat_data['subdivisions']['PRODEV']:.1f}/5", "0.2")
                    fig = create_subdivision_chart("PRODEV CSAT", {"Jan": 4.1, "Feb": 4.3, "Mar": 4.2, "Apr": 4.4, "May": 4.5}, "line")
                    st.plotly_chart(fig, use_container_width=True, key="chart_csat_prodev")
                with tab2:
                    st.metric("PD1 CSAT", f"{csat_data['subdivisions']['PD1']:.1f}/5", "0.1")
                    fig = create_subdivision_chart("PD1 CSAT", {"Jan": 3.9, "Feb": 4.0, "Mar": 4.1, "Apr": 4.2, "May": 4.3}, "bar")
                    st.plotly_chart(fig, use_container_width=True, key="chart_csat_pd1")
                with tab3:
                    st.metric("PD2 CSAT", f"{csat_data['subdivisions']['PD2']:.1f}/5", "0.3")
                with tab4:
                    st.metric("DOCS CSAT", f"{csat_data['subdivisions']['DOCS']:.1f}/5", "0.1")
        st.markdown('</div>', unsafe_allow_html=True)

        # Quality Metrics Section
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown("### 🎯 Quality Metrics")
        qm_col1, qm_col2, qm_col3 = st.columns([2, 1, 1])
        with qm_col1:
            uptime_data = current_data['Quality Metrics']['System Uptime']
            create_kpi_metric("System Uptime", uptime_data['value'], "%", uptime_data['change'], "⚡")
            with st.expander("⚡ System Uptime Details", expanded=False):
                st.markdown("**System Uptime by Subdivision**")
                chart_type = st.selectbox("Chart Type", ["bar", "pie", "line"], key="uptime_chart")
                fig = create_subdivision_chart("System Uptime", uptime_data['subdivisions'], chart_type)
                st.plotly_chart(fig, use_container_width=True)
        with qm_col2:
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
            resolution_data =
