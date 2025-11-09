"""
Sprint & Portfolio Metrics Calculations

Contains all business logic for calculating key performance indicators.
"""

import pandas as pd
import numpy as np
from scipy import stats


def calculate_sprint_health_score(sprint_data, sprints_history):
    """
    Calculate comprehensive sprint health score (0-100).

    Health score based on:
    - Velocity consistency (30%)
    - Estimation accuracy (25%)
    - Completion rate (25%)
    - Blocker frequency (20%)

    Args:
        sprint_data: Current sprint data (Series)
        sprints_history: Historical sprint data (DataFrame)

    Returns:
        dict: Health score and components
    """
    # 1. Velocity consistency (lower std dev = better)
    velocities = sprints_history['velocity'].values
    avg_velocity = np.mean(velocities)
    velocity_std = np.std(velocities)
    velocity_consistency = 1 - min(velocity_std / avg_velocity, 1.0) if avg_velocity > 0 else 0
    velocity_consistency = max(0, velocity_consistency)

    # 2. Estimation accuracy (from stories in sprint)
    estimation_accuracy = sprint_data.get('avg_estimation_accuracy', 0.85)

    # 3. Completion rate
    completion_rate = sprint_data['completion_rate']
    completion_rate = min(1.0, completion_rate)  # Cap at 100%

    # 4. Blocker rate (inverse)
    total_stories = sprint_data.get('stories_count', 1)
    stories_with_blockers = sprint_data.get('stories_with_blockers', 0)
    blocker_rate = stories_with_blockers / total_stories if total_stories > 0 else 0

    # Weighted composite score
    health_score = (
        velocity_consistency * 0.30 +
        estimation_accuracy * 0.25 +
        completion_rate * 0.25 +
        (1 - blocker_rate) * 0.20
    ) * 100

    return {
        'health_score': health_score,
        'velocity_consistency': velocity_consistency * 100,
        'estimation_accuracy': estimation_accuracy * 100,
        'completion_rate': completion_rate * 100,
        'blocker_impact': (1 - blocker_rate) * 100
    }


def calculate_velocity_trend(sprints_df):
    """
    Calculate velocity trend using linear regression.

    Args:
        sprints_df: Sprint DataFrame

    Returns:
        dict: Trend analysis
    """
    sprint_numbers = sprints_df['sprint_number'].values
    velocities = sprints_df['velocity'].values

    if len(sprint_numbers) < 2:
        return {'trend': 'Insufficient data', 'slope': 0, 'r_squared': 0}

    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(sprint_numbers, velocities)

    # Interpret trend
    if slope > 0.5:
        trend = "Increasing"
    elif slope < -0.5:
        trend = "Decreasing"
    else:
        trend = "Stable"

    return {
        'trend': trend,
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_value ** 2,
        'p_value': p_value
    }


def calculate_predictability_score(sprints_df):
    """
    Calculate team predictability based on velocity variance.

    Args:
        sprints_df: Sprint DataFrame

    Returns:
        float: Predictability score (0-1, higher is better)
    """
    velocities = sprints_df['velocity'].values
    avg_velocity = np.mean(velocities)
    velocity_std = np.std(velocities)

    if avg_velocity == 0:
        return 0

    # Coefficient of variation (inverse)
    cv = velocity_std / avg_velocity
    predictability = 1 - min(cv, 1.0)

    return max(0, predictability)


def calculate_cycle_time_metrics(stories_df):
    """
    Calculate cycle time metrics and control limits.

    Args:
        stories_df: Stories DataFrame (completed stories)

    Returns:
        dict: Cycle time metrics
    """
    cycle_times = stories_df['cycle_time_days'].values

    mean_cycle_time = np.mean(cycle_times)
    std_cycle_time = np.std(cycle_times)
    median_cycle_time = np.median(cycle_times)

    # Control limits (3 sigma)
    upper_control_limit = mean_cycle_time + (3 * std_cycle_time)
    lower_control_limit = max(0, mean_cycle_time - (3 * std_cycle_time))

    # Identify outliers
    outliers = stories_df[
        (stories_df['cycle_time_days'] > upper_control_limit) |
        (stories_df['cycle_time_days'] < lower_control_limit)
    ]

    return {
        'mean': mean_cycle_time,
        'median': median_cycle_time,
        'std': std_cycle_time,
        'upper_control_limit': upper_control_limit,
        'lower_control_limit': lower_control_limit,
        'num_outliers': len(outliers),
        'outlier_rate': len(outliers) / len(stories_df) if len(stories_df) > 0 else 0
    }


def calculate_cycle_time_by_points(stories_df):
    """
    Calculate average cycle time by story point size.

    Args:
        stories_df: Stories DataFrame

    Returns:
        DataFrame: Cycle time by story points
    """
    return stories_df.groupby('story_points').agg({
        'cycle_time_days': ['mean', 'median', 'std', 'count']
    }).reset_index()


def calculate_capacity_utilization(sprint_data):
    """
    Calculate capacity utilization for a sprint.

    Args:
        sprint_data: Sprint data (Series or dict)

    Returns:
        dict: Utilization metrics
    """
    capacity = sprint_data['team_capacity']
    committed = sprint_data['committed_points']
    completed = sprint_data['completed_points']

    commitment_utilization = (committed / capacity * 100) if capacity > 0 else 0
    actual_utilization = (completed / capacity * 100) if capacity > 0 else 0

    # Determine health status
    if actual_utilization > 105:
        status = "Over-utilized"
        health = "warning"
    elif actual_utilization > 95:
        status = "At capacity"
        health = "good"
    elif actual_utilization > 70:
        status = "Healthy"
        health = "good"
    else:
        status = "Under-utilized"
        health = "warning"

    return {
        'commitment_utilization': commitment_utilization,
        'actual_utilization': actual_utilization,
        'status': status,
        'health': health
    }


def calculate_estimation_accuracy_trend(stories_df):
    """
    Calculate how estimation accuracy changes over sprints.

    Args:
        stories_df: Stories DataFrame

    Returns:
        DataFrame: Accuracy by sprint
    """
    accuracy_by_sprint = stories_df.groupby('sprint_number').agg({
        'estimation_accuracy': 'mean'
    }).reset_index()

    accuracy_by_sprint.columns = ['sprint_number', 'avg_accuracy']

    return accuracy_by_sprint


def calculate_story_type_mix(stories_df):
    """
    Calculate the distribution of story types.

    Args:
        stories_df: Stories DataFrame

    Returns:
        DataFrame: Story type distribution
    """
    type_counts = stories_df.groupby('story_type').size().reset_index(name='count')
    type_counts['percentage'] = type_counts['count'] / type_counts['count'].sum() * 100

    return type_counts


def calculate_bug_ratio(stories_df):
    """
    Calculate percentage of bugs vs total stories.

    Args:
        stories_df: Stories DataFrame

    Returns:
        float: Bug ratio (0-1)
    """
    total_stories = len(stories_df)
    bug_stories = len(stories_df[stories_df['story_type'] == 'Bug'])

    return bug_stories / total_stories if total_stories > 0 else 0


def calculate_blocker_impact(stories_df):
    """
    Calculate impact of blockers on delivery.

    Args:
        stories_df: Stories DataFrame

    Returns:
        dict: Blocker metrics
    """
    total_stories = len(stories_df)
    stories_with_blockers = len(stories_df[stories_df['num_blockers'] > 0])

    blocker_rate = stories_with_blockers / total_stories if total_stories > 0 else 0

    # Average delay caused by blockers
    blocked_stories = stories_df[stories_df['num_blockers'] > 0]
    avg_blocker_delay = blocked_stories['blocker_duration_days'].mean() if len(blocked_stories) > 0 else 0

    # Correlation between blockers and cycle time
    if len(stories_df) > 10:
        correlation = stories_df['num_blockers'].corr(stories_df['cycle_time_days'])
    else:
        correlation = 0

    return {
        'blocker_rate': blocker_rate,
        'stories_blocked': stories_with_blockers,
        'avg_delay_days': avg_blocker_delay,
        'cycle_time_correlation': correlation
    }


def calculate_carryover_rate(stories_df):
    """
    Calculate story carryover rate.

    Args:
        stories_df: Stories DataFrame

    Returns:
        float: Carryover rate (0-1)
    """
    total_stories = len(stories_df)
    carried_over = len(stories_df[stories_df['status'] == 'Carried Over'])

    return carried_over / total_stories if total_stories > 0 else 0


def calculate_team_velocity_contribution(stories_df, team_df):
    """
    Calculate each team member's contribution to velocity.

    Args:
        stories_df: Stories DataFrame (completed stories)
        team_df: Team DataFrame

    Returns:
        DataFrame: Velocity contribution by team member
    """
    completed_stories = stories_df[stories_df['status'] == 'Completed']

    velocity_contrib = completed_stories.groupby('assignee_id').agg({
        'final_story_points': 'sum',
        'story_id': 'count'
    }).reset_index()

    velocity_contrib.columns = ['member_id', 'points_delivered', 'stories_completed']

    # Calculate percentage
    total_points = velocity_contrib['points_delivered'].sum()
    velocity_contrib['percentage'] = (
        velocity_contrib['points_delivered'] / total_points * 100
        if total_points > 0 else 0
    )

    # Merge with team data
    velocity_contrib = velocity_contrib.merge(
        team_df[['member_id', 'name', 'role']],
        on='member_id',
        how='left'
    )

    return velocity_contrib.sort_values('points_delivered', ascending=False)


def calculate_work_distribution_by_role(stories_df, team_df):
    """
    Calculate how work is distributed across roles.

    Args:
        stories_df: Stories DataFrame
        team_df: Team DataFrame

    Returns:
        DataFrame: Work distribution by role
    """
    # Merge to get roles
    stories_with_roles = stories_df.merge(
        team_df[['member_id', 'role']],
        left_on='assignee_id',
        right_on='member_id',
        how='left'
    )

    role_distribution = stories_with_roles.groupby('role').agg({
        'story_points': 'sum',
        'story_id': 'count'
    }).reset_index()

    role_distribution.columns = ['role', 'total_points', 'story_count']

    # Calculate percentages
    total_points = role_distribution['total_points'].sum()
    role_distribution['percentage'] = (
        role_distribution['total_points'] / total_points * 100
        if total_points > 0 else 0
    )

    return role_distribution.sort_values('total_points', ascending=False)


def identify_bottlenecks(stories_df, team_df):
    """
    Identify potential bottlenecks in the delivery process.

    Args:
        stories_df: Stories DataFrame
        team_df: Team DataFrame

    Returns:
        dict: Identified bottlenecks with recommendations
    """
    bottlenecks = []

    # 1. Story types with longest cycle time
    cycle_time_by_type = stories_df.groupby('story_type')['cycle_time_days'].mean().sort_values(ascending=False)
    if len(cycle_time_by_type) > 0:
        slowest_type = cycle_time_by_type.index[0]
        slowest_time = cycle_time_by_type.values[0]
        avg_time = stories_df['cycle_time_days'].mean()

        if slowest_time > avg_time * 1.5:
            bottlenecks.append({
                'type': 'Story Type',
                'description': f'{slowest_type} stories take {slowest_time:.1f} days on average',
                'impact': 'high' if slowest_time > avg_time * 2 else 'medium',
                'recommendation': f'Investigate why {slowest_type} stories take longer. Consider breaking them down or allocating specialist resources.'
            })

    # 2. Team members with high cycle times
    cycle_time_by_member = stories_df.groupby('assignee_id')['cycle_time_days'].mean().sort_values(ascending=False)
    if len(cycle_time_by_member) > 0:
        slowest_member = cycle_time_by_member.index[0]
        slowest_member_time = cycle_time_by_member.values[0]
        avg_time = stories_df['cycle_time_days'].mean()

        if slowest_member_time > avg_time * 1.5:
            member_name = team_df[team_df['member_id'] == slowest_member]['name'].values[0]
            bottlenecks.append({
                'type': 'Team Member',
                'description': f'{member_name} has average cycle time of {slowest_member_time:.1f} days',
                'impact': 'medium',
                'recommendation': f'Review workload and support needs for {member_name}. May need mentoring or have capacity constraints.'
            })

    # 3. High blocker rate
    blocker_impact = calculate_blocker_impact(stories_df)
    if blocker_impact['blocker_rate'] > 0.20:
        bottlenecks.append({
            'type': 'Blockers',
            'description': f'{blocker_impact["blocker_rate"]*100:.1f}% of stories encounter blockers',
            'impact': 'high',
            'recommendation': 'High blocker rate suggests dependency or process issues. Conduct blocker retrospective and implement mitigation strategies.'
        })

    # 4. High carryover rate
    carryover_rate = calculate_carryover_rate(stories_df)
    if carryover_rate > 0.15:
        bottlenecks.append({
            'type': 'Carryover',
            'description': f'{carryover_rate*100:.1f}% of stories are carried over',
            'impact': 'medium',
            'recommendation': 'High carryover suggests scope issues or overcommitment. Review sprint planning process and estimation practices.'
        })

    return bottlenecks


def calculate_quality_trend(stories_df):
    """
    Calculate quality trend based on bug ratio over time.

    Args:
        stories_df: Stories DataFrame

    Returns:
        DataFrame: Bug ratio by sprint
    """
    bug_ratio_by_sprint = stories_df.groupby('sprint_number').apply(
        lambda x: len(x[x['story_type'] == 'Bug']) / len(x) * 100 if len(x) > 0 else 0
    ).reset_index()

    bug_ratio_by_sprint.columns = ['sprint_number', 'bug_ratio_pct']

    return bug_ratio_by_sprint
