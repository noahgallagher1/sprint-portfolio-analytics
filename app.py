"""
Sprint Performance & Portfolio Analytics Dashboard

A comprehensive analytics dashboard for Agile teams demonstrating:
- Portfolio management and initiative prioritization
- Sprint performance tracking and predictive insights
- Team capacity analysis and bottleneck identification
- Data-driven recommendations for strategic decision-making

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
    page_title="Sprint Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
    }
    .success-card {
        border-left-color: #06A77D;
    }
    .warning-card {
        border-left-color: #f39c12;
    }
    .danger-card {
        border-left-color: #e74c3c;
    }
    .recommendation {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #2E86AB;
    }
    h1 {
        color: #2E86AB;
    }
    h2 {
        color: #2E86AB;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load and prepare all data"""
    data = load_all_data()

    # Add rolling metrics to sprints
    data['sprints'] = calculate_rolling_metrics(data['sprints'])

    # Add priority scores and quadrants to initiatives
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

# Sidebar navigation
st.sidebar.title("📊 Sprint Analytics")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    [
        "🎯 Executive Summary",
        "📋 Portfolio Prioritization",
        "🔍 Sprint Deep Dive",
        "👥 Team Performance",
        "🔮 Predictive Insights",
        "📈 Strategic Trends"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    """
    This dashboard provides comprehensive analytics for Agile teams,
    demonstrating portfolio management, predictive insights, and
    data-driven decision-making capabilities.

    **Key Features:**
    - Initiative prioritization
    - Sprint health scoring
    - Risk assessment
    - Capacity planning
    - Strategic recommendations
    """
)

# Get current sprint info
current_sprint = get_current_sprint(sprints_df)
current_sprint_num = int(current_sprint['sprint_number'])

# ============================================================================
# PAGE 1: EXECUTIVE SUMMARY
# ============================================================================
if page == "🎯 Executive Summary":
    st.title("🎯 Executive Summary")
    st.markdown("**High-level overview of team performance and portfolio health**")
    st.markdown("---")

    # Top KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)

    # Calculate key metrics
    avg_velocity_l3 = sprints_df.tail(3)['velocity'].mean()
    completion_rate = sprints_df['completion_rate'].mean()
    active_initiatives = len(initiatives_df[initiatives_df['status'] == 'Active'])

    # Risk assessment
    team_utilization = current_sprint['completed_points'] / current_sprint['team_capacity']
    risk_df = assess_all_initiatives_risk(initiatives_df, current_sprint_num, sprints_df, team_utilization)
    high_risk_count = len(risk_df[risk_df['risk_level'] == 'High'])

    # Sprint health
    health = calculate_sprint_health_score(current_sprint, sprints_df)

    with col1:
        st.metric("Current Velocity", f"{int(current_sprint['velocity'])} pts",
                 delta=f"{int(current_sprint['velocity'] - avg_velocity_l3)}")

    with col2:
        trend = calculate_velocity_trend(sprints_df)
        st.metric("Avg Velocity (L3)", f"{int(avg_velocity_l3)} pts",
                 delta=trend['trend'])

    with col3:
        st.metric("Completion Rate", f"{completion_rate*100:.0f}%",
                 delta=f"{(current_sprint['completion_rate'] - completion_rate)*100:.0f}%")

    with col4:
        st.metric("Active Initiatives", active_initiatives,
                 delta=None)

    with col5:
        st.metric("High-Risk Initiatives", high_risk_count,
                 delta=None, delta_color="inverse")

    st.markdown("---")

    # Row 1: Velocity Trend and Current Sprint Burndown
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 Velocity Trend")
        velocity_chart = create_velocity_trend_chart(sprints_df)
        st.plotly_chart(velocity_chart, use_container_width=True)

    with col2:
        st.subheader("🔥 Current Sprint Burndown")
        # Simulate burndown (in real app, would use actual daily data)
        days_elapsed = 7  # Assume mid-sprint
        burndown_chart = create_burndown_chart(
            current_sprint['committed_points'],
            current_sprint['completed_points'],
            days_in_sprint=14,
            days_elapsed=days_elapsed
        )
        st.plotly_chart(burndown_chart, use_container_width=True)

    # Row 2: Portfolio Health and Sprint Health
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Portfolio Health")
        portfolio_health = calculate_portfolio_health_score(initiatives_df)

        # Status distribution pie chart
        status_counts = initiatives_df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']

        status_colors = {
            'Completed': COLORS['success'],
            'Active': COLORS['primary'],
            'Backlog': COLORS['neutral'],
            'Deprioritized': COLORS['danger']
        }

        fig = px.pie(status_counts, values='Count', names='Status',
                    color='Status', color_discrete_map=status_colors,
                    title=f"Portfolio Health: {portfolio_health['health_score']:.0f}/100")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💚 Sprint Health Score")
        health_gauge = create_health_gauge(health['health_score'], "Sprint Health")
        st.plotly_chart(health_gauge, use_container_width=True)

        # Health components
        st.markdown("**Health Components:**")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Velocity Consistency", f"{health['velocity_consistency']:.0f}%")
            st.metric("Completion Rate", f"{health['completion_rate']:.0f}%")
        with col_b:
            st.metric("Estimation Accuracy", f"{health['estimation_accuracy']:.0f}%")
            st.metric("Blocker Impact", f"{health['blocker_impact']:.0f}%")

    # Key Insights
    st.markdown("---")
    st.subheader("🔍 Key Business Insights")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        velocity_change = ((sprints_df.tail(3)['velocity'].mean() - sprints_df.head(3)['velocity'].mean()) /
                          sprints_df.head(3)['velocity'].mean() * 100)
        st.markdown(f"""
        <div class="metric-card success-card">
            <h3>📊 Velocity Growth</h3>
            <p>Team velocity improved <b>{velocity_change:.0f}%</b> over 6 months</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        quick_wins = get_quick_wins(initiatives_df)
        quick_wins_backlog = quick_wins[quick_wins['status'] == 'Backlog']
        st.markdown(f"""
        <div class="metric-card success-card">
            <h3>⚡ Quick Wins Ready</h3>
            <p><b>{len(quick_wins_backlog)}</b> high-impact, low-effort initiatives ready for Q1</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        predictability = 1 - (sprints_df['velocity'].std() / sprints_df['velocity'].mean())
        st.markdown(f"""
        <div class="metric-card success-card">
            <h3>🎯 Predictability</h3>
            <p>Sprint predictability at <b>{predictability*100:.0f}%</b></p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        # Completion probability for next sprint
        velocities = sprints_df['velocity'].values
        next_sprint_commitment = int(avg_velocity_l3 * 0.95)
        prob = predict_sprint_completion_probability(next_sprint_commitment, velocities)
        st.markdown(f"""
        <div class="metric-card success-card">
            <h3>🔮 Next Sprint</h3>
            <p><b>{prob['probability']*100:.0f}%</b> probability of completing {next_sprint_commitment} points</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# PAGE 2: PORTFOLIO PRIORITIZATION
# ============================================================================
elif page == "📋 Portfolio Prioritization":
    st.title("📋 Portfolio Prioritization")
    st.markdown("**Initiative intake, scoring, and backlog management**")
    st.markdown("---")

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            options=['All'] + list(initiatives_df['status'].unique()),
            default=['All']
        )

    with col2:
        category_filter = st.multiselect(
            "Strategic Alignment",
            options=['All'] + list(initiatives_df['strategic_category'].unique()),
            default=['All']
        )

    with col3:
        owner_filter = st.multiselect(
            "Owner",
            options=['All'] + list(initiatives_df['owner'].unique()),
            default=['All']
        )

    # Apply filters
    filtered_initiatives = initiatives_df.copy()
    if 'All' not in status_filter and status_filter:
        filtered_initiatives = filtered_initiatives[filtered_initiatives['status'].isin(status_filter)]
    if 'All' not in category_filter and category_filter:
        filtered_initiatives = filtered_initiatives[filtered_initiatives['strategic_category'].isin(category_filter)]
    if 'All' not in owner_filter and owner_filter:
        filtered_initiatives = filtered_initiatives[filtered_initiatives['owner'].isin(owner_filter)]

    st.markdown("---")

    # Row 1: Impact vs Effort Matrix
    st.subheader("🎯 Impact vs Effort Priority Matrix")
    st.markdown("*Initiatives categorized by business impact and effort required*")

    matrix_chart = create_impact_effort_matrix(filtered_initiatives)
    st.plotly_chart(matrix_chart, use_container_width=True)

    # Row 2: Intake Funnel and Portfolio Composition
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📥 Initiative Intake Funnel")
        funnel_data = create_intake_funnel_data(initiatives_df)
        funnel_chart = create_initiative_funnel(funnel_data)
        st.plotly_chart(funnel_chart, use_container_width=True)

    with col2:
        st.subheader("📊 Portfolio Composition")
        composition = get_portfolio_composition(initiatives_df)

        fig = px.bar(composition, x='quadrant', y='initiative_count',
                    color='quadrant', color_discrete_map={
                        'Quick Wins': COLORS['success'],
                        'Major Projects': COLORS['primary'],
                        'Fill-ins': COLORS['neutral'],
                        'Time Sinks': COLORS['danger']
                    },
                    text='initiative_count',
                    labels={'initiative_count': 'Number of Initiatives', 'quadrant': 'Quadrant'})
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Row 3: Portfolio Backlog Table
    st.subheader("📋 Portfolio Backlog")
    st.markdown("*Sortable table of all initiatives with priority scores*")

    # Prepare display dataframe
    display_df = filtered_initiatives[[
        'name', 'owner', 'impact_score', 'effort_score', 'priority_score',
        'priority_rank', 'quadrant', 'status', 'total_story_points',
        'completed_story_points', 'strategic_category', 'roi_estimate'
    ]].copy()

    display_df['completion_%'] = (display_df['completed_story_points'] /
                                   display_df['total_story_points'] * 100).fillna(0).round(0)

    display_df = display_df.sort_values('priority_score', ascending=False)

    # Style the dataframe
    def highlight_quadrant(row):
        if row['quadrant'] == 'Quick Wins':
            return ['background-color: #d4edda'] * len(row)
        elif row['quadrant'] == 'Time Sinks':
            return ['background-color: #f8d7da'] * len(row)
        else:
            return [''] * len(row)

    st.dataframe(
        display_df.style.apply(highlight_quadrant, axis=1),
        use_container_width=True,
        height=400
    )

    # Quick Wins and Time Sinks
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚡ Top Quick Wins")
        quick_wins = get_quick_wins(initiatives_df, limit=5)
        for _, init in quick_wins.iterrows():
            st.markdown(f"""
            <div class="recommendation">
                <b>{init['name']}</b><br>
                Impact: {init['impact_score']}/10 | Effort: {init['effort_score']}/10 |
                Priority: {init['priority_score']:.2f}<br>
                Status: {init['status']} | Points: {init['total_story_points']}
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.subheader("⚠️ Time Sinks to Deprioritize")
        time_sinks = get_time_sinks(initiatives_df).head(5)
        for _, init in time_sinks.iterrows():
            st.markdown(f"""
            <div class="recommendation">
                <b>{init['name']}</b><br>
                Impact: {init['impact_score']}/10 | Effort: {init['effort_score']}/10 |
                Priority: {init['priority_score']:.2f}<br>
                Status: {init['status']} | Points: {init['total_story_points']}
            </div>
            """, unsafe_allow_html=True)

    # Recommendations
    st.markdown("---")
    st.subheader("💡 Portfolio Recommendations")

    recommendations = generate_portfolio_recommendations(initiatives_df, sprints_df)
    for rec in recommendations:
        priority_color = "danger" if rec['priority'] == 'High' else "warning"
        st.markdown(f"""
        <div class="recommendation {priority_color}-card">
            <h4>🎯 {rec['title']}</h4>
            <p><b>Type:</b> {rec['type']} | <b>Priority:</b> {rec['priority']}</p>
            <p>{rec['description']}</p>
            <p><b>Action:</b> {rec['action']}</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# PAGE 3: SPRINT DEEP DIVE
# ============================================================================
elif page == "🔍 Sprint Deep Dive":
    st.title("🔍 Sprint Deep Dive")
    st.markdown("**Detailed sprint performance analysis**")
    st.markdown("---")

    # Sprint selector
    selected_sprint = st.selectbox(
        "Select Sprint",
        options=sprints_df['sprint_number'].tolist(),
        index=len(sprints_df) - 1
    )

    sprint_data = sprints_df[sprints_df['sprint_number'] == selected_sprint].iloc[0]
    sprint_stories = stories_df[stories_df['sprint_number'] == selected_sprint]

    # Sprint Overview Cards
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

    st.markdown("---")

    # Row 1: Story Status and Type Mix
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Story Completion Distribution")
        status_counts = sprint_stories['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']

        fig = px.pie(status_counts, values='Count', names='Status',
                    title=f"Sprint {selected_sprint} Story Status")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎨 Story Type Distribution")
        type_counts = sprint_stories['story_type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']

        fig = px.bar(type_counts, x='Type', y='Count', color='Type',
                    title=f"Sprint {selected_sprint} Story Types")
        st.plotly_chart(fig, use_container_width=True)

    # Row 2: Cycle Time Analysis
    st.subheader("⏱️ Cycle Time Analysis")

    completed_stories = sprint_stories[sprint_stories['status'] == 'Completed']
    if len(completed_stories) > 0:
        cycle_time_chart = create_cycle_time_boxplot(completed_stories)
        st.plotly_chart(cycle_time_chart, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Mean Cycle Time", f"{completed_stories['cycle_time_days'].mean():.1f} days")
        with col2:
            st.metric("Median Cycle Time", f"{completed_stories['cycle_time_days'].median():.1f} days")
        with col3:
            st.metric("Std Dev", f"{completed_stories['cycle_time_days'].std():.1f} days")
    else:
        st.info("No completed stories in this sprint yet.")

    # Row 3: Blocker Analysis
    st.subheader("🚧 Blocker Impact")

    blocked_stories = sprint_stories[sprint_stories['num_blockers'] > 0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Stories with Blockers", len(blocked_stories))
    with col2:
        blocker_rate = len(blocked_stories) / len(sprint_stories) * 100 if len(sprint_stories) > 0 else 0
        st.metric("Blocker Rate", f"{blocker_rate:.0f}%")
    with col3:
        avg_delay = blocked_stories['blocker_duration_days'].mean() if len(blocked_stories) > 0 else 0
        st.metric("Avg Blocker Delay", f"{avg_delay:.1f} days")

    if len(blocked_stories) > 0:
        st.markdown("**Stories with Blockers:**")
        blocker_df = blocked_stories[['story_id', 'story_type', 'story_points',
                                      'num_blockers', 'blocker_duration_days', 'status']]
        st.dataframe(blocker_df, use_container_width=True)

    # Sprint Comparison
    st.markdown("---")
    st.subheader("📊 Sprint-over-Sprint Comparison")

    if selected_sprint > 1:
        prev_sprint = sprints_df[sprints_df['sprint_number'] == selected_sprint - 1].iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            velocity_delta = sprint_data['velocity'] - prev_sprint['velocity']
            st.metric("Velocity Change", f"{velocity_delta:+.0f} pts",
                     delta=f"{velocity_delta/prev_sprint['velocity']*100:+.0f}%")

        with col2:
            completion_delta = sprint_data['completion_rate'] - prev_sprint['completion_rate']
            st.metric("Completion Rate Change", f"{completion_delta*100:+.0f}%",
                     delta=f"{completion_delta*100:+.0f}%")

        with col3:
            prev_sprint_stories = stories_df[stories_df['sprint_number'] == selected_sprint - 1]
            prev_cycle_time = prev_sprint_stories['cycle_time_days'].mean()
            curr_cycle_time = sprint_stories['cycle_time_days'].mean()
            cycle_delta = curr_cycle_time - prev_cycle_time
            st.metric("Avg Cycle Time Change", f"{cycle_delta:+.1f} days",
                     delta=f"{cycle_delta:+.1f}", delta_color="inverse")

        with col4:
            prev_bug_ratio = len(prev_sprint_stories[prev_sprint_stories['story_type']=='Bug']) / len(prev_sprint_stories)
            curr_bug_ratio = len(sprint_stories[sprint_stories['story_type']=='Bug']) / len(sprint_stories)
            bug_delta = (curr_bug_ratio - prev_bug_ratio) * 100
            st.metric("Bug Ratio Change", f"{bug_delta:+.0f}%",
                     delta=f"{bug_delta:+.0f}%", delta_color="inverse")


# ============================================================================
# PAGE 4: TEAM PERFORMANCE
# ============================================================================
elif page == "👥 Team Performance":
    st.title("👥 Team Performance")
    st.markdown("**Individual and team capacity analysis**")
    st.markdown("---")

    # Team velocity contribution
    st.subheader("📊 Individual Velocity Contribution")

    completed_stories_all = stories_df[stories_df['status'] == 'Completed']
    velocity_contrib = calculate_team_velocity_contribution(completed_stories_all, team_df)

    fig = px.bar(velocity_contrib, x='points_delivered', y='name', orientation='h',
                color='points_delivered', color_continuous_scale='Blues',
                text='points_delivered',
                labels={'points_delivered': 'Story Points Delivered', 'name': 'Team Member'})
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Team member details
    col1, col2, col3 = st.columns(3)
    for idx, (_, member) in enumerate(velocity_contrib.head(3).iterrows()):
        with [col1, col2, col3][idx]:
            st.markdown(f"""
            <div class="metric-card">
                <h4>{member['name']}</h4>
                <p><b>Role:</b> {member['role']}</p>
                <p><b>Points:</b> {member['points_delivered']:.0f} ({member['percentage']:.1f}%)</p>
                <p><b>Stories:</b> {member['stories_completed']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Capacity Utilization Heatmap
    st.subheader("🔥 Capacity Utilization Heatmap")
    st.markdown("*Green (70-95%): Healthy | Yellow (95-105%): At Capacity | Red (>105%): Over-utilized*")

    # Prepare heatmap data
    team_sprint_metrics = []
    for sprint_num in sprints_df['sprint_number']:
        sprint_stories = stories_df[stories_df['sprint_number'] == sprint_num]
        for member_id in team_df['member_id']:
            member = team_df[team_df['member_id'] == member_id].iloc[0]
            member_stories = sprint_stories[sprint_stories['assignee_id'] == member_id]
            points = member_stories['final_story_points'].sum()
            utilization = (points / member['avg_capacity_per_sprint'] * 100) if member['avg_capacity_per_sprint'] > 0 else 0

            team_sprint_metrics.append({
                'member_name': member['name'],
                'sprint_number': sprint_num,
                'utilization_pct': utilization
            })

    heatmap_df = pd.DataFrame(team_sprint_metrics)
    heatmap_chart = create_capacity_heatmap(heatmap_df)
    st.plotly_chart(heatmap_chart, use_container_width=True)

    # Estimation Accuracy
    st.markdown("---")
    st.subheader("🎯 Estimation Accuracy by Team Member")

    member_accuracy = stories_df.groupby('assignee_id').agg({
        'estimation_accuracy': 'mean',
        'story_points': 'sum',
        'story_id': 'count'
    }).reset_index()

    member_accuracy = member_accuracy.merge(team_df[['member_id', 'name']],
                                           left_on='assignee_id', right_on='member_id')
    member_accuracy = member_accuracy.sort_values('estimation_accuracy', ascending=False)

    fig = px.bar(member_accuracy, x='name', y='estimation_accuracy',
                color='estimation_accuracy', color_continuous_scale='RdYlGn',
                range_color=[0, 1],
                labels={'estimation_accuracy': 'Accuracy (0-1)', 'name': 'Team Member'},
                title='Average Estimation Accuracy')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Work Distribution by Role
    st.markdown("---")
    st.subheader("🎨 Work Distribution by Role")

    role_distribution = calculate_work_distribution_by_role(stories_df, team_df)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(role_distribution, values='total_points', names='role',
                    title='Story Points by Role')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(role_distribution, x='role', y='story_count',
                    color='role', text='story_count',
                    title='Number of Stories by Role')
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Bottleneck Identification
    st.markdown("---")
    st.subheader("🚧 Identified Bottlenecks")

    bottlenecks = identify_bottlenecks(stories_df, team_df)

    if bottlenecks:
        for bottleneck in bottlenecks:
            impact_class = "danger" if bottleneck['impact'] == 'high' else "warning"
            st.markdown(f"""
            <div class="recommendation {impact_class}-card">
                <h4>{bottleneck['type']} Bottleneck</h4>
                <p><b>Impact:</b> {bottleneck['impact'].title()}</p>
                <p>{bottleneck['description']}</p>
                <p><b>Recommendation:</b> {bottleneck['recommendation']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No significant bottlenecks identified!")


# ============================================================================
# PAGE 5: PREDICTIVE INSIGHTS & RISK SCORING
# ============================================================================
elif page == "🔮 Predictive Insights":
    st.title("🔮 Predictive Insights & Risk Scoring")
    st.markdown("**Forward-looking analytics and risk assessment**")
    st.markdown("---")

    # Sprint Health Score
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("💚 Sprint Health")
        health = calculate_sprint_health_score(current_sprint, sprints_df)
        health_gauge = create_health_gauge(health['health_score'])
        st.plotly_chart(health_gauge, use_container_width=True)

        # Health status
        if health['health_score'] >= 80:
            st.success("✅ **Excellent** - Sprint on track")
        elif health['health_score'] >= 60:
            st.warning("⚠️ **Monitor** - Some concerns")
        else:
            st.error("❌ **At Risk** - Intervention needed")

    with col2:
        st.subheader("📊 Health Components Breakdown")

        health_df = pd.DataFrame({
            'Component': ['Velocity\nConsistency', 'Estimation\nAccuracy',
                         'Completion\nRate', 'Blocker\nImpact'],
            'Score': [health['velocity_consistency'], health['estimation_accuracy'],
                     health['completion_rate'], health['blocker_impact']]
        })

        fig = px.bar(health_df, x='Component', y='Score',
                    color='Score', color_continuous_scale='RdYlGn',
                    range_color=[0, 100],
                    text='Score')
        fig.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Next Sprint Completion Probability
    st.subheader("🎲 Next Sprint Completion Probability")
    st.markdown("*Monte Carlo simulation based on historical velocity patterns*")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("**Simulation Parameters:**")
        avg_velocity = sprints_df.tail(3)['velocity'].mean()
        recommended_commitment = int(avg_velocity * 0.95)

        committed_points_input = st.slider(
            "Committed Points for Next Sprint",
            min_value=20,
            max_value=70,
            value=recommended_commitment,
            step=5
        )

        st.info(f"📊 **Recommended:** {recommended_commitment} points (95% of avg velocity)")

    with col2:
        # Run simulation
        velocities = sprints_df['velocity'].values
        prediction = predict_sprint_completion_probability(committed_points_input, velocities, n_simulations=1000)

        prob_chart_data = calculate_probability_distribution_chart_data(
            committed_points_input, velocities, n_simulations=1000
        )
        prob_chart = create_completion_probability_chart(prob_chart_data)
        st.plotly_chart(prob_chart, use_container_width=True)

    # Prediction summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Completion Probability", f"{prediction['probability']*100:.0f}%")
    with col2:
        st.metric("Expected Velocity", f"{prediction['expected_velocity']:.0f} pts")
    with col3:
        st.metric("90% Confidence Range",
                 f"{prediction['confidence_interval_10']:.0f}-{prediction['confidence_interval_90']:.0f}")

    st.markdown("---")

    # Initiative Risk Assessment
    st.subheader("⚠️ Initiative Delivery Risk Assessment")

    team_utilization = current_sprint['completed_points'] / current_sprint['team_capacity']
    risk_df = assess_all_initiatives_risk(initiatives_df, current_sprint_num, sprints_df, team_utilization)

    if len(risk_df) > 0:
        # Risk distribution
        col1, col2 = st.columns(2)

        with col1:
            risk_counts = risk_df['risk_level'].value_counts().reset_index()
            risk_counts.columns = ['Risk Level', 'Count']

            risk_colors = {'Low': COLORS['success'], 'Medium': COLORS['warning'], 'High': COLORS['danger']}
            fig = px.pie(risk_counts, values='Count', names='Risk Level',
                        color='Risk Level', color_discrete_map=risk_colors,
                        title='Initiative Risk Distribution')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Risk Summary:**")
            high_risk = len(risk_df[risk_df['risk_level'] == 'High'])
            medium_risk = len(risk_df[risk_df['risk_level'] == 'Medium'])
            low_risk = len(risk_df[risk_df['risk_level'] == 'Low'])

            st.metric("High Risk", high_risk, delta=None, delta_color="inverse")
            st.metric("Medium Risk", medium_risk)
            st.metric("Low Risk", low_risk, delta=None, delta_color="normal")

        # High-risk initiatives table
        st.markdown("**High-Risk Initiatives Requiring Attention:**")
        high_risk_initiatives = risk_df[risk_df['risk_level'].isin(['High', 'Medium'])].head(10)

        display_risk_df = high_risk_initiatives[[
            'name', 'status', 'risk_level', 'risk_score',
            'remaining_points', 'sprints_available', 'recommendation'
        ]].copy()

        display_risk_df['risk_score'] = display_risk_df['risk_score'].round(2)

        def highlight_risk(row):
            if row['risk_level'] == 'High':
                return ['background-color: #f8d7da'] * len(row)
            elif row['risk_level'] == 'Medium':
                return ['background-color: #fff3cd'] * len(row)
            else:
                return [''] * len(row)

        st.dataframe(
            display_risk_df.style.apply(highlight_risk, axis=1),
            use_container_width=True,
            height=400
        )
    else:
        st.info("No active or backlog initiatives to assess.")

    # Capacity Forecast
    st.markdown("---")
    st.subheader("📈 Capacity Planning Forecast")
    st.markdown("*Projected velocity for next 3 sprints*")

    forecast = forecast_velocity_next_n_sprints(sprints_df, n_sprints=3)

    # Create forecast chart
    future_sprints = list(range(current_sprint_num + 1, current_sprint_num + 4))

    fig = go.Figure()

    # Historical velocity
    fig.add_trace(go.Scatter(
        x=sprints_df['sprint_number'],
        y=sprints_df['velocity'],
        name='Historical',
        mode='lines+markers',
        line=dict(color=COLORS['primary'], width=2)
    ))

    # Forecast
    fig.add_trace(go.Scatter(
        x=future_sprints,
        y=forecast['forecast'],
        name='Forecast',
        mode='lines+markers',
        line=dict(color=COLORS['warning'], width=2, dash='dash')
    ))

    # Confidence bands
    fig.add_trace(go.Scatter(
        x=future_sprints + future_sprints[::-1],
        y=forecast['upper_bound'] + forecast['lower_bound'][::-1],
        fill='toself',
        fillcolor='rgba(243, 156, 18, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Confidence Interval'
    ))

    fig.update_layout(
        title='Velocity Forecast (Next 3 Sprints)',
        xaxis_title='Sprint Number',
        yaxis_title='Story Points',
        hovermode='x unified',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # Recommendations
    st.markdown("---")
    st.subheader("💡 Data-Driven Recommendations")

    recommendations = generate_predictive_recommendations(sprints_df, stories_df, initiatives_df, team_df)

    for rec in recommendations:
        priority_class = "danger" if rec['priority'] == 'High' else "warning"
        st.markdown(f"""
        <div class="recommendation {priority_class}-card">
            <h4>{rec['category']}</h4>
            <p><b>Priority:</b> {rec['priority']}</p>
            <p><b>Insight:</b> {rec['insight']}</p>
            <p><b>Recommendation:</b> {rec['recommendation']}</p>
            <p><i>Impact: {rec['impact']}</i></p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# PAGE 6: STRATEGIC TRENDS & ROI ANALYSIS
# ============================================================================
elif page == "📈 Strategic Trends":
    st.title("📈 Strategic Trends & ROI Analysis")
    st.markdown("**Long-term patterns and business impact**")
    st.markdown("---")

    # Velocity Stability Curve
    st.subheader("📊 Velocity Stability Over Time")
    st.markdown("*How team velocity has stabilized and become more predictable*")

    sprints_with_std = sprints_df.copy()

    fig = go.Figure()

    # Mean velocity
    fig.add_trace(go.Scatter(
        x=sprints_with_std['sprint_number'],
        y=sprints_with_std['velocity'],
        name='Velocity',
        mode='lines+markers',
        line=dict(color=COLORS['primary'], width=3)
    ))

    # Rolling average
    if 'velocity_rolling_avg' in sprints_with_std.columns:
        fig.add_trace(go.Scatter(
            x=sprints_with_std['sprint_number'],
            y=sprints_with_std['velocity_rolling_avg'],
            name='3-Sprint Avg',
            mode='lines',
            line=dict(color=COLORS['warning'], width=2, dash='dash')
        ))

        # Confidence bands
        if 'velocity_rolling_std' in sprints_with_std.columns:
            upper_band = sprints_with_std['velocity_rolling_avg'] + sprints_with_std['velocity_rolling_std']
            lower_band = sprints_with_std['velocity_rolling_avg'] - sprints_with_std['velocity_rolling_std']

            fig.add_trace(go.Scatter(
                x=sprints_with_std['sprint_number'].tolist() + sprints_with_std['sprint_number'].tolist()[::-1],
                y=upper_band.tolist() + lower_band.tolist()[::-1],
                fill='toself',
                fillcolor='rgba(46, 134, 171, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='±1 Std Dev'
            ))

    fig.update_layout(
        xaxis_title='Sprint Number',
        yaxis_title='Story Points',
        hovermode='x unified',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # Key metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        early_velocity = sprints_df.head(3)['velocity'].mean()
        late_velocity = sprints_df.tail(3)['velocity'].mean()
        improvement = ((late_velocity - early_velocity) / early_velocity * 100)
        st.metric("Velocity Improvement", f"{improvement:.0f}%",
                 delta=f"{late_velocity - early_velocity:.0f} pts")

    with col2:
        early_std = sprints_df.head(6)['velocity'].std()
        late_std = sprints_df.tail(6)['velocity'].std()
        stability_improvement = ((early_std - late_std) / early_std * 100)
        st.metric("Stability Improvement", f"{stability_improvement:.0f}%",
                 help="Lower variance = higher predictability")

    with col3:
        predictability = 1 - (sprints_df['velocity'].std() / sprints_df['velocity'].mean())
        st.metric("Overall Predictability", f"{predictability*100:.0f}%")

    st.markdown("---")

    # Estimation Accuracy Learning Curve
    st.subheader("🎯 Estimation Accuracy Learning Curve")

    accuracy_by_sprint = stories_df.groupby('sprint_number').agg({
        'estimation_accuracy': 'mean'
    }).reset_index()

    fig = px.line(accuracy_by_sprint, x='sprint_number', y='estimation_accuracy',
                 markers=True,
                 labels={'sprint_number': 'Sprint Number',
                        'estimation_accuracy': 'Estimation Accuracy'},
                 title='Team Estimation Calibration Over Time')

    # Add goal line
    fig.add_hline(y=0.85, line_dash="dash", line_color="green",
                 annotation_text="Target: 85%", annotation_position="right")

    fig.update_layout(height=400, yaxis_range=[0, 1])
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        early_accuracy = accuracy_by_sprint.head(3)['estimation_accuracy'].mean()
        st.metric("Early Accuracy (Sprints 1-3)", f"{early_accuracy*100:.0f}%")
    with col2:
        late_accuracy = accuracy_by_sprint.tail(3)['estimation_accuracy'].mean()
        st.metric("Recent Accuracy (Last 3)", f"{late_accuracy*100:.0f}%")

    st.markdown("---")

    # Work Composition Evolution
    st.subheader("🎨 Work Composition Evolution")
    st.markdown("*How the mix of Features, Bugs, and Technical Debt has changed*")

    story_type_by_sprint = calculate_story_type_distribution(stories_df)
    stacked_area = create_story_type_stacked_area(story_type_by_sprint)
    st.plotly_chart(stacked_area, use_container_width=True)

    # Quality trend
    quality_trend = calculate_quality_trend(stories_df)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(quality_trend, x='sprint_number', y='bug_ratio_pct',
                     markers=True,
                     labels={'sprint_number': 'Sprint Number', 'bug_ratio_pct': 'Bug Ratio (%)'},
                     title='Bug Ratio Trend')
        fig.add_hline(y=25, line_dash="dash", line_color="red",
                     annotation_text="Warning: >25%", annotation_position="right")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        early_bug_ratio = quality_trend.head(3)['bug_ratio_pct'].mean()
        late_bug_ratio = quality_trend.tail(3)['bug_ratio_pct'].mean()
        bug_reduction = early_bug_ratio - late_bug_ratio

        st.markdown(f"""
        <div class="metric-card success-card">
            <h3>🐛 Quality Improvement</h3>
            <p>Bug ratio decreased by <b>{bug_reduction:.1f}%</b></p>
            <p>From {early_bug_ratio:.1f}% (early) to {late_bug_ratio:.1f}% (recent)</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <h3>📦 Total Delivery</h3>
            <p><b>{sprints_df['completed_points'].sum():.0f}</b> story points delivered</p>
            <p>Across {len(sprints_df)} sprints ({len(stories_df)} stories)</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Initiative Throughput
    st.subheader("🚀 Initiative Throughput & Success Rate")

    completed_initiatives = initiatives_df[initiatives_df['status'] == 'Completed']
    deprioritized_initiatives = initiatives_df[initiatives_df['status'] == 'Deprioritized']

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Initiatives", len(initiatives_df))
    with col2:
        st.metric("Completed", len(completed_initiatives))
    with col3:
        success_rate = len(completed_initiatives) / (len(completed_initiatives) + len(deprioritized_initiatives)) * 100 if (len(completed_initiatives) + len(deprioritized_initiatives)) > 0 else 0
        st.metric("Success Rate", f"{success_rate:.0f}%")
    with col4:
        st.metric("Active", len(initiatives_df[initiatives_df['status'] == 'Active']))

    # ROI Analysis
    st.markdown("---")
    st.subheader("💰 ROI Impact Analysis")
    st.markdown("*Investment vs business impact for completed initiatives*")

    completed_with_roi = completed_initiatives.copy()
    if len(completed_with_roi) > 0:
        roi_scatter = create_roi_scatter(completed_with_roi)
        st.plotly_chart(roi_scatter, use_container_width=True)

        # ROI Summary
        col1, col2, col3 = st.columns(3)

        high_roi = completed_with_roi[completed_with_roi['roi_estimate'] == 'High']
        medium_roi = completed_with_roi[completed_with_roi['roi_estimate'] == 'Medium']
        low_roi = completed_with_roi[completed_with_roi['roi_estimate'] == 'Low']

        total_points = completed_with_roi['completed_story_points'].sum()

        with col1:
            high_roi_pct = high_roi['completed_story_points'].sum() / total_points * 100 if total_points > 0 else 0
            st.markdown(f"""
            <div class="metric-card success-card">
                <h4>High ROI Initiatives</h4>
                <p><b>{len(high_roi)}</b> initiatives</p>
                <p><b>{high_roi_pct:.0f}%</b> of effort</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            medium_roi_pct = medium_roi['completed_story_points'].sum() / total_points * 100 if total_points > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <h4>Medium ROI Initiatives</h4>
                <p><b>{len(medium_roi)}</b> initiatives</p>
                <p><b>{medium_roi_pct:.0f}%</b> of effort</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            low_roi_pct = low_roi['completed_story_points'].sum() / total_points * 100 if total_points > 0 else 0
            st.markdown(f"""
            <div class="metric-card warning-card">
                <h4>Low ROI Initiatives</h4>
                <p><b>{len(low_roi)}</b> initiatives</p>
                <p><b>{low_roi_pct:.0f}%</b> of effort</p>
            </div>
            """, unsafe_allow_html=True)

    # Quarterly Summary
    st.markdown("---")
    st.subheader("📊 6-Month Summary")

    summary_stats = get_sprint_summary_stats(sprints_df, stories_df)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Delivery Metrics")
        st.markdown(f"""
        - **Total Sprints:** {summary_stats['total_sprints']}
        - **Total Story Points:** {summary_stats['total_points_delivered']:.0f}
        - **Total Stories:** {summary_stats['total_stories']}
        - **Average Velocity:** {summary_stats['avg_velocity']:.1f} ±{summary_stats['velocity_std']:.1f}
        - **Average Completion:** {summary_stats['avg_completion_rate']*100:.0f}%
        """)

    with col2:
        st.markdown("### 🏆 Top Achievements")
        st.markdown(f"""
        1. **Velocity Growth:** {improvement:.0f}% improvement over 6 months
        2. **Predictability:** {predictability*100:.0f}% sprint predictability achieved
        3. **Quality:** {bug_reduction:.0f}% reduction in bug ratio
        4. **Initiatives:** {len(completed_initiatives)} initiatives successfully delivered
        5. **Team Calibration:** Estimation accuracy improved to {late_accuracy*100:.0f}%
        """)

    st.markdown("### 🎯 Areas for Improvement")
    improvement_areas = []

    if summary_stats['avg_cycle_time'] > 7:
        improvement_areas.append(f"- **Cycle Time:** Average of {summary_stats['avg_cycle_time']:.1f} days - target <7 days")

    if summary_stats['total_blockers'] > summary_stats['total_stories'] * 0.15:
        improvement_areas.append(f"- **Blockers:** {summary_stats['total_blockers']} blockers encountered - work on dependency management")

    if low_roi_pct > 25:
        improvement_areas.append(f"- **Portfolio Focus:** {low_roi_pct:.0f}% effort on low-ROI initiatives - prioritize high-impact work")

    if improvement_areas:
        for area in improvement_areas:
            st.markdown(area)
    else:
        st.success("✅ Team performing excellently across all metrics!")


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 20px;'>
    <p>Sprint Performance & Portfolio Analytics Dashboard</p>
    <p>Built with Streamlit | Designed for PM & Strategy/Operations Roles</p>
</div>
""", unsafe_allow_html=True)
