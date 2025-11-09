"""
Agile Sprint Performance & Portfolio Analytics Dashboard
Executive Presentation View

Strategic Project Management & Operations Portfolio Project
Designed to showcase PM and Strategy/Operations capabilities.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Import utility modules
from utils.data_processing import (
    load_all_data, get_current_sprint, calculate_rolling_metrics,
    calculate_story_type_distribution, get_completed_stories,
    calculate_team_member_metrics, get_initiative_summary,
    get_sprint_summary_stats
)
from utils.metrics import (
    calculate_sprint_health_score, calculate_velocity_trend,
    calculate_cycle_time_metrics, calculate_blocker_impact,
    calculate_team_velocity_contribution, identify_bottlenecks,
    calculate_quality_trend, calculate_work_distribution_by_role
)
from utils.prioritization import (
    add_priority_scores, add_quadrant_classification,
    get_portfolio_composition, get_quick_wins, get_time_sinks,
    calculate_portfolio_health_score, generate_portfolio_recommendations,
    create_intake_funnel_data
)
from utils.predictive_models import (
    predict_sprint_completion_probability, assess_all_initiatives_risk,
    forecast_velocity_next_n_sprints, generate_predictive_recommendations,
    calculate_probability_distribution_chart_data
)
from utils.visualizations import (
    create_velocity_trend_chart, create_burndown_chart,
    create_impact_effort_matrix, create_health_gauge,
    create_capacity_heatmap, create_cycle_time_boxplot,
    create_story_type_stacked_area, create_completion_probability_chart,
    create_initiative_funnel, create_treemap, create_roi_scatter, COLORS
)

# Page config
st.set_page_config(
    page_title="Sprint Analytics Executive Presentation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Executive Presentation Style
st.markdown("""
<style>
    /* Import professional font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif !important;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Remove padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }

    /* Left sidebar styling */
    .sidebar-content {
        background: linear-gradient(135deg, #d4e6f1 0%, #aed6f1 100%);
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .sidebar-header {
        background: #5d3a9b;
        color: white;
        padding: 12px 15px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.9rem;
        text-align: center;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
    }

    .sidebar-header-teal {
        background: #00a896;
        color: white;
        padding: 12px 15px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.9rem;
        text-align: center;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
    }

    .sidebar-text {
        font-size: 0.85rem;
        line-height: 1.6;
        color: #1a1a1a;
        margin-bottom: 10px;
    }

    .sidebar-bullet {
        margin-left: 15px;
        margin-bottom: 8px;
        font-size: 0.8rem;
        line-height: 1.5;
    }

    /* Main header */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a1a1a;
        text-align: center;
        margin: 0;
        padding: 20px 0 5px 0;
    }

    .main-subtitle {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin: 0;
        padding: 0 0 20px 0;
        font-style: italic;
    }

    /* Blue dashboard header bar */
    .dashboard-header {
        background: linear-gradient(90deg, #2e7d9e 0%, #3b9fc7 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        margin: 20px 0;
        font-size: 1.3rem;
        font-weight: 700;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15);
    }

    /* KPI metric cards */
    .kpi-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #2e7d9e;
        margin: 5px 0;
    }

    .kpi-label {
        font-size: 0.85rem;
        color: #666;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-sublabel {
        font-size: 0.75rem;
        color: #999;
        margin-top: 3px;
    }

    /* Section headers */
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2d3748;
        margin: 25px 0 15px 0;
        padding-bottom: 8px;
        border-bottom: 3px solid #2e7d9e;
    }

    /* Recommendation boxes */
    .recommendation-box {
        background: white;
        border-left: 5px solid #3b82f6;
        padding: 12px 18px;
        margin: 10px 0;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        font-size: 0.9rem;
        line-height: 1.5;
    }

    .recommendation-box-green {
        border-left-color: #10b981;
        background: #f0fdf4;
    }

    .recommendation-box-orange {
        border-left-color: #f59e0b;
        background: #fffbeb;
    }

    .recommendation-box-red {
        border-left-color: #ef4444;
        background: #fef2f2;
    }

    /* Yellow results box */
    .results-box {
        background: linear-gradient(135deg, #fff4b3 0%, #ffe680 100%);
        border: 3px solid #f59e0b;
        border-radius: 10px;
        padding: 20px;
        margin: 25px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .results-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .results-text {
        font-size: 0.95rem;
        line-height: 1.7;
        color: #1a1a1a;
        font-weight: 500;
    }

    /* Footer bar */
    .footer-bar {
        background: linear-gradient(90deg, #5d3a9b 0%, #7c5aae 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        margin: 30px 0 10px 0;
        text-align: center;
        font-size: 1rem;
        font-weight: 700;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15);
    }

    .target-role {
        font-size: 0.95rem;
        color: #666;
        text-align: center;
        margin: 10px 0;
        font-style: italic;
    }

    /* Contact info */
    .contact-info {
        font-size: 0.75rem;
        color: #1a1a1a;
        text-align: center;
        margin-top: 15px;
        line-height: 1.5;
        font-weight: 500;
    }

    /* Streamlit metric overrides */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #2e7d9e !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        color: #666 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load and prepare all data"""
    data = load_all_data()
    data['sprints'] = calculate_rolling_metrics(data['sprints'])
    data['initiatives'] = add_priority_scores(data['initiatives'])
    data['initiatives'] = add_quadrant_classification(data['initiatives'])
    return data

try:
    data = load_data()
    sprints_df = data['sprints']
    stories_df = data['stories']
    initiatives_df = data['initiatives']
    team_df = data['team']
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Please run: `python data/generate_data.py` to generate sample data.")
    st.stop()

# Get current sprint info
current_sprint = get_current_sprint(sprints_df)
current_sprint_num = int(current_sprint['sprint_number'])

# ============================================================================
# LAYOUT: 2-COLUMN (SIDEBAR + MAIN CONTENT)
# ============================================================================

# Create main layout
sidebar_col, main_col = st.columns([1, 3])

# ============================================================================
# LEFT SIDEBAR - PROJECT OVERVIEW
# ============================================================================
with sidebar_col:
    # PROJECT OVERVIEW
    st.markdown("""
    <div class="sidebar-content">
        <div style="background: #2e7d9e; color: white; padding: 12px; border-radius: 6px; font-weight: 700; text-align: center; margin-bottom: 15px; font-size: 0.9rem;">
            PROJECT OVERVIEW
        </div>
        <div class="sidebar-text">
            <strong>Purpose:</strong><br>
            <div class="sidebar-bullet">
            • Analyzes 6 months of Agile sprint data<br>
            (12 sprints, 355+ stories, 28 initiatives)<br><br>
            • Enables data-driven portfolio prioritization<br>
            using Impact/Effort matrix & ROI scoring<br><br>
            • Portfolio sprint health scoring &<br>
            risk identification framework<br><br>
            • Predictive analytics for capacity planning<br>
            & delivery forecasting
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # SKILLS DEMONSTRATED
    st.markdown("""
    <div class="sidebar-content">
        <div class="sidebar-header">
            SKILLS DEMONSTRATED
        </div>
        <div class="sidebar-text">
            <div class="sidebar-bullet">
            ✓ Portfolio & Roadmap Prioritization<br>
            ✓ Analytical Problem Solving & Insights<br>
            ✓ Data-Driven Decision Making<br>
            ✓ Cross-functional Stakeholder Rollups<br>
            ✓ Executive Analytics & Risk Scoring
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # BUSINESS IMPACT
    st.markdown("""
    <div class="sidebar-content">
        <div class="sidebar-header-teal">
            BUSINESS IMPACT
        </div>
        <div class="sidebar-text">
            <div class="sidebar-bullet">
            → Strategic Value:<br>
            Optimize resource allocation across<br>
            competing priorities<br><br>

            → Delivery Confidence:<br>
            Quantify delivery risk & capacity early<br><br>

            → Portfolio ROI:<br>
            75%+ effort on high-ROI initiatives
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # TECHNICAL CAPABILITIES
    st.markdown("""
    <div class="sidebar-content">
        <div class="sidebar-text">
            <strong>Technical Stack:</strong><br>
            <div class="sidebar-bullet">
            • Python (Pandas, NumPy, SciPy)<br>
            • Streamlit (Interactive Dashboards)<br>
            • Plotly (Data Visualization)<br>
            • Monte Carlo Simulations<br>
            • Statistical Risk Modeling
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CONTACT INFO
    st.markdown("""
    <div class="contact-info">
        <strong>Portfolio Project by: </strong><br>
        <strong>Noah Gallagher</strong><br>
        noah@datadrivenmgmt.com<br>
        github.com/noahgallagher1
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================
with main_col:
    # Main Title
    st.markdown("""
    <div class="main-title">
        Agile Sprint Performance & Portfolio Analytics Dashboard
    </div>
    <div class="main-subtitle">
        Strategic Project Management & Operations Portfolio Project
    </div>
    """, unsafe_allow_html=True)

    # Dashboard Header Bar
    st.markdown("""
    <div class="dashboard-header">
        Sprint Analytics & Portfolio Analytics Dashboard
    </div>
    """, unsafe_allow_html=True)

    # ========================================================================
    # KPI METRICS ROW
    # ========================================================================
    st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    # Calculate KPI values
    current_velocity = int(current_sprint['velocity'])
    avg_velocity_12m = int(sprints_df['velocity'].mean())
    completion_rate = current_sprint['completion_rate']
    health = calculate_sprint_health_score(current_sprint, sprints_df)
    sprint_health_score = int(health['health_score'])
    total_initiatives = len(initiatives_df)
    completed_initiatives = len(initiatives_df[initiatives_df['status'] == 'Completed'])

    with kpi1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{current_velocity}</div>
            <div class="kpi-label">Current Velocity</div>
            <div class="kpi-sublabel">Story Points</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{avg_velocity_12m}</div>
            <div class="kpi-label">Avg Velocity 12M</div>
            <div class="kpi-sublabel">Historical Average</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{int(completion_rate*100)}%</div>
            <div class="kpi-label">Completion Rate</div>
            <div class="kpi-sublabel">Current Sprint</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{sprint_health_score}/100</div>
            <div class="kpi-label">Sprint Health</div>
            <div class="kpi-sublabel">Composite Score</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total_initiatives}</div>
            <div class="kpi-label">Total Projects</div>
            <div class="kpi-sublabel">{completed_initiatives} Completed</div>
        </div>
        """, unsafe_allow_html=True)

    # ========================================================================
    # CHARTS ROW 1: Velocity, Impact/Effort Matrix, Team Heatmap
    # ========================================================================
    st.markdown('<div style="margin: 30px 0 15px 0;"></div>', unsafe_allow_html=True)

    chart1, chart2, chart3 = st.columns([1.2, 1.2, 1])

    with chart1:
        st.markdown('<div class="section-title">Velocity Trend</div>', unsafe_allow_html=True)
        velocity_chart = create_velocity_trend_chart(sprints_df)
        velocity_chart.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=40))
        st.plotly_chart(velocity_chart, use_container_width=True)

    with chart2:
        st.markdown('<div class="section-title">Impact vs Effort</div>', unsafe_allow_html=True)
        matrix_chart = create_impact_effort_matrix(initiatives_df)
        matrix_chart.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=40))
        st.plotly_chart(matrix_chart, use_container_width=True)

    with chart3:
        st.markdown('<div class="section-title">Team Performance</div>', unsafe_allow_html=True)

        # Create simplified heatmap data (last 6 sprints)
        team_sprint_metrics = []
        for sprint_num in sprints_df.tail(6)['sprint_number']:
            sprint_stories = stories_df[stories_df['sprint_number'] == sprint_num]
            for member_id in team_df['member_id'].head(6):  # Top 6 team members
                member = team_df[team_df['member_id'] == member_id].iloc[0]
                member_stories = sprint_stories[sprint_stories['assignee_id'] == member_id]
                points = member_stories['final_story_points'].sum()
                utilization = (points / member['avg_capacity_per_sprint'] * 100) if member['avg_capacity_per_sprint'] > 0 else 0

                team_sprint_metrics.append({
                    'member_name': member['name'].split()[0],  # First name only
                    'sprint_number': sprint_num,
                    'utilization_pct': utilization
                })

        heatmap_df = pd.DataFrame(team_sprint_metrics)
        heatmap_chart = create_capacity_heatmap(heatmap_df)
        heatmap_chart.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=40))
        st.plotly_chart(heatmap_chart, use_container_width=True)

    # ========================================================================
    # CHARTS ROW 2: Work Distribution Stacked Area Chart
    # ========================================================================
    st.markdown('<div style="margin: 25px 0 15px 0;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Work Distribution & Completion Trends</div>', unsafe_allow_html=True)

    story_type_by_sprint = calculate_story_type_distribution(stories_df)
    stacked_area = create_story_type_stacked_area(story_type_by_sprint)
    stacked_area.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=40))
    st.plotly_chart(stacked_area, use_container_width=True)

    # ========================================================================
    # STRATEGIC INSIGHTS & RECOMMENDATIONS
    # ========================================================================
    st.markdown('<div class="section-title">Strategic Insights & Recommendations</div>', unsafe_allow_html=True)

    # Generate recommendations
    quick_wins = get_quick_wins(initiatives_df)
    quick_wins_backlog = quick_wins[quick_wins['status'] == 'Backlog']
    time_sinks = get_time_sinks(initiatives_df)

    # Calculate velocity improvement
    velocity_change = ((sprints_df.tail(3)['velocity'].mean() - sprints_df.head(3)['velocity'].mean()) /
                      sprints_df.head(3)['velocity'].mean() * 100)

    # Risk assessment
    team_utilization = current_sprint['completed_points'] / current_sprint['team_capacity']
    risk_df = assess_all_initiatives_risk(initiatives_df, current_sprint_num, sprints_df, team_utilization)
    high_risk_count = len(risk_df[risk_df['risk_level'] == 'High']) if len(risk_df) > 0 else 0

    # Display recommendations
    st.markdown(f"""
    <div class="recommendation-box recommendation-box-green">
        <strong>✅ STRENGTH:</strong> Team velocity improved {velocity_change:.0f}% over 6 months - momentum building
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="recommendation-box recommendation-box-green">
        <strong>⚡ OPPORTUNITY:</strong> {len(quick_wins_backlog)} "Quick Win" initiatives ready for immediate delivery
    </div>
    """, unsafe_allow_html=True)

    if high_risk_count > 0:
        st.markdown(f"""
        <div class="recommendation-box recommendation-box-red">
            <strong>🚨 ALERT:</strong> {high_risk_count} initiatives flagged high-risk - realign scope or extend timeline
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="recommendation-box recommendation-box-orange">
        <strong>⚠️ OPTIMIZATION:</strong> Deprioritize {len(time_sinks)} "Time Sink" initiatives to free capacity
    </div>
    """, unsafe_allow_html=True)

    # Calculate predictability
    predictability = 1 - (sprints_df['velocity'].std() / sprints_df['velocity'].mean())

    st.markdown(f"""
    <div class="recommendation-box recommendation-box-green">
        <strong>📊 PREDICTABILITY:</strong> Sprint predictability at {predictability*100:.0f}% - reliable for forecasting
    </div>
    """, unsafe_allow_html=True)

    # ========================================================================
    # PROJECT RESULTS & BUSINESS VALUE
    # ========================================================================
    st.markdown("""
    <div class="results-box">
        <div class="results-title">
            ⭐ PROJECT RESULTS & BUSINESS VALUE ⭐
        </div>
        <div class="results-text">
            <strong>Simulated this dashboard with 6+ simulations across 4 pages including portfolio metrics,
            feature prioritization, sprint analytics, team performance insights, predictive forecasting,
            and strategic ROI analysis.</strong> Each simulation ran Monte Carlo models with 1000+ iterations
            to generate statistically significant delivery confidence intervals. Prioritized portfolio using
            multi-factor scoring (Impact × Effort × Strategic Fit × ROI) to surface actionable "Quick Wins" and
            flag resource-intensive "Time Sinks" for deprioritization.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ========================================================================
    # FOOTER - DIRECTOR ALIGNMENT
    # ========================================================================
    st.markdown("""
    <div class="footer-bar">
        DIRECTOR ALIGNMENT
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="target-role">
        <strong>Target Roles:</strong> Sr. PM (Revenue Ops) | Strategy & Operations<br>
        <strong>Relevant Companies:</strong> B2B SaaS | Custom Ink | Google | Meta | LinkedIn
    </div>
    """, unsafe_allow_html=True)
