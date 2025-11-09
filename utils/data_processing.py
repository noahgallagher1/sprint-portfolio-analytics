"""
Data Processing Utilities

Handles loading, cleaning, and transforming sprint analytics data.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st


@st.cache_data
def load_all_data():
    """
    Load all data files and return as dictionary of DataFrames.

    Returns:
        dict: Dictionary containing 'sprints', 'stories', 'initiatives', 'team'
    """
    try:
        sprints = pd.read_csv('data/sprint_data.csv')
        stories = pd.read_csv('data/story_data.csv')
        initiatives = pd.read_csv('data/initiative_data.csv')
        team = pd.read_csv('data/team_data.csv')

        # Convert date columns
        sprints['start_date'] = pd.to_datetime(sprints['start_date'])
        sprints['end_date'] = pd.to_datetime(sprints['end_date'])
        stories['start_date'] = pd.to_datetime(stories['start_date'])

        return {
            'sprints': sprints,
            'stories': stories,
            'initiatives': initiatives,
            'team': team
        }
    except FileNotFoundError as e:
        st.error(f"Data files not found. Please run: python data/generate_data.py")
        st.stop()


def get_current_sprint(sprints_df):
    """
    Get the most recent sprint (assume it's the current one).

    Args:
        sprints_df: Sprint DataFrame

    Returns:
        Series: Current sprint data
    """
    return sprints_df.iloc[-1]


def get_sprint_stories(stories_df, sprint_number):
    """
    Get all stories for a specific sprint.

    Args:
        stories_df: Stories DataFrame
        sprint_number: Sprint number to filter by

    Returns:
        DataFrame: Filtered stories
    """
    return stories_df[stories_df['sprint_number'] == sprint_number].copy()


def get_initiative_stories(stories_df, initiative_id):
    """
    Get all stories for a specific initiative.

    Args:
        stories_df: Stories DataFrame
        initiative_id: Initiative ID to filter by

    Returns:
        DataFrame: Filtered stories
    """
    return stories_df[stories_df['initiative_id'] == initiative_id].copy()


def calculate_rolling_metrics(sprints_df, window=3):
    """
    Calculate rolling window metrics for sprints.

    Args:
        sprints_df: Sprint DataFrame
        window: Rolling window size (default 3)

    Returns:
        DataFrame: Sprint data with rolling metrics
    """
    df = sprints_df.copy()

    # Rolling averages
    df['velocity_rolling_avg'] = df['velocity'].rolling(window=window, min_periods=1).mean()
    df['velocity_rolling_std'] = df['velocity'].rolling(window=window, min_periods=1).std()
    df['completion_rate_rolling_avg'] = df['completion_rate'].rolling(window=window, min_periods=1).mean()

    return df


def enrich_stories_with_team_data(stories_df, team_df):
    """
    Enrich stories DataFrame with team member information.

    Args:
        stories_df: Stories DataFrame
        team_df: Team DataFrame

    Returns:
        DataFrame: Enriched stories
    """
    return stories_df.merge(
        team_df[['member_id', 'role', 'specialization']],
        left_on='assignee_id',
        right_on='member_id',
        how='left'
    )


def calculate_story_metrics_by_sprint(stories_df):
    """
    Calculate aggregated story metrics by sprint.

    Args:
        stories_df: Stories DataFrame

    Returns:
        DataFrame: Aggregated metrics by sprint
    """
    metrics = stories_df.groupby('sprint_number').agg({
        'story_id': 'count',
        'story_points': 'sum',
        'final_story_points': 'sum',
        'cycle_time_days': 'mean',
        'num_blockers': 'sum',
        'blocker_duration_days': 'sum',
        'estimation_accuracy': 'mean',
        'dependencies_count': 'sum'
    }).reset_index()

    metrics.columns = [
        'sprint_number', 'total_stories', 'planned_points', 'actual_points',
        'avg_cycle_time', 'total_blockers', 'total_blocker_days',
        'avg_estimation_accuracy', 'total_dependencies'
    ]

    return metrics


def calculate_story_type_distribution(stories_df):
    """
    Calculate distribution of story types across all sprints.

    Args:
        stories_df: Stories DataFrame

    Returns:
        DataFrame: Story type distribution by sprint
    """
    return stories_df.groupby(['sprint_number', 'story_type']).size().reset_index(name='count')


def get_completed_stories(stories_df):
    """
    Filter for completed stories only.

    Args:
        stories_df: Stories DataFrame

    Returns:
        DataFrame: Only completed stories
    """
    return stories_df[stories_df['status'] == 'Completed'].copy()


def get_stories_by_status(stories_df, sprint_number=None):
    """
    Get story counts by status, optionally for a specific sprint.

    Args:
        stories_df: Stories DataFrame
        sprint_number: Optional sprint number to filter

    Returns:
        Series: Story counts by status
    """
    if sprint_number is not None:
        stories_df = stories_df[stories_df['sprint_number'] == sprint_number]

    return stories_df['status'].value_counts()


def calculate_team_member_metrics(stories_df, team_df):
    """
    Calculate performance metrics for each team member.

    Args:
        stories_df: Stories DataFrame
        team_df: Team DataFrame

    Returns:
        DataFrame: Team member metrics
    """
    # Aggregate by team member
    member_metrics = stories_df.groupby('assignee_id').agg({
        'story_points': 'sum',
        'final_story_points': 'sum',
        'cycle_time_days': 'mean',
        'story_id': 'count',
        'estimation_accuracy': 'mean'
    }).reset_index()

    member_metrics.columns = [
        'member_id', 'total_points_planned', 'total_points_delivered',
        'avg_cycle_time', 'stories_completed', 'avg_estimation_accuracy'
    ]

    # Merge with team data
    member_metrics = member_metrics.merge(team_df, on='member_id', how='left')

    # Calculate utilization (assuming avg_capacity_per_sprint is for the entire period)
    num_sprints = stories_df['sprint_number'].nunique()
    member_metrics['avg_points_per_sprint'] = member_metrics['total_points_delivered'] / num_sprints
    member_metrics['utilization_pct'] = (
        member_metrics['avg_points_per_sprint'] / member_metrics['avg_capacity_per_sprint'] * 100
    )

    return member_metrics


def filter_data_by_date_range(df, start_date, end_date, date_column='start_date'):
    """
    Filter DataFrame by date range.

    Args:
        df: DataFrame to filter
        start_date: Start date
        end_date: End date
        date_column: Name of date column to filter on

    Returns:
        DataFrame: Filtered data
    """
    return df[(df[date_column] >= start_date) & (df[date_column] <= end_date)].copy()


def get_initiative_summary(initiatives_df, stories_df):
    """
    Create summary view of initiatives with calculated metrics.

    Args:
        initiatives_df: Initiatives DataFrame
        stories_df: Stories DataFrame

    Returns:
        DataFrame: Initiative summary with metrics
    """
    df = initiatives_df.copy()

    # Calculate completion percentage
    df['completion_pct'] = (df['completed_story_points'] / df['total_story_points'] * 100).fillna(0)

    # Calculate priority score (from prioritization module will be called separately)
    df['priority_score_base'] = df['impact_score'] / df['effort_score']

    # Add story count if not present or update it
    story_counts = stories_df.groupby('initiative_id').size().reset_index(name='actual_story_count')
    df = df.merge(story_counts, left_on='initiative_id', right_on='initiative_id', how='left')
    df['actual_story_count'] = df['actual_story_count'].fillna(0).astype(int)

    return df


def get_sprint_summary_stats(sprints_df, stories_df):
    """
    Calculate summary statistics across all sprints.

    Args:
        sprints_df: Sprints DataFrame
        stories_df: Stories DataFrame

    Returns:
        dict: Summary statistics
    """
    return {
        'total_sprints': len(sprints_df),
        'avg_velocity': sprints_df['velocity'].mean(),
        'velocity_std': sprints_df['velocity'].std(),
        'avg_completion_rate': sprints_df['completion_rate'].mean(),
        'total_stories': len(stories_df),
        'total_points_delivered': sprints_df['completed_points'].sum(),
        'avg_cycle_time': stories_df['cycle_time_days'].mean(),
        'total_blockers': stories_df['num_blockers'].sum(),
    }
