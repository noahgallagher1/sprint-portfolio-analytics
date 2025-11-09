"""
Visualization Utilities

Reusable Plotly chart functions for sprint analytics dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


# Color scheme
COLORS = {
    'primary': '#2E86AB',
    'success': '#06A77D',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'neutral': '#6c757d',
    'light_blue': '#A3CEF1',
    'light_green': '#90EE90',
    'light_red': '#FFB6C1'
}

# Quadrant colors
QUADRANT_COLORS = {
    'Quick Wins': COLORS['success'],
    'Major Projects': COLORS['primary'],
    'Fill-ins': COLORS['neutral'],
    'Time Sinks': COLORS['danger']
}


def create_velocity_trend_chart(sprints_df):
    """
    Create velocity trend chart with committed vs completed points.

    Args:
        sprints_df: Sprint DataFrame with rolling averages

    Returns:
        plotly Figure
    """
    fig = go.Figure()

    # Committed points
    fig.add_trace(go.Scatter(
        x=sprints_df['sprint_number'],
        y=sprints_df['committed_points'],
        name='Committed',
        mode='lines+markers',
        line=dict(color=COLORS['primary'], width=2, dash='dot'),
        marker=dict(size=6)
    ))

    # Completed points
    fig.add_trace(go.Scatter(
        x=sprints_df['sprint_number'],
        y=sprints_df['completed_points'],
        name='Completed',
        mode='lines+markers',
        line=dict(color=COLORS['success'], width=3),
        marker=dict(size=8)
    ))

    # 3-sprint moving average
    if 'velocity_rolling_avg' in sprints_df.columns:
        fig.add_trace(go.Scatter(
            x=sprints_df['sprint_number'],
            y=sprints_df['velocity_rolling_avg'],
            name='3-Sprint Avg',
            mode='lines',
            line=dict(color=COLORS['warning'], width=2, dash='dash')
        ))

    fig.update_layout(
        xaxis_title='Sprint Number',
        yaxis_title='Story Points',
        hovermode='x unified',
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=10)
    )

    return fig


def create_burndown_chart(committed_points, completed_points, days_in_sprint=14, days_elapsed=7):
    """
    Create sprint burndown chart.

    Args:
        committed_points: Total committed story points
        completed_points: Completed story points so far
        days_in_sprint: Total sprint duration (default 14)
        days_elapsed: Days elapsed in sprint (default 7)

    Returns:
        plotly Figure
    """
    # Ideal burndown
    ideal_x = [0, days_in_sprint]
    ideal_y = [committed_points, 0]

    # Actual burndown (simulated for demo)
    remaining_points = committed_points - completed_points
    actual_x = [0, days_elapsed]
    actual_y = [committed_points, remaining_points]

    # Projected completion
    if days_elapsed > 0:
        burn_rate = completed_points / days_elapsed
        projected_completion_day = committed_points / burn_rate if burn_rate > 0 else days_in_sprint
        projected_x = [0, days_elapsed, min(projected_completion_day, days_in_sprint * 1.5)]
        projected_y = [committed_points, remaining_points, 0]
    else:
        projected_x = [0, days_in_sprint]
        projected_y = [committed_points, 0]

    fig = go.Figure()

    # Ideal line
    fig.add_trace(go.Scatter(
        x=ideal_x, y=ideal_y,
        name='Ideal',
        mode='lines',
        line=dict(color=COLORS['neutral'], width=2, dash='dash')
    ))

    # Actual progress
    fig.add_trace(go.Scatter(
        x=actual_x, y=actual_y,
        name='Actual',
        mode='lines+markers',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=10)
    ))

    # Projected
    fig.add_trace(go.Scatter(
        x=projected_x, y=projected_y,
        name='Projected',
        mode='lines',
        line=dict(color=COLORS['warning'], width=2, dash='dot')
    ))

    fig.update_layout(
        title=f'Current Sprint Burndown (Day {days_elapsed} of {days_in_sprint})',
        xaxis_title='Days',
        yaxis_title='Story Points Remaining',
        hovermode='x unified',
        height=350
    )

    return fig


def create_impact_effort_matrix(initiatives_df):
    """
    Create Impact vs Effort scatter plot (Priority Matrix).

    Args:
        initiatives_df: Initiatives DataFrame with quadrant classification

    Returns:
        plotly Figure
    """
    fig = px.scatter(
        initiatives_df,
        x='impact_score',
        y='effort_score',
        size='total_story_points',
        color='quadrant',
        hover_name='name',
        hover_data={
            'impact_score': True,
            'effort_score': True,
            'total_story_points': True,
            'status': True,
            'quadrant': False
        },
        color_discrete_map=QUADRANT_COLORS,
        labels={
            'impact_score': 'Business Impact Score',
            'effort_score': 'Effort Score',
            'total_story_points': 'Story Points'
        }
    )

    # Add quadrant dividing lines
    fig.add_hline(y=5.5, line_dash="dot", line_color="gray", opacity=0.5)
    fig.add_vline(x=6.5, line_dash="dot", line_color="gray", opacity=0.5)

    # Add quadrant labels - positioned in corners to avoid overlapping bubbles
    fig.add_annotation(x=9.5, y=1.5, text="Quick Wins", showarrow=False,
                      font=dict(size=11, color=COLORS['success'], family="Arial Black"),
                      bgcolor="rgba(255,255,255,0.8)", bordercolor=COLORS['success'], borderwidth=2, borderpad=4)
    fig.add_annotation(x=9.5, y=9.5, text="Major Projects", showarrow=False,
                      font=dict(size=11, color=COLORS['primary'], family="Arial Black"),
                      bgcolor="rgba(255,255,255,0.8)", bordercolor=COLORS['primary'], borderwidth=2, borderpad=4)
    fig.add_annotation(x=1.5, y=1.5, text="Fill-ins", showarrow=False,
                      font=dict(size=11, color=COLORS['neutral'], family="Arial Black"),
                      bgcolor="rgba(255,255,255,0.8)", bordercolor=COLORS['neutral'], borderwidth=2, borderpad=4)
    fig.add_annotation(x=1.5, y=9.5, text="Time Sinks", showarrow=False,
                      font=dict(size=11, color=COLORS['danger'], family="Arial Black"),
                      bgcolor="rgba(255,255,255,0.8)", bordercolor=COLORS['danger'], borderwidth=2, borderpad=4)

    fig.update_layout(
        xaxis=dict(range=[0, 11], title='Business Impact Score →'),
        yaxis=dict(range=[0, 11], title='Effort Required →'),
        height=500,
        showlegend=True,
        margin=dict(t=10)
    )

    return fig


def create_health_gauge(health_score, title="Sprint Health Score"):
    """
    Create gauge chart for health scores.

    Args:
        health_score: Score from 0-100
        title: Gauge title

    Returns:
        plotly Figure
    """
    # Determine color based on score
    if health_score >= 80:
        color = COLORS['success']
    elif health_score >= 60:
        color = COLORS['warning']
    else:
        color = COLORS['danger']

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 60], 'color': COLORS['light_red']},
                {'range': [60, 80], 'color': COLORS['light_blue']},
                {'range': [80, 100], 'color': COLORS['light_green']}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 2},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))

    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))

    return fig


def create_capacity_heatmap(team_metrics_by_sprint):
    """
    Create capacity utilization heatmap for team members across sprints.

    Args:
        team_metrics_by_sprint: DataFrame with columns [member_name, sprint_number, utilization_pct]

    Returns:
        plotly Figure
    """
    # Pivot for heatmap
    pivot_data = team_metrics_by_sprint.pivot(
        index='member_name',
        columns='sprint_number',
        values='utilization_pct'
    )

    # Create custom colorscale
    colorscale = [
        [0, COLORS['light_blue']],      # Under-utilized
        [0.7, COLORS['success']],        # Healthy
        [0.95, COLORS['warning']],       # At capacity
        [1, COLORS['danger']]            # Over-utilized
    ]

    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale=colorscale,
        zmid=85,  # Center around 85% utilization
        colorbar=dict(title="Utilization %"),
        hovertemplate='<b>%{y}</b><br>Sprint: %{x}<br>Utilization: %{z:.0f}%<extra></extra>'
    ))

    fig.update_layout(
        xaxis_title='Sprint Number',
        yaxis_title='Team Member',
        height=400,
        margin=dict(t=10)
    )

    return fig


def create_portfolio_quadrant_summary(initiatives_df):
    """
    Create a simple bar chart showing portfolio composition by quadrant.
    Alternative to the detailed scatter plot for executive summary.

    Args:
        initiatives_df: Initiatives DataFrame with quadrant classification

    Returns:
        plotly Figure
    """
    # Count initiatives by quadrant
    quadrant_counts = initiatives_df['quadrant'].value_counts().reset_index()
    quadrant_counts.columns = ['Quadrant', 'Count']

    # Get total story points by quadrant
    quadrant_points = initiatives_df.groupby('quadrant')['total_story_points'].sum().reset_index()
    quadrant_points.columns = ['Quadrant', 'Total Points']

    # Merge
    quadrant_summary = quadrant_counts.merge(quadrant_points, on='Quadrant')

    # Order by priority (Quick Wins, Major Projects, Fill-ins, Time Sinks)
    order = ['Quick Wins', 'Major Projects', 'Fill-ins', 'Time Sinks']
    quadrant_summary['Quadrant'] = pd.Categorical(quadrant_summary['Quadrant'], categories=order, ordered=True)
    quadrant_summary = quadrant_summary.sort_values('Quadrant')

    # Create grouped bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Initiatives',
        x=quadrant_summary['Quadrant'],
        y=quadrant_summary['Count'],
        marker_color=[QUADRANT_COLORS.get(q, COLORS['neutral']) for q in quadrant_summary['Quadrant']],
        text=quadrant_summary['Count'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Initiatives: %{y}<extra></extra>'
    ))

    fig.update_layout(
        xaxis_title='Portfolio Quadrant',
        yaxis_title='Number of Initiatives',
        showlegend=False,
        height=400,
        margin=dict(t=10)
    )

    return fig


def create_cycle_time_boxplot(stories_df):
    """
    Create box plot for cycle time by story point size.

    Args:
        stories_df: Stories DataFrame

    Returns:
        plotly Figure
    """
    fig = px.box(
        stories_df,
        x='story_points',
        y='cycle_time_days',
        color='story_points',
        labels={
            'story_points': 'Story Points',
            'cycle_time_days': 'Cycle Time (Days)'
        },
        title='Cycle Time Distribution by Story Size'
    )

    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis={'type': 'category'}
    )

    return fig


def create_story_type_stacked_area(story_type_by_sprint):
    """
    Create stacked area chart for story type distribution over time.

    Args:
        story_type_by_sprint: DataFrame with columns [sprint_number, story_type, count]

    Returns:
        plotly Figure
    """
    # Pivot data
    pivot_data = story_type_by_sprint.pivot(
        index='sprint_number',
        columns='story_type',
        values='count'
    ).fillna(0)

    fig = go.Figure()

    story_type_colors = {
        'Feature': COLORS['primary'],
        'Bug': COLORS['danger'],
        'Technical Debt': COLORS['warning'],
        'Spike': COLORS['neutral']
    }

    for story_type in pivot_data.columns:
        fig.add_trace(go.Scatter(
            x=pivot_data.index,
            y=pivot_data[story_type],
            name=story_type,
            mode='lines',
            stackgroup='one',
            fillcolor=story_type_colors.get(story_type, COLORS['neutral'])
        ))

    fig.update_layout(
        xaxis_title='Sprint Number',
        yaxis_title='Number of Stories',
        hovermode='x unified',
        height=400,
        margin=dict(t=20)
    )

    return fig


def create_completion_probability_chart(prediction_data):
    """
    Create probability distribution chart for sprint completion.

    Args:
        prediction_data: Dict from calculate_probability_distribution_chart_data

    Returns:
        plotly Figure
    """
    fig = go.Figure()

    # Histogram of simulated velocities
    fig.add_trace(go.Histogram(
        x=prediction_data['simulated_velocities'],
        name='Simulated Outcomes',
        marker_color=COLORS['primary'],
        opacity=0.7,
        nbinsx=30
    ))

    # Add committed points line
    fig.add_vline(
        x=prediction_data['committed_points'],
        line_dash="dash",
        line_color=COLORS['danger'],
        annotation_text=f"Committed: {prediction_data['committed_points']} pts",
        annotation_position="top right"
    )

    # Add expected velocity line
    fig.add_vline(
        x=prediction_data['expected_velocity'],
        line_dash="dot",
        line_color=COLORS['success'],
        annotation_text=f"Expected: {prediction_data['expected_velocity']:.0f} pts",
        annotation_position="top left"
    )

    probability_pct = prediction_data['probability'] * 100

    fig.update_layout(
        title=f'Sprint Completion Probability: {probability_pct:.0f}%',
        xaxis_title='Simulated Velocity (Story Points)',
        yaxis_title='Frequency',
        height=400,
        showlegend=False
    )

    return fig


def create_initiative_funnel(funnel_data):
    """
    Create funnel chart for initiative intake process.

    Args:
        funnel_data: DataFrame with columns [stage, count, percentage]

    Returns:
        plotly Figure
    """
    fig = go.Figure(go.Funnel(
        y=funnel_data['stage'],
        x=funnel_data['count'],
        textinfo="value+percent initial",
        marker=dict(color=[COLORS['neutral'], COLORS['primary'],
                          COLORS['warning'], COLORS['success']])
    ))

    fig.update_layout(
        title='Initiative Intake Funnel',
        height=400
    )

    return fig


def create_treemap(data_df, path_columns, value_column, color_column=None, title="Treemap"):
    """
    Create treemap visualization.

    Args:
        data_df: DataFrame
        path_columns: List of column names for hierarchy
        value_column: Column name for size
        color_column: Optional column name for color
        title: Chart title

    Returns:
        plotly Figure
    """
    fig = px.treemap(
        data_df,
        path=path_columns,
        values=value_column,
        color=color_column,
        title=title,
        height=500
    )

    return fig


def create_roi_scatter(initiatives_df):
    """
    Create ROI-focused scatter plot.

    Args:
        initiatives_df: Initiatives DataFrame

    Returns:
        plotly Figure
    """
    roi_colors = {'High': COLORS['success'], 'Medium': COLORS['warning'], 'Low': COLORS['danger']}

    fig = px.scatter(
        initiatives_df,
        x='completed_story_points',
        y='impact_score',
        size='total_story_points',
        color='roi_estimate',
        hover_name='name',
        color_discrete_map=roi_colors,
        labels={
            'completed_story_points': 'Investment (Story Points Completed)',
            'impact_score': 'Business Impact Score',
            'roi_estimate': 'ROI Category'
        },
        title='Initiative ROI Analysis: Investment vs Impact'
    )

    fig.update_layout(height=450)

    return fig
