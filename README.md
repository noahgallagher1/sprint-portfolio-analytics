# Sprint Performance & Portfolio Analytics Dashboard

**A comprehensive Agile analytics platform demonstrating portfolio management, predictive insights, and data-driven decision-making**

## 📊 Project Overview

This project showcases a production-ready analytics dashboard that addresses real-world challenges in Agile product management and operations strategy. Built with Python and Streamlit

### Business Problem Solved

Modern product organizations struggle with:
- **Portfolio visibility:** Difficulty prioritizing initiatives across competing business needs
- **Predictability:** Uncertainty in sprint commitments and delivery timelines
- **Resource optimization:** Suboptimal capacity allocation and team burnout risks
- **Strategic alignment:** Disconnect between tactical execution and business goals
- **Data-driven decisions:** Reliance on gut feel vs. quantitative insights

This dashboard transforms sprint data into actionable intelligence, enabling proactive management and strategic portfolio optimization.

---



### Comprehensive Dashboard Pages

#### 1. 🎯 Executive Summary
**Purpose:** C-suite/Director level overview

**Features:**
- 5 key performance indicators (KPIs) with trends
- Velocity trend analysis with 3-sprint moving average
- Current sprint burndown projection
- Portfolio health snapshot
- Key business insights in plain language

**Business Value:** Provides leadership with instant visibility into team performance and portfolio health, enabling data-informed strategic decisions.

#### 2. 📋 Portfolio Prioritization
**Purpose:** Initiative intake, scoring, and backlog management

**Features:**
- Impact vs Effort priority matrix (4 quadrants)
- Initiative intake funnel visualization
- Sortable portfolio backlog table
- Quick wins identification
- Time sink detection and deprioritization recommendations
- Data-driven portfolio recommendations

**Business Value:** Transparent, objective prioritization framework that aligns team capacity with business strategy and maximizes ROI.

#### 3. 🔍 Sprint Deep Dive
**Purpose:** Detailed sprint performance analysis

**Features:**
- Sprint-level capacity vs delivery metrics
- Story completion distribution
- Cycle time analysis by story size
- Blocker impact assessment
- Sprint-over-sprint comparison
- Story type mix tracking

**Business Value:** Identifies process bottlenecks and quality trends, enabling continuous improvement and velocity optimization.

#### 4. 👥 Team Performance
**Purpose:** Individual and team capacity analysis

**Features:**
- Individual velocity contribution tracking
- Capacity utilization heatmap (identifies burnout risks)
- Estimation accuracy by team member
- Work distribution by role
- Automated bottleneck identification
- Team specialization analysis

**Business Value:** Supports fair work distribution, identifies skill gaps, and prevents team burnout through proactive capacity management.

#### 5. 🔮 Predictive Insights & Risk Scoring
**Purpose:** Forward-looking analytics and risk assessment

**Features:**
- Sprint health score (0-100 composite metric)
- Next sprint completion probability (Monte Carlo simulation)
- Initiative delivery risk assessment
- Capacity planning forecast (3-sprint projection)
- Automated recommendations engine
- Risk factor breakdown

**Business Value:** Provides 2-3 sprint early warning for delivery risks, enabling proactive mitigation and realistic stakeholder expectations.

#### 6. 📈 Strategic Trends & ROI Analysis
**Purpose:** Long-term patterns and business impact

**Features:**
- Velocity stability and learning curves
- Estimation accuracy improvement tracking
- Work composition evolution (Features vs Bugs vs Tech Debt)
- Initiative throughput and success rates
- ROI impact analysis (investment vs business value)
- Quarterly business review summaries

**Business Value:** Connects tactical execution to strategic outcomes, demonstrates ROI of investments, and supports quarterly planning.

---

## 📈 Key Metrics Explained

### Sprint Health Score (0-100)

**Formula:**
```
Health = (Velocity Consistency × 0.30) +
         (Estimation Accuracy × 0.25) +
         (Completion Rate × 0.25) +
         (Blocker Impact × 0.20)
```

**Zones:**
- 80-100 (Green): Excellent - Sprint on track
- 60-79 (Yellow): Monitor - Some concerns
- <60 (Red): At Risk - Intervention needed

**Business Use:** Early warning system for sprint delivery risks. Scores <70 trigger proactive team discussions.

### Initiative Priority Score

**Formula:**
```
Priority = (Impact Score / Effort Score) × Strategic Weight × ROI Multiplier

Strategic Weights:
- Revenue Growth: 1.5×
- Customer Experience: 1.3×
- Cost Reduction: 1.2×
- Technical Excellence: 1.1×
- Process Improvement: 1.0×
```

**Business Use:** Objective ranking for initiative selection. Enables transparent, data-driven portfolio decisions aligned with strategic goals.

### Monte Carlo Completion Probability

**Method:** Runs 1000 simulations of next sprint velocity based on historical distribution

**Output:** "87% probability of completing 42 points"

**Business Use:** Quantifies sprint planning risk. Informs commitment discussions with stakeholders based on statistical confidence.

### Initiative Risk Score (0-1)

**Factors:**
1. **Capacity Risk (35%)** - Remaining work vs available team capacity
2. **Volatility Risk (25%)** - Historical velocity variance
3. **Utilization Risk (25%)** - Current team over/under-utilization
4. **Progress Risk (15%)** - Actual vs expected progress

**Thresholds:**
- <0.3: Low Risk - On track
- 0.3-0.6: Medium Risk - Monitor closely
- >0.6: High Risk - Immediate intervention

**Business Use:** Prioritizes PM attention on at-risk initiatives. Enables proactive scope/resource adjustments.

---

## 🛠️ Technical Architecture

### Stack
- **Python 3.9+** - Core language
- **Streamlit** - Interactive web dashboard
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **NumPy** - Numerical computations
- **SciPy** - Statistical analysis
- **scikit-learn** - Predictive modeling

### Project Structure
```
sprint-portfolio-analytics/
├── app.py                          # Main Streamlit application (6 pages)
├── data/
│   ├── generate_data.py            # Realistic data generation script
│   ├── sprint_data.csv             # Sprint-level metrics (12 sprints)
│   ├── story_data.csv              # Story-level data (355 stories)
│   ├── initiative_data.csv         # Initiative/portfolio data (28 initiatives)
│   └── team_data.csv               # Team member data (8 members)
├── utils/
│   ├── data_processing.py          # Data loading & transformation
│   ├── metrics.py                  # Sprint & portfolio metrics
│   ├── prioritization.py           # Initiative scoring & ranking
│   ├── predictive_models.py        # Risk scoring & forecasting
│   └── visualizations.py           # Reusable Plotly charts
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

### Design Decisions

**Modular Architecture:**
- Separation of concerns: data, business logic, visualization
- Reusable utility functions for maintainability
- Caching for performance optimization

**Data Generation:**
- Realistic patterns (velocity stabilization, estimation improvement)
- Edge cases (holiday capacity reduction, blocker spikes)
- Authentic initiative distribution across priority quadrants

**Performance Optimizations:**
- `@st.cache_data` for data loading (sub-second page loads)
- `@st.cache_resource` for model computations
- Efficient Pandas operations (vectorization)

**Extensibility Points:**
- Easy integration with real data sources (Jira API, CSV export)
- Pluggable metrics framework (add custom KPIs)
- Configurable thresholds and weights

---

## 🚀 Installation & Usage

### Quick Start

```bash
# Clone repository
git clone [repository-url]
cd sprint-portfolio-analytics

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python data/generate_data.py

# Launch dashboard
streamlit run app.py
```

Dashboard will open in your browser at `http://localhost:8501`

### System Requirements
- Python 3.9 or higher
- 4GB RAM minimum
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Using Your Own Data

**Option 1: CSV Import**
Replace generated CSV files in `/data` folder with your own data following the same schema.

**Option 2: API Integration**
Modify `data_processing.py` to connect to Jira, Monday.com, or other PM tools.

Example Jira integration:
```python
from jira import JIRA

jira = JIRA(server='https://your-domain.atlassian.net', basic_auth=('email', 'token'))
issues = jira.search_issues('project=ABC AND sprint=12')
# Transform to DataFrame format
```

---

## 📄 License

This project is created as a portfolio demonstration piece. Feel free to use, modify, and extend for your own portfolio projects.

---
*This dashboard transforms sprint data into strategic intelligence, enabling proactive management and measurable business impact.*
