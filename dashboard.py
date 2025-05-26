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
    
    # Format change value
    if change > 0:
        change_str = f"+{change}%"
        delta_color = "normal"
    elif change < 0:
        change_str = f"{change}%"
        delta_color = "inverse"
    else:
        change_str = "0%"
        delta_color = "off"
    
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
        # Financial Section
        st.markdown("### 📊 Financial")
        
        fin_col1, fin_col2, fin_col3 = st.columns([1, 1, 1])
        
        with fin_col1:
            # Revenue vs Target
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
            
            # Cost per Project
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
            # Gross Margin
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
            
            # AR Days
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
            # Revenue
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
        
        # Customer & Service Section
        st.markdown("### 👥 Customer & Service")
        cs_col1, cs_col2, cs_col3 = st.columns([1, 1, 1])
        
        with cs_col1:
            # NPS
            nps_data = current_data['Customer & Service']['NPS']
            create_kpi_metric("NPS", nps_data['value'], "", nps_data['change'], "📈")
            
            # Avg Response Time
            response_data = current_data['Customer & Service']['Avg Response Time']
            create_kpi_metric("Avg Response Time", response_data['value'], "h", response_data['change'], "⏱️")
        
        with cs_col2:
            # SLA Achievement
            sla_data = current_data['Customer & Service']['SLA Achievement']
            create_kpi_metric("SLA Achievement", sla_data['value'], "%", sla_data['change'], "🎯")
            
            # Retention Rate
            retention_data = current_data['Customer & Service']['Retention Rate']
            create_kpi_metric("Retention Rate", retention_data['value'], "%", retention_data['change'], "🔒")
        
        with cs_col3:
            # CSAT
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
            
            # Rework Rate
            rework_data = current_data['Quality Metrics']['Rework Rate']
            create_kpi_metric("Rework Rate", rework_data['value'], "%", rework_data['change'], "🔄")
        
        with qm_col3:
            # Resolution Success
            resolution_data = current_data['Quality Metrics']['Resolution Success']
            create_kpi_metric("Resolution Success", resolution_data['value'], "%", resolution_data['change'], "✅")
            
            # Code Review Coverage
            review_data = current_data['Quality Metrics']['Code Review Coverage']
            create_kpi_metric("Code Review Coverage", review_data['value'], "%", review_data['change'], "📝")
        
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
            
            # Training Hours
            training_data = current_data['Employee Fulfillment']['Training Hours']
            create_kpi_metric("Training Hours/Emp", training_data['value'], "hrs", training_data['change'], "📚")
        
        with ef_col3:
            # Overtime per FTE
            overtime_data = current_data['Employee Fulfillment']['Overtime per FTE']
            create_kpi_metric("Overtime per FTE", overtime_data['value'], "h", overtime_data['change'], "⏰")
            
            # Internal Promotion Rate
            promotion_data = current_data['Employee Fulfillment']['Internal Promotion Rate']
            create_kpi_metric("Internal Promotion Rate", promotion_data['value'], "%", promotion_data['change'], "🎖️")
    
    with col_right:
        # Performance Overview
        st.markdown("### 📈 Performance Overview")
        fig_radar = create_radar_chart(st.session_state.selected_bu, st.session_state.selected_month)
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Quality Metrics Summary
        st.markdown("### 🎯 Quality Summary")
        
        uptime_data = current_data['Quality Metrics']['System Uptime']
        create_kpi_metric("System Uptime", uptime_data['value'], "%", uptime_data['change'], "⚡")
        
        qm_col1, qm_col2 = st.columns(2)
        
        with qm_col1:
            defect_data = current_data['Quality Metrics']['Defect Rate']
            create_kpi_metric("Defect Rate", defect_data['value'], "%", defect_data['change'], "🔍")
            
            rework_data = current_data['Quality Metrics']['Rework Rate']
            create_kpi_metric("Rework Rate", rework_data['value'], "%", rework_data['change'], "🔄")
        
        with qm_col2:
            resolution_data = current_data['Quality Metrics']['Resolution Success']
            create_kpi_metric("Resolution Success", resolution_data['value'], "%", resolution_data['change'], "✅")
            
            code_review_data = current_data['Quality Metrics']['Code Review Coverage']
            create_kpi_metric("Code Review", code_review_data['value'], "%", code_review_data['change'], "📝")
