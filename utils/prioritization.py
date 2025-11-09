"""
Initiative Prioritization & Portfolio Management

Handles scoring, ranking, and prioritization of portfolio initiatives.
"""

import pandas as pd
import numpy as np


# Strategic alignment weights
STRATEGIC_WEIGHTS = {
    'Revenue Growth': 1.5,
    'Customer Experience': 1.3,
    'Cost Reduction': 1.2,
    'Process Improvement': 1.0,
    'Technical Excellence': 1.1
}

# ROI multipliers
ROI_MULTIPLIERS = {
    'High': 1.3,
    'Medium': 1.0,
    'Low': 0.7
}


def calculate_priority_score(initiative):
    """
    Calculate comprehensive priority score for an initiative.

    Priority Score = (Impact / Effort) * Strategic Weight * ROI Multiplier

    Args:
        initiative: Initiative data (Series or dict)

    Returns:
        float: Priority score
    """
    # Base score: impact to effort ratio
    impact = initiative['impact_score']
    effort = initiative['effort_score']

    if effort == 0:
        return 0

    base_score = impact / effort

    # Strategic alignment multiplier
    strategic_category = initiative.get('strategic_category', 'Process Improvement')
    strategic_multiplier = STRATEGIC_WEIGHTS.get(strategic_category, 1.0)

    # ROI multiplier
    roi_estimate = initiative.get('roi_estimate', 'Medium')
    roi_multiplier = ROI_MULTIPLIERS.get(roi_estimate, 1.0)

    # Final priority score
    priority_score = base_score * strategic_multiplier * roi_multiplier

    return priority_score


def add_priority_scores(initiatives_df):
    """
    Add priority scores to initiatives DataFrame.

    Args:
        initiatives_df: Initiatives DataFrame

    Returns:
        DataFrame: Initiatives with priority scores
    """
    df = initiatives_df.copy()

    # Calculate priority score for each initiative
    df['priority_score'] = df.apply(calculate_priority_score, axis=1)

    # Add priority rank
    df['priority_rank'] = df['priority_score'].rank(ascending=False, method='dense').astype(int)

    # Categorize into priority tiers
    df['priority_tier'] = pd.cut(
        df['priority_score'],
        bins=[0, 1.5, 2.5, float('inf')],
        labels=['Low', 'Medium', 'High']
    )

    return df


def categorize_quadrant(initiative):
    """
    Categorize initiative into Impact/Effort quadrant.

    Quadrants:
    - Quick Wins: High Impact (>6), Low Effort (<=5)
    - Major Projects: High Impact (>6), High Effort (>5)
    - Fill-ins: Low Impact (<=6), Low Effort (<=5)
    - Time Sinks: Low Impact (<=6), High Effort (>5)

    Args:
        initiative: Initiative data (Series or dict)

    Returns:
        str: Quadrant name
    """
    impact = initiative['impact_score']
    effort = initiative['effort_score']

    if impact > 6 and effort <= 5:
        return 'Quick Wins'
    elif impact > 6 and effort > 5:
        return 'Major Projects'
    elif impact <= 6 and effort <= 5:
        return 'Fill-ins'
    else:
        return 'Time Sinks'


def add_quadrant_classification(initiatives_df):
    """
    Add quadrant classification to initiatives DataFrame.

    Args:
        initiatives_df: Initiatives DataFrame

    Returns:
        DataFrame: Initiatives with quadrant classification
    """
    df = initiatives_df.copy()
    df['quadrant'] = df.apply(categorize_quadrant, axis=1)
    return df


def get_portfolio_composition(initiatives_df):
    """
    Calculate portfolio composition across quadrants.

    Args:
        initiatives_df: Initiatives DataFrame

    Returns:
        DataFrame: Composition by quadrant
    """
    initiatives_with_quadrants = add_quadrant_classification(initiatives_df)

    composition = initiatives_with_quadrants.groupby('quadrant').agg({
        'initiative_id': 'count',
        'total_story_points': 'sum',
        'impact_score': 'mean',
        'effort_score': 'mean'
    }).reset_index()

    composition.columns = [
        'quadrant', 'initiative_count', 'total_points',
        'avg_impact', 'avg_effort'
    ]

    # Add percentages
    total_initiatives = composition['initiative_count'].sum()
    total_points = composition['total_points'].sum()

    composition['initiative_pct'] = (
        composition['initiative_count'] / total_initiatives * 100
        if total_initiatives > 0 else 0
    )
    composition['points_pct'] = (
        composition['total_points'] / total_points * 100
        if total_points > 0 else 0
    )

    return composition


def get_quick_wins(initiatives_df, limit=10):
    """
    Identify top quick-win opportunities.

    Quick wins are high priority initiatives in the "Quick Wins" quadrant.

    Args:
        initiatives_df: Initiatives DataFrame
        limit: Maximum number to return

    Returns:
        DataFrame: Top quick win initiatives
    """
    df = add_priority_scores(initiatives_df)
    df = add_quadrant_classification(df)

    quick_wins = df[df['quadrant'] == 'Quick Wins'].copy()
    quick_wins = quick_wins.sort_values('priority_score', ascending=False)

    return quick_wins.head(limit)


def get_time_sinks(initiatives_df):
    """
    Identify time sink initiatives that should be deprioritized.

    Args:
        initiatives_df: Initiatives DataFrame

    Returns:
        DataFrame: Time sink initiatives
    """
    df = add_quadrant_classification(initiatives_df)

    time_sinks = df[df['quadrant'] == 'Time Sinks'].copy()
    time_sinks = time_sinks.sort_values('effort_score', ascending=False)

    return time_sinks


def calculate_portfolio_health_score(initiatives_df):
    """
    Calculate overall portfolio health based on composition and progress.

    Health factors:
    - Quick wins ratio (positive)
    - Time sinks ratio (negative)
    - Active initiatives on track
    - Completion rate

    Args:
        initiatives_df: Initiatives DataFrame

    Returns:
        dict: Portfolio health metrics
    """
    df = add_quadrant_classification(initiatives_df)

    total_initiatives = len(df)

    # Quadrant distribution
    quick_wins_count = len(df[df['quadrant'] == 'Quick Wins'])
    time_sinks_count = len(df[df['quadrant'] == 'Time Sinks'])

    quick_wins_ratio = quick_wins_count / total_initiatives if total_initiatives > 0 else 0
    time_sinks_ratio = time_sinks_count / total_initiatives if total_initiatives > 0 else 0

    # Status distribution
    completed_count = len(df[df['status'] == 'Completed'])
    active_count = len(df[df['status'] == 'Active'])
    deprioritized_count = len(df[df['status'] == 'Deprioritized'])

    completion_rate = completed_count / total_initiatives if total_initiatives > 0 else 0

    # Calculate health score (0-100)
    health_score = (
        (quick_wins_ratio * 30) +                    # 30% for having quick wins
        ((1 - time_sinks_ratio) * 20) +              # 20% for avoiding time sinks
        (completion_rate * 30) +                      # 30% for completion rate
        ((1 - deprioritized_count / total_initiatives) * 20 if total_initiatives > 0 else 0)  # 20% for low deprioritization
    ) * 100

    return {
        'health_score': health_score,
        'quick_wins_ratio': quick_wins_ratio * 100,
        'time_sinks_ratio': time_sinks_ratio * 100,
        'completion_rate': completion_rate * 100,
        'active_count': active_count,
        'completed_count': completed_count,
        'deprioritized_count': deprioritized_count
    }


def simulate_capacity_allocation(initiatives_df, sprints_df, future_sprints=3):
    """
    Simulate capacity allocation for future sprints.

    Args:
        initiatives_df: Initiatives DataFrame
        sprints_df: Sprint DataFrame
        future_sprints: Number of future sprints to simulate

    Returns:
        dict: Capacity allocation simulation
    """
    # Calculate average team capacity
    avg_velocity = sprints_df['velocity'].tail(3).mean()

    # Available capacity for future sprints
    available_capacity = avg_velocity * future_sprints

    # Get active and backlog initiatives
    pending_initiatives = initiatives_df[
        initiatives_df['status'].isin(['Active', 'Backlog'])
    ].copy()

    # Add priority scores
    pending_initiatives = add_priority_scores(pending_initiatives)

    # Sort by priority
    pending_initiatives = pending_initiatives.sort_values('priority_score', ascending=False)

    # Calculate remaining effort
    pending_initiatives['remaining_points'] = (
        pending_initiatives['total_story_points'] -
        pending_initiatives['completed_story_points']
    )

    # Simulate allocation
    allocated = []
    capacity_used = 0

    for _, initiative in pending_initiatives.iterrows():
        remaining = initiative['remaining_points']

        if capacity_used + remaining <= available_capacity:
            allocated.append({
                'initiative_id': initiative['initiative_id'],
                'name': initiative['name'],
                'points_allocated': remaining,
                'priority_score': initiative['priority_score'],
                'fits_in_capacity': True
            })
            capacity_used += remaining
        else:
            # Can partially allocate
            points_available = available_capacity - capacity_used
            if points_available > 0:
                allocated.append({
                    'initiative_id': initiative['initiative_id'],
                    'name': initiative['name'],
                    'points_allocated': points_available,
                    'priority_score': initiative['priority_score'],
                    'fits_in_capacity': False
                })
                capacity_used = available_capacity
                break

    return {
        'available_capacity': available_capacity,
        'capacity_used': capacity_used,
        'capacity_utilization': (capacity_used / available_capacity * 100) if available_capacity > 0 else 0,
        'allocated_initiatives': allocated,
        'initiatives_fully_allocated': len([i for i in allocated if i['fits_in_capacity']])
    }


def generate_portfolio_recommendations(initiatives_df, sprints_df):
    """
    Generate data-driven recommendations for portfolio management.

    Args:
        initiatives_df: Initiatives DataFrame
        sprints_df: Sprint DataFrame

    Returns:
        list: List of recommendation dictionaries
    """
    recommendations = []

    # 1. Quick wins available
    quick_wins = get_quick_wins(initiatives_df, limit=5)
    if len(quick_wins[quick_wins['status'] == 'Backlog']) > 0:
        backlog_quick_wins = quick_wins[quick_wins['status'] == 'Backlog']
        total_points = backlog_quick_wins['total_story_points'].sum()
        recommendations.append({
            'type': 'Quick Wins',
            'priority': 'High',
            'title': f'{len(backlog_quick_wins)} Quick Win Initiatives Ready',
            'description': f'{len(backlog_quick_wins)} high-impact, low-effort initiatives identified with combined effort of {total_points} points.',
            'action': 'Prioritize these for immediate execution in next sprint.'
        })

    # 2. Time sinks to deprioritize
    time_sinks = get_time_sinks(initiatives_df)
    active_time_sinks = time_sinks[time_sinks['status'].isin(['Active', 'Backlog'])]
    if len(active_time_sinks) > 0:
        recommendations.append({
            'type': 'Time Sinks',
            'priority': 'Medium',
            'title': f'{len(active_time_sinks)} Low-Value Initiatives Consuming Resources',
            'description': f'{len(active_time_sinks)} low-impact, high-effort initiatives identified. These represent opportunity cost.',
            'action': 'Review and consider deprioritizing to free up capacity for higher-value work.'
        })

    # 3. Portfolio balance
    composition = get_portfolio_composition(initiatives_df)
    major_projects_pct = composition[composition['quadrant'] == 'Major Projects']['initiative_pct'].values
    if len(major_projects_pct) > 0 and major_projects_pct[0] > 40:
        recommendations.append({
            'type': 'Portfolio Balance',
            'priority': 'Medium',
            'title': 'Heavy Concentration in Major Projects',
            'description': f'{major_projects_pct[0]:.0f}% of initiatives are major projects (high impact, high effort).',
            'action': 'Balance portfolio with quick wins to maintain steady value delivery while major projects are in progress.'
        })

    # 4. Capacity planning
    capacity_sim = simulate_capacity_allocation(initiatives_df, sprints_df, future_sprints=3)
    if capacity_sim['capacity_utilization'] > 110:
        recommendations.append({
            'type': 'Capacity',
            'priority': 'High',
            'title': 'Capacity Overcommitment Detected',
            'description': f'Active initiatives require {capacity_sim["capacity_used"]:.0f} points but only {capacity_sim["available_capacity"]:.0f} points available in next 3 sprints.',
            'action': 'Review active initiatives and descope or deprioritize to match team capacity.'
        })

    # 5. Strategic alignment
    strategic_distribution = initiatives_df.groupby('strategic_category').size()
    total = len(initiatives_df)

    revenue_growth_pct = (strategic_distribution.get('Revenue Growth', 0) / total * 100) if total > 0 else 0

    if revenue_growth_pct < 20:
        recommendations.append({
            'type': 'Strategic Alignment',
            'priority': 'Medium',
            'title': 'Limited Revenue Growth Focus',
            'description': f'Only {revenue_growth_pct:.0f}% of initiatives directly target revenue growth.',
            'action': 'Consider increasing focus on revenue-generating initiatives to support business goals.'
        })

    return recommendations


def create_intake_funnel_data(initiatives_df):
    """
    Create data for initiative intake funnel visualization.

    Stages: Total → Backlog → Active → Completed

    Args:
        initiatives_df: Initiatives DataFrame

    Returns:
        DataFrame: Funnel data
    """
    total = len(initiatives_df)

    status_counts = initiatives_df['status'].value_counts().to_dict()

    funnel_data = pd.DataFrame([
        {'stage': 'Submitted', 'count': total, 'percentage': 100},
        {'stage': 'Backlog', 'count': status_counts.get('Backlog', 0),
         'percentage': (status_counts.get('Backlog', 0) / total * 100) if total > 0 else 0},
        {'stage': 'Active', 'count': status_counts.get('Active', 0),
         'percentage': (status_counts.get('Active', 0) / total * 100) if total > 0 else 0},
        {'stage': 'Completed', 'count': status_counts.get('Completed', 0),
         'percentage': (status_counts.get('Completed', 0) / total * 100) if total > 0 else 0}
    ])

    return funnel_data
