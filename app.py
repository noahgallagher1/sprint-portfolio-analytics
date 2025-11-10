"""
Agile Sprint Performance & Portfolio Analytics Dashboard
Executive Presentation with Interactive Tabs

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
    create_initiative_funnel, create_treemap, create_roi_scatter,
    create_portfolio_quadrant_summary, COLORS
)

# Page config
st.set_page_config(
    page_title="Sprint Analytics Executive Presentation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Executive Presentation Style with Tabs
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

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: linear-gradient(90deg, #2e7d9e 0%, #3b9fc7 100%);
        padding: 15px 20px;
        border-radius: 8px 8px 0 0;
        margin-top: 10px;
        display: flex;
        justify-content: space-between;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 6px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        border: 2px solid transparent;
        flex: 1;
        text-align: center;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.3);
    }

    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #2e7d9e !important;
        border: 2px solid #2e7d9e !important;
        font-weight: 700;
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
        padding: 0 0 10px 0;
        font-style: italic;
    }

    /* KPI metric cards */
    .kpi-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 15px 10px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .kpi-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #2e7d9e;
        margin: 3px 0;
        line-height: 1.1;
    }

    .kpi-label {
        font-size: 0.7rem;
        color: #666;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        line-height: 1.2;
    }

    .kpi-sublabel {
        font-size: 0.65rem;
        color: #999;
        margin-top: 2px;
    }

    /* Section headers */
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #2d3748;
        margin: 15px 0 10px 0;
        padding-bottom: 6px;
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

    /* Contact buttons */
    .contact-button {
        display: inline-block;
        background: linear-gradient(135deg, #2e7d9e 0%, #3b9fc7 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 12px 5px 0 5px;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }

    .contact-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.25);
        text-decoration: none;
        color: white;
    }

    .linkedin-button {
        display: inline-block;
        background: linear-gradient(135deg, #0077B5 0%, #00A0DC 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 12px 5px 0 5px;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }

    .linkedin-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.25);
        text-decoration: none;
        color: white;
    }

    .github-button {
        display: inline-block;
        background: linear-gradient(135deg, #24292e 0%, #444d56 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 12px 5px 0 5px;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }

    .github-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.25);
        text-decoration: none;
        color: white;
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

    /* Table styling */
    .dataframe {
        font-size: 0.85rem;
    }

    h2, h3 {
        color: #2d3748 !important;
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
# LEFT SIDEBAR - PROJECT OVERVIEW (PERSISTENT ACROSS TABS)
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
        <div class="sidebar-text" style="line-height: 1.7;">
            <strong>→ Strategic Value:</strong><br>
            Optimize resource allocation across competing priorities
            <br><br>
            <strong>→ Delivery Confidence:</strong><br>
            Quantify delivery risk & capacity early
            <br><br>
            <strong>→ Portfolio ROI:</strong><br>
            75%+ effort on high-ROI initiatives
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
        noahgallagher1@gmail.com<br>
        <br>
        <a href="mailto:noahgallagher1@gmail.com?subject=Sprint%20Analytics%20Dashboard%20Inquiry" class="contact-button">
            📧 Contact Me
        </a>
        <a href="https://www.linkedin.com/in/noahgallagher/" target="_blank" rel="noopener noreferrer" class="linkedin-button">
            💼 LinkedIn
        </a>
        <a href="https://github.com/noahgallagher1/sprint-portfolio-analytics" target="_blank" rel="noopener noreferrer" class="github-button">
            🐙 GitHub
        </a>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT AREA WITH TABS
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

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Summary", "🎯 Portfolio & Strategy", "⚡ Delivery & Performance", "📚 About the Data"])

    # ========================================================================
    # TAB 1: EXECUTIVE SUMMARY
    # ========================================================================
    with tab1:
        st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)

        # KPI METRICS ROW
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

        # CHARTS ROW 1: Velocity, Impact/Effort Matrix, Team Heatmap
        st.markdown('<div style="margin: 30px 0 15px 0;"></div>', unsafe_allow_html=True)

        chart1, chart2, chart3 = st.columns([1.2, 1.2, 1])

        with chart1:
            st.markdown('<div class="section-title">Velocity Trend</div>', unsafe_allow_html=True)
            velocity_chart = create_velocity_trend_chart(sprints_df)
            velocity_chart.update_layout(height=240, margin=dict(l=30, r=10, t=20, b=30))
            st.plotly_chart(velocity_chart, use_container_width=True)

        with chart2:
            st.markdown('<div class="section-title">Portfolio Composition</div>', unsafe_allow_html=True)
            portfolio_chart = create_portfolio_quadrant_summary(initiatives_df)
            portfolio_chart.update_layout(height=240, margin=dict(l=30, r=10, t=10, b=30))
            st.plotly_chart(portfolio_chart, use_container_width=True)

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
            heatmap_chart.update_layout(height=240, margin=dict(l=30, r=10, t=20, b=30))
            st.plotly_chart(heatmap_chart, use_container_width=True)

        # CHARTS ROW 2: Work Distribution Stacked Area Chart
        st.markdown('<div style="margin: 20px 0 10px 0;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Work Distribution & Completion Trends</div>', unsafe_allow_html=True)

        story_type_by_sprint = calculate_story_type_distribution(stories_df)
        stacked_area = create_story_type_stacked_area(story_type_by_sprint)
        stacked_area.update_layout(height=220, margin=dict(l=30, r=10, t=10, b=30))
        st.plotly_chart(stacked_area, use_container_width=True)

        # STRATEGIC INSIGHTS & RECOMMENDATIONS (2-column layout)
        st.markdown('<div style="margin: 15px 0 10px 0;"></div>', unsafe_allow_html=True)
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

        # Display recommendations in 2-column layout
        rec_col1, rec_col2 = st.columns(2)

        with rec_col1:
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

            # Calculate predictability
            predictability = 1 - (sprints_df['velocity'].std() / sprints_df['velocity'].mean())

            st.markdown(f"""
            <div class="recommendation-box recommendation-box-green">
                <strong>📊 PREDICTABILITY:</strong> Sprint predictability at {predictability*100:.0f}% - reliable for forecasting
            </div>
            """, unsafe_allow_html=True)

        with rec_col2:
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

        # PROJECT RESULTS & BUSINESS VALUE
        st.markdown('<div style="margin: 15px 0 0 0;"></div>', unsafe_allow_html=True)
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
    # TAB 2: PORTFOLIO & STRATEGY
    # ========================================================================
    with tab2:
        st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)

        # Portfolio Prioritization Section
        st.markdown('<div class="section-title">Portfolio Prioritization Matrix</div>', unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])

        with col1:
            matrix_chart = create_impact_effort_matrix(initiatives_df)
            matrix_chart.update_layout(height=450, margin=dict(l=20, r=20, t=30, b=40))
            st.plotly_chart(matrix_chart, use_container_width=True)

        with col2:
            st.markdown("**Portfolio Composition**")
            composition = get_portfolio_composition(initiatives_df)

            fig = px.bar(composition, x='quadrant', y='initiative_count',
                        color='quadrant', color_discrete_map={
                            'Quick Wins': COLORS['success'],
                            'Major Projects': COLORS['primary'],
                            'Fill-ins': COLORS['neutral'],
                            'Time Sinks': COLORS['danger']
                        },
                        text='initiative_count',
                        labels={'initiative_count': 'Count', 'quadrant': 'Quadrant'})
            fig.update_traces(textposition='outside')
            fig.update_layout(showlegend=False, height=450)
            st.plotly_chart(fig, use_container_width=True)

        # Quick Wins and Time Sinks
        st.markdown('<div style="margin: 25px 0 15px 0;"></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="section-title">⚡ Top Quick Wins</div>', unsafe_allow_html=True)
            quick_wins = get_quick_wins(initiatives_df, limit=5)
            for _, init in quick_wins.iterrows():
                st.markdown(f"""
                <div class="recommendation-box recommendation-box-green">
                    <strong>{init['name']}</strong><br>
                    Impact: {init['impact_score']}/10 | Effort: {init['effort_score']}/10 |
                    Priority: {init['priority_score']:.2f}<br>
                    Status: {init['status']} | Points: {init['total_story_points']}
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="section-title">⚠️ Time Sinks to Deprioritize</div>', unsafe_allow_html=True)
            time_sinks = get_time_sinks(initiatives_df).head(5)
            for _, init in time_sinks.iterrows():
                st.markdown(f"""
                <div class="recommendation-box recommendation-box-orange">
                    <strong>{init['name']}</strong><br>
                    Impact: {init['impact_score']}/10 | Effort: {init['effort_score']}/10 |
                    Priority: {init['priority_score']:.2f}<br>
                    Status: {init['status']} | Points: {init['total_story_points']}
                </div>
                """, unsafe_allow_html=True)

        # Strategic Trends
        st.markdown('<div style="margin: 30px 0 15px 0;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Strategic Trends & ROI Analysis</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            # Velocity Stability
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=sprints_df['sprint_number'],
                y=sprints_df['velocity'],
                name='Velocity',
                mode='lines+markers',
                line=dict(color=COLORS['primary'], width=3)
            ))

            if 'velocity_rolling_avg' in sprints_df.columns:
                fig.add_trace(go.Scatter(
                    x=sprints_df['sprint_number'],
                    y=sprints_df['velocity_rolling_avg'],
                    name='3-Sprint Avg',
                    mode='lines',
                    line=dict(color=COLORS['warning'], width=2, dash='dash')
                ))

            fig.update_layout(
                title='Velocity Stability Over Time',
                xaxis_title='Sprint Number',
                yaxis_title='Story Points',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # ROI Scatter
            completed_initiatives = initiatives_df[initiatives_df['status'] == 'Completed']
            if len(completed_initiatives) > 0:
                roi_scatter = create_roi_scatter(completed_initiatives)
                roi_scatter.update_layout(height=350)
                st.plotly_chart(roi_scatter, use_container_width=True)

        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)

        early_velocity = sprints_df.head(3)['velocity'].mean()
        late_velocity = sprints_df.tail(3)['velocity'].mean()
        improvement = ((late_velocity - early_velocity) / early_velocity * 100)

        with col1:
            st.metric("Velocity Improvement", f"{improvement:.0f}%",
                     delta=f"{late_velocity - early_velocity:.0f} pts")

        with col2:
            predictability = 1 - (sprints_df['velocity'].std() / sprints_df['velocity'].mean())
            st.metric("Predictability", f"{predictability*100:.0f}%")

        with col3:
            success_rate = len(completed_initiatives) / len(initiatives_df) * 100 if len(initiatives_df) > 0 else 0
            st.metric("Initiative Success Rate", f"{success_rate:.0f}%")

        with col4:
            st.metric("Total Delivered", f"{sprints_df['completed_points'].sum():.0f} pts")

    # ========================================================================
    # TAB 3: DELIVERY & PERFORMANCE
    # ========================================================================
    with tab3:
        st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)

        # Sprint Selector
        st.markdown('<div class="section-title">Sprint Deep Dive</div>', unsafe_allow_html=True)

        selected_sprint = st.selectbox(
            "Select Sprint to Analyze",
            options=sprints_df['sprint_number'].tolist(),
            index=len(sprints_df) - 1
        )

        sprint_data = sprints_df[sprints_df['sprint_number'] == selected_sprint].iloc[0]
        sprint_stories = stories_df[stories_df['sprint_number'] == selected_sprint]

        # Sprint Overview
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Committed Points", int(sprint_data['committed_points']))
        with col2:
            st.metric("Completed Points", int(sprint_data['completed_points']))
        with col3:
            st.metric("Completion Rate", f"{sprint_data['completion_rate']*100:.0f}%")
        with col4:
            utilization = sprint_data['completed_points'] / sprint_data['team_capacity'] * 100
            st.metric("Capacity Utilization", f"{utilization:.0f}%")

        # Charts
        st.markdown('<div style="margin: 25px 0 15px 0;"></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            status_counts = sprint_stories['status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']

            fig = px.pie(status_counts, values='Count', names='Status',
                        title=f"Sprint {selected_sprint} Story Status")
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            completed_stories = sprint_stories[sprint_stories['status'] == 'Completed']
            if len(completed_stories) > 0:
                cycle_time_chart = create_cycle_time_boxplot(completed_stories)
                cycle_time_chart.update_layout(height=350)
                st.plotly_chart(cycle_time_chart, use_container_width=True)

        # Team Performance
        st.markdown('<div style="margin: 30px 0 15px 0;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Team Performance Analytics</div>', unsafe_allow_html=True)

        completed_stories_all = stories_df[stories_df['status'] == 'Completed']
        velocity_contrib = calculate_team_velocity_contribution(completed_stories_all, team_df)

        fig = px.bar(velocity_contrib, x='points_delivered', y='name', orientation='h',
                    color='points_delivered', color_continuous_scale='Blues',
                    text='points_delivered',
                    labels={'points_delivered': 'Story Points Delivered', 'name': 'Team Member'})
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

        # Predictive Insights
        st.markdown('<div style="margin: 30px 0 15px 0;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Predictive Insights & Risk Assessment</div>', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])

        with col1:
            health = calculate_sprint_health_score(current_sprint, sprints_df)
            health_gauge = create_health_gauge(health['health_score'])
            health_gauge.update_layout(height=300)
            st.plotly_chart(health_gauge, use_container_width=True)

            if health['health_score'] >= 80:
                st.success("✅ **Excellent** - Sprint on track")
            elif health['health_score'] >= 60:
                st.warning("⚠️ **Monitor** - Some concerns")
            else:
                st.error("❌ **At Risk** - Intervention needed")

        with col2:
            # Risk assessment
            team_utilization = current_sprint['completed_points'] / current_sprint['team_capacity']
            risk_df = assess_all_initiatives_risk(initiatives_df, current_sprint_num, sprints_df, team_utilization)

            if len(risk_df) > 0:
                risk_counts = risk_df['risk_level'].value_counts().reset_index()
                risk_counts.columns = ['Risk Level', 'Count']

                risk_colors = {'Low': COLORS['success'], 'Medium': COLORS['warning'], 'High': COLORS['danger']}
                fig = px.pie(risk_counts, values='Count', names='Risk Level',
                            color='Risk Level', color_discrete_map=risk_colors,
                            title='Initiative Risk Distribution')
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

        # Velocity Forecast
        st.markdown('<div style="margin: 25px 0 15px 0;"></div>', unsafe_allow_html=True)

        forecast = forecast_velocity_next_n_sprints(sprints_df, n_sprints=3)
        future_sprints = list(range(current_sprint_num + 1, current_sprint_num + 4))

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=sprints_df['sprint_number'],
            y=sprints_df['velocity'],
            name='Historical',
            mode='lines+markers',
            line=dict(color=COLORS['primary'], width=2)
        ))

        fig.add_trace(go.Scatter(
            x=future_sprints,
            y=forecast['forecast'],
            name='Forecast',
            mode='lines+markers',
            line=dict(color=COLORS['warning'], width=2, dash='dash')
        ))

        fig.update_layout(
            title='Velocity Forecast (Next 3 Sprints)',
            xaxis_title='Sprint Number',
            yaxis_title='Story Points',
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

    # ========================================================================
    # TAB 4: ABOUT THE DATA
    # ========================================================================
    with tab4:
        st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Understanding the Sprint Data</div>', unsafe_allow_html=True)

        st.markdown("""
        This dashboard analyzes **6 months of Agile sprint data** from a simulated software development team.
        The data represents realistic patterns and challenges faced by modern product teams.
        """)

        # Data Overview
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{len(sprints_df)}</div>
                <div class="kpi-label">Total Sprints</div>
                <div class="kpi-sublabel">2-week iterations</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{len(stories_df)}</div>
                <div class="kpi-label">User Stories</div>
                <div class="kpi-sublabel">Across all sprints</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{len(initiatives_df)}</div>
                <div class="kpi-label">Initiatives</div>
                <div class="kpi-sublabel">Strategic projects</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div style="margin: 25px 0 15px 0;"></div>', unsafe_allow_html=True)

        # Sprint Details
        st.markdown('<div class="section-title">Sprint Timeline & Context</div>', unsafe_allow_html=True)

        # Create sprint summary table
        sprint_summary = sprints_df[['sprint_number', 'committed_points', 'completed_points',
                                     'completion_rate', 'velocity']].copy()
        sprint_summary['completion_rate'] = (sprint_summary['completion_rate'] * 100).round(0).astype(int)
        sprint_summary.columns = ['Sprint #', 'Committed', 'Completed', 'Completion %', 'Velocity']

        st.markdown("""
        **Sprint Overview Table** - Select any sprint number in the "Delivery & Performance" tab to analyze specific metrics.
        """)

        st.dataframe(sprint_summary, use_container_width=True, hide_index=True)

        st.markdown('<div style="margin: 25px 0 15px 0;"></div>', unsafe_allow_html=True)

        # Data Composition
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="section-title">Story Type Breakdown</div>', unsafe_allow_html=True)

            story_types = stories_df['story_type'].value_counts().reset_index()
            story_types.columns = ['Story Type', 'Count']

            fig = px.pie(story_types, values='Count', names='Story Type',
                        color='Story Type',
                        color_discrete_map={
                            'Feature': COLORS['primary'],
                            'Bug': COLORS['danger'],
                            'Technical Debt': COLORS['warning'],
                            'Spike': COLORS['neutral']
                        })
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-title">Initiative Status</div>', unsafe_allow_html=True)

            initiative_status = initiatives_df['status'].value_counts().reset_index()
            initiative_status.columns = ['Status', 'Count']

            fig = px.bar(initiative_status, x='Status', y='Count',
                        color='Status',
                        color_discrete_map={
                            'Completed': COLORS['success'],
                            'Active': COLORS['primary'],
                            'Backlog': COLORS['neutral'],
                            'Deprioritized': COLORS['danger']
                        })
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div style="margin: 25px 0 15px 0;"></div>', unsafe_allow_html=True)

        # Key Definitions
        st.markdown('<div class="section-title">Key Terms & Metrics</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Sprint Metrics:**
            - **Velocity**: Total story points completed in a sprint
            - **Completion Rate**: % of committed points actually completed
            - **Sprint Health Score**: Composite metric (0-100) combining velocity consistency, completion rate, and estimation accuracy
            - **Cycle Time**: Days from story start to completion

            **Team Metrics:**
            - **Capacity Utilization**: % of team capacity used
            - **Estimation Accuracy**: How close final points are to initial estimates
            """)

        with col2:
            st.markdown("""
            **Portfolio Metrics:**
            - **Impact Score**: Business value rating (0-10)
            - **Effort Score**: Complexity & time required (0-10)
            - **Priority Score**: Calculated as (Impact × 10) / Effort
            - **ROI Estimate**: Expected return on investment (High/Medium/Low)

            **Risk Levels:**
            - **High Risk**: Initiatives with scope/timeline concerns
            - **Medium Risk**: Requires monitoring
            - **Low Risk**: On track for delivery
            """)

        st.markdown('<div style="margin: 25px 0 15px 0;"></div>', unsafe_allow_html=True)

        # How to Use This Dashboard
        st.markdown('<div class="section-title">How to Use This Dashboard</div>', unsafe_allow_html=True)

        st.markdown("""
        1. **Executive Summary Tab**: Get a high-level overview of team performance, key trends, and strategic recommendations
        2. **Portfolio & Strategy Tab**: Prioritize initiatives using the Impact/Effort matrix and identify Quick Wins vs Time Sinks
        3. **Delivery & Performance Tab**: Deep dive into specific sprints, analyze team performance, and view predictive insights
        4. **About the Data Tab** (this tab): Understand the data context and metric definitions

        **Navigation Tip**: Use the sprint selector dropdown in the Delivery & Performance tab to analyze any of the {len(sprints_df)} sprints in detail.
        """)

    # FOOTER (PERSISTENT ACROSS TABS)
    st.markdown("""
    <div class="footer-bar">
        DATA SCIENCE & ANALYTICS PORTFOLIO
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="target-role">
        <strong>Target Roles:</strong> Data Scientist | Analytics Engineer | Business Intelligence Analyst<br>
        <strong>Relevant Companies:</strong> Tech | SaaS | Finance | Healthcare | E-commerce
    </div>
    """, unsafe_allow_html=True)
