# Quick Start Guide

Get the dashboard running in 3 minutes!

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation Steps

### 1. Clone Repository

```bash
git clone [your-repo-url]
cd sprint-portfolio-analytics
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- streamlit (dashboard framework)
- pandas (data processing)
- plotly (interactive charts)
- numpy, scipy, scikit-learn (analytics)

### 3. Generate Sample Data

```bash
python data/generate_data.py
```

This creates:
- 12 sprints of data (6 months)
- 355 user stories
- 28 portfolio initiatives
- 8 team members

### 4. Launch Dashboard

```bash
streamlit run app.py
```

Dashboard opens automatically at `http://localhost:8501`

## What to Explore

### Tab 1: 📊 Executive Summary
- View team velocity trends
- Check current sprint health (0-100 score)
- See portfolio composition across Quick Wins, Major Projects, Fill-ins, and Time Sinks
- Review team performance heatmap
- Get automated strategic insights and recommendations

### Tab 2: 🎯 Portfolio & Strategy
- Explore Impact vs Effort matrix with 4-quadrant classification
- Find "Quick Wins" (high impact, low effort initiatives)
- Identify "Time Sinks" to deprioritize
- Analyze velocity stability and predictability
- View ROI scatter plot of completed initiatives

### Tab 3: ⚡ Delivery & Performance
- Select any sprint (1-12) for deep dive analysis
- Analyze cycle times with box plots and outlier detection
- Review team performance bar charts
- Check sprint health gauge
- View initiative risk distribution (Low/Medium/High)
- See 3-sprint velocity forecast with confidence intervals

### Tab 4: 📚 About the Data
- Understand data schema and structure
- Review all sprint timeline metrics in table format
- See story type and initiative status distributions
- Read comprehensive metric definitions
- Learn how to navigate and interpret the dashboard

## Troubleshooting

### "Module not found" errors
```bash
pip install --upgrade -r requirements.txt
```

### "Data files not found"
```bash
python data/generate_data.py
```

### Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

## Using Your Own Data

Replace CSV files in `/data` folder:

**Required columns:**

`sprint_data.csv`:
- sprint_number, start_date, end_date, duration_days
- team_capacity, committed_points, completed_points
- velocity, team_size, completion_rate

`story_data.csv`:
- story_id, sprint_number, story_points, final_story_points
- story_type, initiative_id, status, cycle_time_days
- num_blockers, blocker_duration_days, assignee_id
- priority, dependencies_count, estimation_accuracy

`initiative_data.csv`:
- initiative_id, name, description
- impact_score, effort_score, strategic_category
- status, owner, total_story_points, completed_story_points
- target_sprint, actual_completion_sprint, roi_estimate

`team_data.csv`:
- member_id, name, role, avg_capacity_per_sprint, specialization

## Next Steps

1. **Explore the data** - Click through all 4 tabs
2. **Read the README** - Understand business value and metrics
3. **Review USER_GUIDE.md** - Comprehensive documentation with examples
4. **Customize** - Adjust thresholds, colors, and calculations
5. **Integrate** - Connect to your real data sources (Jira, etc.)

## Support

- Full documentation: See [README.md](README.md)
- Data generation: See `data/generate_data.py`
- Metrics logic: See `utils/metrics.py`
- Custom visualizations: See `utils/visualizations.py`

---

**Dashboard loads slow?**
- Data is cached automatically after first load
- Subsequent page changes are instant

**Want to share with team?**
- Deploy to Streamlit Cloud (free): https://streamlit.io/cloud
- Or use Docker for self-hosting

Enjoy exploring your sprint analytics! 📊
