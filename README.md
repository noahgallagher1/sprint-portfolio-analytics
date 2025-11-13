# Sprint Portfolio Analytics Dashboard

**An interactive analytics platform demonstrating advanced data science, statistical modeling, and business intelligence capabilities for Agile teams.**

By Noah Gallagher | [Dashboard](https://sprint-portfolio-analytics-bfvfhcrlagola34wftvxm3.streamlit.app/) | [LinkedIn](https://www.linkedin.com/in/noahgallagher/) | [GitHub](https://github.com/noahgallagher1/sprint-portfolio-analytics)

---

## 📊 Project Overview

This project showcases end-to-end data science and analytics capabilities through a production-ready dashboard that transforms sprint data into actionable business intelligence. Built with Python, Streamlit, and advanced statistical modeling, it demonstrates proficiency in data visualization, predictive analytics, and strategic decision support.

### What This Project Demonstrates

**Data Science & Analytics Skills:**
- Statistical modeling and trend analysis
- Predictive analytics using Monte Carlo simulations
- Portfolio optimization algorithms
- Risk assessment modeling
- Interactive data visualization
- Business intelligence dashboard development

**Technical Capabilities:**
- Python ecosystem (Pandas, NumPy, SciPy, Plotly)
- Streamlit application development
- Data processing pipelines
- Statistical analysis and hypothesis testing
- Performance optimization and caching
- Modular software architecture

**Business Impact:**
- Transforms raw sprint data into strategic insights
- Enables data-driven portfolio prioritization
- Provides predictive capacity planning
- Identifies delivery risks 2-3 sprints in advance
- Quantifies team performance and bottlenecks

---

## 🎯 Business Problem

Modern Agile teams face critical challenges:
- **Portfolio Visibility**: Difficulty prioritizing initiatives across competing needs
- **Predictability**: Uncertainty in sprint commitments and delivery timelines
- **Resource Optimization**: Suboptimal capacity allocation leading to burnout
- **Risk Management**: Late discovery of at-risk initiatives
- **Data-Driven Decisions**: Reliance on intuition vs quantitative insights

This dashboard addresses these challenges through comprehensive analytics and predictive modeling.

---

## 🚀 Dashboard Features

### 4 Interactive Tabs

#### 1. 📊 Executive Summary
**Purpose**: High-level performance overview with key metrics and trends

**Components**:
- **5 KPI Cards**: Current velocity, average velocity (12 months), completion rate, sprint health score, total initiatives
- **Velocity Trend Chart**: Historical velocity with 3-sprint rolling average
- **Portfolio Composition**: Distribution across Quick Wins, Major Projects, Fill-ins, and Time Sinks
- **Team Performance Heatmap**: Capacity utilization by team member across last 6 sprints
- **Work Distribution**: Stacked area chart showing story types (Features, Bugs, Technical Debt, Spikes) over time
- **Strategic Insights**: Automated recommendations based on data patterns
- **Business Value Summary**: ROI and portfolio optimization results

**Analytics Applied**:
- Rolling window calculations
- Trend analysis
- Composite health scoring
- Automated insight generation

---

#### 2. 🎯 Portfolio & Strategy
**Purpose**: Data-driven initiative prioritization and ROI analysis

**Components**:
- **Impact/Effort Matrix**: Interactive scatter plot with 4-quadrant classification
  - Quick Wins: High impact, low effort
  - Major Projects: High impact, high effort
  - Fill-ins: Low impact, low effort
  - Time Sinks: Low impact, high effort
- **Portfolio Composition Chart**: Initiative distribution by quadrant
- **Top Quick Wins**: Ranked list of high-ROI initiatives
- **Time Sinks to Deprioritize**: Low-ROI initiatives consuming resources
- **Velocity Stability Analysis**: Trend chart with rolling statistics
- **ROI Scatter Plot**: Completed initiatives by impact vs effort
- **Key Metrics**: Velocity improvement, predictability score, success rate, total delivered

**Analytics Applied**:
- Priority scoring algorithm: `(Impact / Effort) × Strategic Weight × ROI Multiplier`
- Quadrant classification based on threshold analysis
- Portfolio composition optimization
- Linear regression for trend analysis
- ROI calculation and ranking

---

#### 3. ⚡ Delivery & Performance
**Purpose**: Sprint-level deep dive and predictive analytics

**Components**:
- **Sprint Selector**: Dropdown to analyze any of 12 sprints
- **Sprint Overview Metrics**: Committed points, completed points, completion rate, capacity utilization
- **Story Status Pie Chart**: Distribution of completed, in progress, not started, blocked stories
- **Cycle Time Box Plot**: Distribution analysis with outlier detection
- **Team Performance Bar Chart**: Velocity contribution by team member
- **Sprint Health Gauge**: 0-100 composite health score with color zones
- **Initiative Risk Distribution**: Breakdown by Low/Medium/High risk
- **Velocity Forecast**: 3-sprint prediction with confidence intervals

**Analytics Applied**:
- Sprint health composite score: `(Velocity Consistency × 0.30) + (Estimation Accuracy × 0.25) + (Completion Rate × 0.25) + (Blocker Impact × 0.20)`
- Box plot statistical analysis (quartiles, outliers)
- Multi-factor risk scoring
- Monte Carlo simulation for forecasting
- Capacity utilization thresholds (optimal: 85-95%)

---

#### 4. 📚 About the Data
**Purpose**: Data schema reference and metric definitions

**Components**:
- **Data Overview**: Sprint, story, and initiative counts
- **Sprint Timeline Table**: All 12 sprints with key metrics
- **Story Type Breakdown**: Distribution pie chart
- **Initiative Status**: Bar chart of active, completed, backlog, deprioritized
- **Metric Definitions**: Comprehensive glossary
- **Usage Guide**: Step-by-step navigation instructions

**Value**: Ensures transparency and enables users to understand calculation methodologies

---

## 📈 Key Metrics & Formulas

### Sprint Health Score (0-100)

**Formula**:
```
Health = (Velocity Consistency × 0.30) +
         (Estimation Accuracy × 0.25) +
         (Completion Rate × 0.25) +
         (Blocker Impact × 0.20)
```

**Components**:
1. **Velocity Consistency**: `1 - (std_dev / mean)` - Lower variance = higher score
2. **Estimation Accuracy**: Actual vs estimated story points
3. **Completion Rate**: Completed / committed points
4. **Blocker Impact**: `1 - blocker_rate` - Fewer blockers = higher score

**Interpretation**:
- 80-100 (Green): Excellent - Sprint on track
- 60-79 (Yellow): Monitor - Some concerns
- 0-59 (Red): At Risk - Intervention needed

---

### Initiative Priority Score

**Formula**:
```
Priority = (Impact Score / Effort Score) × Strategic Weight × ROI Multiplier

Strategic Weights:
- Revenue Growth: 1.5×
- Customer Experience: 1.3×
- Cost Reduction: 1.2×
- Technical Excellence: 1.1×
- Process Improvement: 1.0×

ROI Multipliers:
- High: 1.3×
- Medium: 1.0×
- Low: 0.7×
```

**Example**:
```
Initiative: "API Integration Platform"
Impact: 9/10, Effort: 3/10
Strategic Category: Revenue Growth (1.5×)
ROI Estimate: High (1.3×)

Priority = (9/3) × 1.5 × 1.3 = 3.0 × 1.95 = 5.85
```

**Usage**: Enables objective, data-driven portfolio prioritization aligned with business strategy.

---

### Monte Carlo Completion Probability

**Method**: 1000 simulation iterations using historical velocity distribution

**Output**: Probability distribution for next sprint completion

**Example**: "87% probability of completing 42 points in next sprint"

**Usage**: Quantifies sprint planning risk with statistical confidence

---

### Initiative Risk Score

**Factors**:
1. **Capacity Risk (35%)**: Remaining work vs available team capacity
2. **Volatility Risk (25%)**: Historical velocity variance
3. **Utilization Risk (25%)**: Current team over/under-utilization
4. **Progress Risk (15%)**: Actual vs expected completion rate

**Thresholds**:
- <0.3: Low Risk - On track
- 0.3-0.6: Medium Risk - Monitor closely
- >0.6: High Risk - Immediate intervention required

**Usage**: Prioritizes attention on at-risk initiatives for proactive mitigation

---

### Predictability Score

**Formula**: `1 - Coefficient of Variation` where `CV = std_dev / mean_velocity`

**Interpretation**:
- 0.90-1.00 (90-100%): Highly predictable team
- 0.75-0.90 (75-90%): Predictable
- 0.60-0.75 (60-75%): Moderate variance
- <0.60 (<60%): High variance, difficult to forecast

**Usage**: Assesses reliability of velocity for capacity planning

---

## 🛠️ Technical Architecture

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.9+ | Core application logic |
| **Dashboard Framework** | Streamlit | Interactive web interface |
| **Data Processing** | Pandas | Data manipulation and aggregation |
| **Numerical Computing** | NumPy | Array operations and calculations |
| **Statistical Analysis** | SciPy | Statistical tests and distributions |
| **Machine Learning** | scikit-learn | Predictive modeling |
| **Visualization** | Plotly | Interactive charts and graphs |

### Project Structure

```
sprint-portfolio-analytics/
├── app.py                          # Main Streamlit application (4 tabs)
├── data/
│   ├── generate_data.py            # Realistic data generation script
│   ├── sprint_data.csv             # Sprint-level metrics (12 sprints)
│   ├── story_data.csv              # Story-level data (355 stories)
│   ├── initiative_data.csv         # Initiative data (28 initiatives)
│   └── team_data.csv               # Team member data (8-10 members)
├── utils/
│   ├── data_processing.py          # Data loading & transformation
│   ├── metrics.py                  # Sprint & portfolio metrics
│   ├── prioritization.py           # Initiative scoring & ranking
│   ├── predictive_models.py        # Risk scoring & forecasting
│   └── visualizations.py           # Reusable Plotly charts
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── USER_GUIDE.md                   # Comprehensive user documentation
└── METRICS_VALIDATION_REPORT.md   # Metrics accuracy validation
```

### Design Principles

**1. Modular Architecture**
- Separation of concerns: data, business logic, visualization layers
- Reusable utility functions for maintainability
- Clear module boundaries with defined interfaces

**2. Performance Optimization**
- `@st.cache_data` decorator for data loading (sub-second page loads)
- `@st.cache_resource` for expensive computations
- Vectorized Pandas operations (no loops)
- Efficient memory management

**3. Data Quality**
- Input validation and error handling
- Consistent data schema across all modules
- Realistic data generation with edge cases
- Statistical validation of metrics

**4. Extensibility**
- Easy integration with real data sources (Jira API, CSV export)
- Pluggable metrics framework (add custom KPIs)
- Configurable thresholds and weights
- Template for adding new visualizations

---

## 🚀 Installation & Usage

### Quick Start

```bash
# Clone repository
git clone https://github.com/noahgallagher1/sprint-portfolio-analytics.git
cd sprint-portfolio-analytics

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python data/generate_data.py

# Launch dashboard
streamlit run app.py
```

Dashboard will open automatically at `http://localhost:8501`

### System Requirements
- Python 3.9 or higher
- 4GB RAM minimum (8GB recommended)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for initial package installation)

### Using Your Own Data

**Option 1: CSV Import**

Replace generated CSV files in `/data` folder with your own data following the same schema:

| File | Required Columns |
|------|------------------|
| `sprint_data.csv` | sprint_number, velocity, committed_points, completed_points, completion_rate, team_capacity |
| `story_data.csv` | story_id, sprint_number, story_type, status, story_points, final_story_points, cycle_time_days, assignee_id |
| `initiative_data.csv` | initiative_id, name, impact_score, effort_score, strategic_category, status, total_story_points, roi_estimate |
| `team_data.csv` | member_id, name, role, avg_capacity_per_sprint |

**Option 2: API Integration**

Modify `utils/data_processing.py` to connect to Jira, Azure DevOps, or other project management tools:

```python
from jira import JIRA

jira = JIRA(
    server='https://your-domain.atlassian.net',
    basic_auth=('email', 'api_token')
)

# Fetch sprint data
issues = jira.search_issues('project=ABC AND sprint=12')

# Transform to DataFrame format
df = pd.DataFrame([{
    'story_id': issue.key,
    'story_points': issue.fields.customfield_10106,
    'status': issue.fields.status.name,
    # ... more fields
} for issue in issues])
```

---

## 📊 Sample Insights Generated

### Portfolio Optimization
```
Analysis: 28 initiatives analyzed
- 8 Quick Wins (high impact, low effort) - PRIORITIZE
- 5 Major Projects (high impact, high effort) - strategic investments
- 10 Fill-ins (low impact, low effort) - capacity fillers
- 5 Time Sinks (low impact, high effort) - DEPRIORITIZE

Recommendation: Reallocate 55 story points from Time Sinks to Quick Wins
Expected Impact: +35% portfolio ROI
```

### Velocity Forecasting
```
Historical Average: 41.8 points/sprint (std dev: 5.4)
Predictability Score: 87% (high confidence)

Next 3 Sprint Forecast:
- Sprint 13: 44 points (80% confidence interval: 39-49)
- Sprint 14: 45 points (80% confidence interval: 40-50)
- Sprint 15: 46 points (80% confidence interval: 41-51)

Capacity Planning: Can commit to 135 points over next 3 sprints with 80% confidence
```

### Risk Identification
```
High-Risk Initiatives (3):
1. "Microservices Migration" - 89 points remaining, team at 95% capacity
   Risk Factors: Capacity (0.8), Volatility (0.6), Progress (0.5)
   Recommendation: Extend timeline by 2 sprints or add 1 engineer

2. "API Integration Platform" - Blocked dependencies, 60 points remaining
   Risk Factors: Blocker (0.9), Progress (0.7)
   Recommendation: Resolve external dependency before next sprint

3. "Legacy System Upgrade" - Estimation accuracy 65%, high variance
   Risk Factors: Volatility (0.7), Estimation (0.6)
   Recommendation: Break into smaller stories, improve estimation
```

---

## 🎓 Key Learnings & Insights

### Data Science Techniques Applied

**1. Statistical Modeling**
- Linear regression for velocity trend analysis
- Box plot analysis for outlier detection
- Correlation analysis (blockers vs cycle time)
- Distribution fitting for Monte Carlo simulation

**2. Predictive Analytics**
- Monte Carlo simulation (1000 iterations per forecast)
- Rolling window forecasting
- Confidence interval calculation
- Risk factor weighting and composite scoring

**3. Optimization Algorithms**
- Portfolio prioritization using multi-objective scoring
- Quadrant classification based on threshold optimization
- Capacity allocation optimization
- ROI maximization framework

**4. Data Visualization Best Practices**
- Color theory for data representation (red/yellow/green zones)
- Interactive elements (hover details, drill-downs)
- Executive-friendly dashboards (3-second rule)
- Responsive layouts for different screen sizes

### Business Intelligence Skills

**1. Metric Design**
- Composite scoring methodologies
- Threshold determination based on business context
- Leading vs lagging indicators
- Actionable vs informational metrics

**2. Stakeholder Communication**
- Translating technical metrics into business language
- Executive summary dashboards
- Data storytelling through visualizations
- Recommendation engines for decision support

**3. Process Improvement**
- Bottleneck identification algorithms
- Team performance analytics
- Estimation accuracy tracking
- Continuous improvement frameworks

---

## 🔮 Future Enhancements

### Phase 2 Features (Planned)

**1. Real-Time Integration**
- Jira/Azure DevOps API connections
- Automated daily data refresh
- Webhook notifications for status changes
- Live sprint tracking

**2. Advanced Analytics**
- Machine learning models for burnout prediction
- NLP for story complexity analysis
- Dependency network graph visualization
- Team morale indicators based on patterns

**3. Enhanced Visualizations**
- Sankey diagrams for initiative flow
- Gantt charts for timeline visualization
- Network graphs for dependency mapping
- Animated trend visualizations

**4. Export & Reporting**
- PDF report generation
- PowerPoint export for presentations
- CSV data downloads
- Scheduled email summaries

**5. Collaboration Features**
- Multi-user access control
- Inline commenting on initiatives
- Sprint retrospective tracking
- Custom dashboard creation

---

## 📞 Contact & Links

**Noah Gallagher**
- **Email**: noahgallagher1@gmail.com
- **LinkedIn**: [linkedin.com/in/noahgallagher](https://www.linkedin.com/in/noahgallagher/)
- **GitHub**: [github.com/noahgallagher1/sprint-portfolio-analytics](https://github.com/noahgallagher1/sprint-portfolio-analytics)

### Additional Documentation
- **User Guide**: See `USER_GUIDE.md` for comprehensive step-by-step documentation
- **Metrics Validation**: See `METRICS_VALIDATION_REPORT.md` for formula verification
- **Quick Start**: See `QUICKSTART.md` for installation and basic usage

---

## 📄 License & Usage

This project is created as a portfolio demonstration piece. Feel free to use for educational purposes, personal projects, or as inspiration for your own analytics dashboards.

For commercial use or questions about implementation, please contact: noahgallagher1@gmail.com

---

## 🏆 Project Highlights

**Data Science Proficiency**:
- End-to-end data pipeline development
- Statistical modeling and validation
- Predictive analytics implementation
- Interactive visualization design

**Technical Excellence**:
- Modular, maintainable codebase
- Performance-optimized algorithms
- Comprehensive error handling
- Production-ready code quality

**Business Acumen**:
- Translates data into actionable insights
- Solves real business problems
- Demonstrates ROI quantification
- Executive-level communication

---

**Created by Noah Gallagher**
*Demonstrating Data Science & Analytics Expertise*

---

## 📚 Technologies Demonstrated

| Category | Skills |
|----------|--------|
| **Programming** | Python, Pandas, NumPy, SciPy |
| **Data Visualization** | Plotly, Streamlit, Interactive Dashboards |
| **Statistical Analysis** | Regression, Distributions, Hypothesis Testing |
| **Predictive Modeling** | Monte Carlo Simulation, Risk Scoring, Forecasting |
| **Software Engineering** | Modular Architecture, Caching, Performance Optimization |
| **Business Intelligence** | KPI Design, Executive Dashboards, Decision Support |
| **Data Processing** | ETL Pipelines, Data Cleaning, Schema Design |
| **Version Control** | Git, GitHub, Documentation |

---

*This dashboard transforms sprint data into strategic intelligence, enabling data-driven decision-making and predictive planning.*
