"""
Predictive Models & Risk Assessment

Monte Carlo simulations, risk scoring, and forecasting capabilities.
"""

import pandas as pd
import numpy as np
from scipy import stats


def predict_sprint_completion_probability(committed_points, historical_velocities, n_simulations=1000):
    """
    Monte Carlo simulation to predict probability of completing committed points.

    Args:
        committed_points: Story points committed for next sprint
        historical_velocities: List or array of historical velocity values
        n_simulations: Number of Monte Carlo simulations (default 1000)

    Returns:
        dict: Prediction results with probability and confidence intervals
    """
    if len(historical_velocities) < 2:
        return {
            'probability': 0.5,
            'expected_velocity': committed_points,
            'confidence_interval_10': committed_points,
            'confidence_interval_90': committed_points,
            'simulated_velocities': []
        }

    # Fit normal distribution to historical velocities
    mean_velocity = np.mean(historical_velocities)
    std_velocity = np.std(historical_velocities)

    # Run Monte Carlo simulations
    simulated_velocities = np.random.normal(mean_velocity, std_velocity, n_simulations)

    # Ensure no negative velocities
    simulated_velocities = np.maximum(simulated_velocities, 0)

    # Count successful completions (velocity >= committed points)
    successful_completions = np.sum(simulated_velocities >= committed_points)

    # Calculate probability
    probability = successful_completions / n_simulations

    # Calculate confidence intervals
    percentile_10 = np.percentile(simulated_velocities, 10)
    percentile_50 = np.percentile(simulated_velocities, 50)
    percentile_90 = np.percentile(simulated_velocities, 90)

    return {
        'probability': probability,
        'expected_velocity': mean_velocity,
        'median_velocity': percentile_50,
        'confidence_interval_10': percentile_10,
        'confidence_interval_90': percentile_90,
        'simulated_velocities': simulated_velocities,
        'committed_points': committed_points
    }


def calculate_initiative_risk_score(initiative, current_sprint, avg_velocity, velocity_std, team_utilization):
    """
    Calculate comprehensive risk score for initiative delivery.

    Risk factors:
    1. Remaining effort vs available capacity (35%)
    2. Historical velocity variance/volatility (25%)
    3. Current team utilization (25%)
    4. Progress rate (15%)

    Args:
        initiative: Initiative data (Series or dict)
        current_sprint: Current sprint number
        avg_velocity: Average team velocity
        velocity_std: Velocity standard deviation
        team_utilization: Current team utilization (0-1+)

    Returns:
        dict: Risk assessment with score, level, and factors
    """
    # Extract initiative data
    total_points = initiative.get('total_story_points', 0)
    completed_points = initiative.get('completed_story_points', 0)
    target_sprint = initiative.get('target_sprint', current_sprint + 10)
    status = initiative.get('status', 'Backlog')

    # If already completed or deprioritized, no risk
    if status in ['Completed', 'Deprioritized']:
        return {
            'risk_score': 0,
            'risk_level': 'None',
            'factors': {},
            'recommendation': 'No action needed'
        }

    # Calculate remaining effort
    remaining_points = max(0, total_points - completed_points)

    # Calculate sprints available
    sprints_available = max(1, target_sprint - current_sprint)

    # Calculate capacity available
    capacity_available = avg_velocity * sprints_available

    # --- FACTOR 1: Capacity Risk (35%) ---
    if capacity_available > 0:
        capacity_ratio = remaining_points / capacity_available
        # Risk increases as we need more than 80% of capacity
        capacity_risk = min(1.0, capacity_ratio / 0.8)
    else:
        capacity_risk = 1.0

    # --- FACTOR 2: Volatility Risk (25%) ---
    if avg_velocity > 0:
        coefficient_of_variation = velocity_std / avg_velocity
        # Risk increases with higher CV (>15% CV is risky)
        volatility_risk = min(1.0, coefficient_of_variation / 0.15)
    else:
        volatility_risk = 0.5

    # --- FACTOR 3: Utilization Risk (25%) ---
    if team_utilization > 1.05:
        utilization_risk = 0.9
    elif team_utilization > 0.95:
        utilization_risk = 0.5
    elif team_utilization > 0.70:
        utilization_risk = 0.2
    else:
        utilization_risk = 0.4  # Under-utilization can also be a risk signal

    # --- FACTOR 4: Progress Risk (15%) ---
    if total_points > 0:
        completion_pct = completed_points / total_points

        # Calculate expected progress (linear assumption)
        # If we're at current sprint and target is target_sprint, expected progress = (current-start)/(target-start)
        # Simplified: assume initiative should be proportionally complete
        if status == 'Active':
            # For active initiatives, check if on track
            # Rough heuristic: if we're past 50% of timeline but less than 50% complete, that's risky
            if sprints_available < 3 and completion_pct < 0.5:
                progress_risk = 0.8
            elif completion_pct < 0.3:
                progress_risk = 0.6
            else:
                progress_risk = 0.2
        else:
            # Backlog items - low progress risk until activated
            progress_risk = 0.1
    else:
        progress_risk = 0.5

    # --- COMPOSITE RISK SCORE (0-1) ---
    risk_score = (
        capacity_risk * 0.35 +
        volatility_risk * 0.25 +
        utilization_risk * 0.25 +
        progress_risk * 0.15
    )

    # Determine risk level
    if risk_score < 0.3:
        risk_level = "Low"
        recommendation = "No action needed - on track for delivery"
    elif risk_score < 0.6:
        risk_level = "Medium"
        recommendation = "Monitor closely - may need resource adjustment or scope review"
    else:
        risk_level = "High"
        if capacity_risk > 0.7:
            recommendation = "High risk - consider descoping, extending timeline, or adding resources"
        else:
            recommendation = "High risk - immediate intervention needed"

    return {
        'risk_score': risk_score,
        'risk_level': risk_level,
        'factors': {
            'capacity_risk': capacity_risk,
            'volatility_risk': volatility_risk,
            'utilization_risk': utilization_risk,
            'progress_risk': progress_risk
        },
        'remaining_points': remaining_points,
        'sprints_available': sprints_available,
        'capacity_available': capacity_available,
        'recommendation': recommendation
    }


def assess_all_initiatives_risk(initiatives_df, current_sprint, sprints_df, team_utilization=0.85):
    """
    Assess risk for all active and backlog initiatives.

    Args:
        initiatives_df: Initiatives DataFrame
        current_sprint: Current sprint number
        sprints_df: Sprint DataFrame for velocity calculation
        team_utilization: Current team utilization (default 0.85)

    Returns:
        DataFrame: Initiatives with risk assessments
    """
    # Calculate velocity statistics
    recent_velocities = sprints_df.tail(5)['velocity'].values
    avg_velocity = np.mean(recent_velocities)
    velocity_std = np.std(recent_velocities)

    # Filter to active and backlog initiatives
    df = initiatives_df[initiatives_df['status'].isin(['Active', 'Backlog'])].copy()

    # Calculate risk for each
    risk_assessments = []

    for _, initiative in df.iterrows():
        risk = calculate_initiative_risk_score(
            initiative,
            current_sprint,
            avg_velocity,
            velocity_std,
            team_utilization
        )

        risk_assessments.append({
            'initiative_id': initiative['initiative_id'],
            'name': initiative['name'],
            'status': initiative['status'],
            'risk_score': risk['risk_score'],
            'risk_level': risk['risk_level'],
            'capacity_risk': risk['factors']['capacity_risk'],
            'volatility_risk': risk['factors']['volatility_risk'],
            'utilization_risk': risk['factors']['utilization_risk'],
            'progress_risk': risk['factors']['progress_risk'],
            'remaining_points': risk['remaining_points'],
            'sprints_available': risk['sprints_available'],
            'recommendation': risk['recommendation']
        })

    risk_df = pd.DataFrame(risk_assessments)

    # Sort by risk score descending
    risk_df = risk_df.sort_values('risk_score', ascending=False)

    return risk_df


def forecast_velocity_next_n_sprints(sprints_df, n_sprints=3):
    """
    Forecast velocity for next N sprints using historical trends.

    Uses simple moving average with trend adjustment.

    Args:
        sprints_df: Sprint DataFrame
        n_sprints: Number of sprints to forecast

    Returns:
        dict: Forecast with confidence intervals
    """
    velocities = sprints_df['velocity'].values
    sprint_numbers = sprints_df['sprint_number'].values

    if len(velocities) < 3:
        # Not enough data for reliable forecast
        avg = np.mean(velocities) if len(velocities) > 0 else 40
        return {
            'forecast': [avg] * n_sprints,
            'lower_bound': [avg * 0.8] * n_sprints,
            'upper_bound': [avg * 1.2] * n_sprints
        }

    # Use last 5 sprints for trend
    recent_velocities = velocities[-5:]
    recent_sprint_nums = sprint_numbers[-5:]

    # Calculate trend
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        recent_sprint_nums, recent_velocities
    )

    # Calculate moving average
    moving_avg = np.mean(recent_velocities)

    # Standard deviation for confidence intervals
    std_velocity = np.std(recent_velocities)

    # Forecast
    last_sprint = sprint_numbers[-1]
    forecast = []
    lower_bounds = []
    upper_bounds = []

    for i in range(1, n_sprints + 1):
        future_sprint = last_sprint + i

        # Trend-adjusted forecast
        trend_forecast = slope * future_sprint + intercept

        # Weighted average of trend and moving average (more weight to trend if strong correlation)
        if abs(r_value) > 0.5:
            predicted_velocity = 0.7 * trend_forecast + 0.3 * moving_avg
        else:
            predicted_velocity = 0.3 * trend_forecast + 0.7 * moving_avg

        # Ensure reasonable bounds
        predicted_velocity = max(20, min(60, predicted_velocity))

        forecast.append(predicted_velocity)

        # Confidence intervals (1.5 std for ~86% confidence)
        lower_bounds.append(max(15, predicted_velocity - 1.5 * std_velocity))
        upper_bounds.append(min(70, predicted_velocity + 1.5 * std_velocity))

    return {
        'forecast': forecast,
        'lower_bound': lower_bounds,
        'upper_bound': upper_bounds,
        'avg_velocity': moving_avg,
        'trend_slope': slope
    }


def generate_predictive_recommendations(sprints_df, stories_df, initiatives_df, team_df):
    """
    Generate data-driven predictive recommendations.

    Args:
        sprints_df: Sprint DataFrame
        stories_df: Stories DataFrame
        initiatives_df: Initiatives DataFrame
        team_df: Team DataFrame

    Returns:
        list: List of recommendations
    """
    recommendations = []

    # Get current sprint
    current_sprint = sprints_df.iloc[-1]
    current_sprint_num = current_sprint['sprint_number']

    # Get last 3 sprints velocity
    recent_velocities = sprints_df.tail(3)['velocity'].values
    avg_recent_velocity = np.mean(recent_velocities)

    # 1. Sprint health prediction
    from .metrics import calculate_sprint_health_score
    health = calculate_sprint_health_score(current_sprint, sprints_df)

    if health['health_score'] < 70:
        recommendations.append({
            'category': 'Sprint Health',
            'priority': 'High',
            'insight': f'Current sprint health score is {health["health_score"]:.0f}/100 (below healthy threshold)',
            'recommendation': 'Review sprint commitments and address blockers proactively. Consider reducing scope for current sprint.',
            'impact': 'Prevents sprint failure and team burnout'
        })

    # 2. Estimation accuracy
    recent_stories = stories_df[stories_df['sprint_number'] >= current_sprint_num - 2]
    avg_accuracy = recent_stories['estimation_accuracy'].mean()

    if avg_accuracy < 0.75:
        recommendations.append({
            'category': 'Estimation',
            'priority': 'Medium',
            'insight': f'Recent estimation accuracy is {avg_accuracy*100:.0f}% (target: >85%)',
            'recommendation': 'Conduct estimation calibration session. Consider increasing story point estimates for historically underestimated work types.',
            'impact': 'Improves sprint predictability and team confidence'
        })

    # 3. Cycle time optimization
    avg_cycle_time = recent_stories['cycle_time_days'].mean()

    # Check for stories taking too long
    if avg_cycle_time > 7:
        recommendations.append({
            'category': 'Cycle Time',
            'priority': 'Medium',
            'insight': f'Average cycle time is {avg_cycle_time:.1f} days (target: <7 days)',
            'recommendation': 'Break down larger stories into smaller increments. Review WIP limits and consider pair programming for faster completion.',
            'impact': 'Faster value delivery and improved flow'
        })

    # 4. Capacity planning for next sprint
    # Simulate next sprint with recommended commitment
    optimal_commitment = int(avg_recent_velocity * 0.95)  # Slightly conservative

    recommendations.append({
        'category': 'Capacity Planning',
        'priority': 'High',
        'insight': f'Based on last 3 sprints (avg velocity: {avg_recent_velocity:.0f}), optimal commitment is {optimal_commitment} points',
        'recommendation': f'Recommend committing {optimal_commitment}±3 points for next sprint to maintain healthy 95% completion rate.',
        'impact': 'Maximizes throughput while maintaining sustainable pace'
    })

    # 5. Team utilization
    team_metrics = stories_df.groupby('assignee_id').agg({
        'final_story_points': 'sum',
        'story_id': 'count'
    }).reset_index()

    team_metrics = team_metrics.merge(team_df[['member_id', 'name', 'avg_capacity_per_sprint']],
                                     left_on='assignee_id', right_on='member_id')

    num_sprints = sprints_df['sprint_number'].nunique()
    team_metrics['avg_per_sprint'] = team_metrics['final_story_points'] / num_sprints
    team_metrics['utilization'] = team_metrics['avg_per_sprint'] / team_metrics['avg_capacity_per_sprint']

    # Check for over-utilized members
    overutilized = team_metrics[team_metrics['utilization'] > 1.05]

    if len(overutilized) > 0:
        overutilized_names = ', '.join(overutilized['name'].head(2).tolist())
        recommendations.append({
            'category': 'Team Capacity',
            'priority': 'High',
            'insight': f'{len(overutilized)} team member(s) consistently over-utilized (>105%): {overutilized_names}',
            'recommendation': 'Rebalance work distribution or increase capacity in bottleneck areas. Risk of burnout if sustained.',
            'impact': 'Prevents burnout and improves team sustainability'
        })

    # 6. At-risk initiatives
    team_utilization = current_sprint['completed_points'] / current_sprint['team_capacity']
    risk_assessments = assess_all_initiatives_risk(
        initiatives_df, current_sprint_num, sprints_df, team_utilization
    )

    high_risk = risk_assessments[risk_assessments['risk_level'] == 'High']

    if len(high_risk) > 0:
        recommendations.append({
            'category': 'Initiative Risk',
            'priority': 'High',
            'insight': f'{len(high_risk)} initiative(s) at high risk of missing target dates',
            'recommendation': f'Immediate review needed for: {high_risk.iloc[0]["name"]}. Consider descoping, extending timeline, or adding resources.',
            'impact': 'Prevents initiative failures and sets realistic stakeholder expectations'
        })

    return recommendations


def calculate_probability_distribution_chart_data(committed_points, historical_velocities, n_simulations=1000):
    """
    Generate data for probability distribution visualization.

    Args:
        committed_points: Committed story points
        historical_velocities: Historical velocity values
        n_simulations: Number of simulations

    Returns:
        dict: Data for plotting histogram/distribution
    """
    prediction = predict_sprint_completion_probability(
        committed_points, historical_velocities, n_simulations
    )

    # Create histogram data
    hist, bin_edges = np.histogram(prediction['simulated_velocities'], bins=30)

    return {
        'hist_counts': hist.tolist(),
        'bin_edges': bin_edges.tolist(),
        'committed_points': committed_points,
        'probability': prediction['probability'],
        'expected_velocity': prediction['expected_velocity']
    }
