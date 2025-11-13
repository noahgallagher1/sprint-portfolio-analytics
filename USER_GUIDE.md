# Sprint Portfolio Analytics Dashboard - User Guide & Job Aid

**Version 1.0** | Created by Noah Gallagher
**Purpose:** A comprehensive guide to understand and navigate the Agile Sprint Performance & Portfolio Analytics Dashboard

---

## Table of Contents
1. [Dashboard Overview](#dashboard-overview)
2. [Getting Started](#getting-started)
3. [Dashboard Layout](#dashboard-layout)
4. [Tab-by-Tab Guide](#tab-by-tab-guide)
5. [Key Metrics Explained](#key-metrics-explained)
6. [How to Interpret the Data](#how-to-interpret-the-data)
7. [Common Use Cases](#common-use-cases)
8. [Troubleshooting](#troubleshooting)

---

## Dashboard Overview

### What is This Dashboard?
This dashboard analyzes **6 months of Agile sprint data** from a software development team. It provides:
- **Real-time performance metrics** for sprint velocity, completion rates, and team capacity
- **Portfolio prioritization tools** using Impact vs. Effort analysis
- **Predictive analytics** for forecasting future sprint performance
- **Risk assessment** for identifying at-risk initiatives

### Who Should Use This Dashboard?
- **Product Managers** - Prioritize features and initiatives based on ROI
- **Scrum Masters** - Monitor sprint health and team performance
- **Engineering Leaders** - Assess capacity utilization and bottlenecks
- **Executives** - Get high-level insights on delivery trends and strategic alignment
- **Data Analysts** - Explore sprint data patterns and predictive models

### Data Overview
The dashboard contains:
- **12 sprints** (6 months of data, 2-week iterations)
- **355+ user stories** across all sprints
- **28 strategic initiatives** (epics/features)
- **Team of 8-10 members** with varying capacities

---

## Getting Started

### Accessing the Dashboard
1. Navigate to the dashboard URL (Streamlit app)
2. Wait for the data to load (should take 2-3 seconds)
3. The dashboard opens to the **Executive Summary** tab by default

### Navigation Basics
- **Tabs at the top** - Click any of the 4 main tabs to switch views
- **Left sidebar** - Contains project overview and contact information (persistent across all tabs)
- **Interactive charts** - Hover over data points to see detailed values
- **Dropdown selectors** - Used in the "Delivery & Performance" tab to analyze specific sprints

### Quick Start Checklist
✅ Familiarize yourself with the 4 main tabs
✅ Review the KPI metrics at the top of the Executive Summary
✅ Explore the Impact/Effort Matrix in Portfolio & Strategy
✅ Select different sprints in Delivery & Performance
✅ Read metric definitions in the About the Data tab

---

## Dashboard Layout

### Left Sidebar (Persistent)
The left sidebar appears on all tabs and contains:

#### 1. Project Overview
- **Purpose** - High-level summary of what the dashboard does
- **Key capabilities** - 4 bullet points highlighting main features

#### 2. Skills Demonstrated
- Portfolio & Roadmap Prioritization
- Analytical Problem Solving & Insights
- Data-Driven Decision Making
- Cross-functional Stakeholder Rollups
- Executive Analytics & Risk Scoring

#### 3. Business Impact
- Strategic Value
- Delivery Confidence
- Portfolio ROI

#### 4. Technical Capabilities
- Python (Pandas, NumPy, SciPy)
- Streamlit (Interactive Dashboards)
- Plotly (Data Visualization)
- Monte Carlo Simulations
- Statistical Risk Modeling

#### 5. Contact Information
- Email: noahgallagher1@gmail.com
- LinkedIn: [Noah Gallagher](https://www.linkedin.com/in/noahgallagher/)
- GitHub: [Repository Link](https://github.com/noahgallagher1/sprint-portfolio-analytics)

### Main Content Area (Changes by Tab)
The right side contains 4 tabs with different content.

---

## Tab-by-Tab Guide

### Tab 1: 📊 Executive Summary

**Purpose:** Get a high-level overview of team performance and strategic recommendations

#### Key Components:

##### 1. Top KPI Row (5 Metrics)
These 5 cards appear at the very top:

| Metric | Example Value | What It Means |
|--------|---------------|---------------|
| **Current Velocity** | 42 | Story points completed in the most recent sprint |
| **Avg Velocity 12M** | 38 | Average story points per sprint over all 12 sprints |
| **Completion Rate** | 85% | Percentage of committed work actually completed in current sprint |
| **Sprint Health** | 78/100 | Composite score combining velocity consistency, completion rate, and accuracy |
| **Total Projects** | 28 (12 Completed) | Total initiatives in the portfolio and how many are done |

**💡 How to Read This:**
- If Current Velocity > Avg Velocity: Team is improving
- Completion Rate above 80% is excellent
- Sprint Health above 75 = Healthy, 60-75 = Monitor, Below 60 = At Risk

##### 2. Chart Row 1 (3 Charts)

**A. Velocity Trend Chart**
- **What it shows:** Line chart of story points delivered per sprint over time
- **How to read it:**
  - Upward trend = Team is accelerating
  - Flat line = Consistent velocity (good for predictability)
  - Downward trend = May indicate capacity issues or scope creep
- **Example:** If Sprint 1 shows 32 points and Sprint 12 shows 45 points, the team improved velocity by ~40%

**B. Portfolio Composition Chart**
- **What it shows:** Bar chart breaking down initiatives by quadrant
  - Quick Wins (High Impact, Low Effort) - Green
  - Major Projects (High Impact, High Effort) - Blue
  - Fill-ins (Low Impact, Low Effort) - Gray
  - Time Sinks (Low Impact, High Effort) - Red
- **How to read it:**
  - More Quick Wins = Better portfolio health
  - Too many Time Sinks = Need to deprioritize
- **Example:** "8 Quick Wins, 5 Major Projects, 3 Fill-ins, 2 Time Sinks"

**C. Team Performance Heatmap**
- **What it shows:** Color-coded grid showing capacity utilization per team member across last 6 sprints
  - Green = 80-100% utilized (optimal)
  - Yellow = 60-80% or 100-120% (monitor)
  - Red = Below 60% or above 120% (concern)
- **How to read it:**
  - Look for patterns: Is one person consistently overloaded?
  - Check for underutilization: Are resources being wasted?
- **Example:** "Sarah shows 115% utilization in Sprint 12 - possible burnout risk"

##### 3. Work Distribution Stacked Area Chart
- **What it shows:** How story types (Features, Bugs, Technical Debt, Spikes) are distributed over time
- **How to read it:**
  - Increasing Feature work = Good (delivering value)
  - Too much Bug work = Quality issues
  - Spikes should be minimal and temporary

##### 4. Strategic Insights & Recommendations (2 columns)

**Left Column (Green boxes - Strengths/Opportunities):**
- Velocity improvement percentage
- Number of Quick Win initiatives available
- Predictability score

**Right Column (Orange/Red boxes - Alerts/Optimizations):**
- High-risk initiatives that need attention
- Time Sink initiatives to deprioritize

**💡 Example Interpretation:**
```
✅ STRENGTH: Team velocity improved 15% over 6 months - momentum building
⚡ OPPORTUNITY: 6 "Quick Win" initiatives ready for immediate delivery
🚨 ALERT: 3 initiatives flagged high-risk - realign scope or extend timeline
```

##### 5. Project Results & Business Value (Yellow Box)
- Summary of the dashboard's technical approach
- Describes Monte Carlo simulations and prioritization methodology

---

### Tab 2: 🎯 Portfolio & Strategy

**Purpose:** Prioritize initiatives and optimize portfolio composition

#### Key Components:

##### 1. Portfolio Prioritization Matrix (Impact vs. Effort)
- **What it shows:** Scatter plot with all 28 initiatives plotted
  - X-axis = Effort Score (0-10, left = low effort, right = high effort)
  - Y-axis = Impact Score (0-10, bottom = low impact, top = high impact)
  - Color = Quadrant (Green = Quick Wins, Blue = Major Projects, etc.)
  - Size of bubble = Total story points

- **How to read it:**
  - **Top-left quadrant (Quick Wins):** High impact, low effort - PRIORITIZE THESE FIRST
  - **Top-right quadrant (Major Projects):** High impact, high effort - Strategic investments
  - **Bottom-left quadrant (Fill-ins):** Low impact, low effort - Use to fill capacity gaps
  - **Bottom-right quadrant (Time Sinks):** Low impact, high effort - AVOID OR DEPRIORITIZE

- **💡 Example:**
  ```
  Initiative: "Mobile App Onboarding Redesign"
  - Impact Score: 9/10
  - Effort Score: 3/10
  - Quadrant: Quick Win
  - Story Points: 21
  - Status: Backlog

  ➡️ ACTION: Prioritize immediately - high value, low cost
  ```

##### 2. Portfolio Composition Bar Chart
- Shows count of initiatives in each quadrant
- **Ideal distribution:** 30-40% Quick Wins, 25-35% Major Projects, 20-30% Fill-ins, 0-10% Time Sinks

##### 3. Top Quick Wins (Left Column)
- Lists top 5 initiatives with best Priority Score
- **Priority Score Formula:** (Impact × 10) / Effort
- **Example:**
  ```
  Initiative: "Email Notification System"
  Impact: 8/10 | Effort: 2/10 | Priority: 40.00
  Status: Backlog | Points: 13

  ➡️ This initiative has a priority score of 40 - extremely high ROI
  ```

##### 4. Time Sinks to Deprioritize (Right Column)
- Lists initiatives with poor ROI
- **Example:**
  ```
  Initiative: "Custom Admin Dashboard"
  Impact: 3/10 | Effort: 9/10 | Priority: 3.33
  Status: Backlog | Points: 55

  ➡️ This initiative requires 55 story points but delivers low impact - consider removing
  ```

##### 5. Strategic Trends & ROI Analysis

**Velocity Stability Chart:**
- Line chart showing velocity over time with 3-sprint rolling average
- Helps assess predictability

**ROI Scatter Plot:**
- Shows completed initiatives only
- X-axis = Effort Score
- Y-axis = Impact Score
- Color = ROI Estimate (High/Medium/Low)
- **How to read it:** Completed initiatives in top-left delivered best ROI

##### 6. Key Metrics Row (4 metrics)
| Metric | Example | Interpretation |
|--------|---------|----------------|
| Velocity Improvement | +15% | Team is getting faster |
| Predictability | 82% | High confidence in forecasts |
| Initiative Success Rate | 43% | Percentage of initiatives completed |
| Total Delivered | 456 pts | Cumulative story points across all sprints |

---

### Tab 3: ⚡ Delivery & Performance

**Purpose:** Deep dive into specific sprints and team performance

#### Key Components:

##### 1. Sprint Selector Dropdown
- **How to use:** Click the dropdown and select any sprint number (1-12)
- All charts below update based on your selection

##### 2. Sprint Overview Metrics (4 cards)
| Metric | Example | What It Means |
|--------|---------|---------------|
| Committed Points | 50 | Story points the team planned to complete |
| Completed Points | 42 | Story points actually finished |
| Completion Rate | 84% | 42/50 = 84% |
| Capacity Utilization | 95% | Team used 95% of available capacity |

**💡 Interpretation:**
- Completion Rate 80-100% = Excellent planning
- Capacity Utilization 85-95% = Optimal (not overloaded, not underutilized)
- Capacity Utilization above 100% = Team overcommitted

##### 3. Sprint Story Status Pie Chart
- Shows breakdown of stories in selected sprint:
  - Completed (Green)
  - In Progress (Yellow)
  - Not Started (Gray)
  - Blocked (Red)
- **Example:** "Sprint 8: 15 Completed, 2 In Progress, 1 Blocked"

##### 4. Cycle Time Box Plot
- **What it shows:** Distribution of days from story start to completion
- **Box plot components:**
  - Box = Middle 50% of stories (25th to 75th percentile)
  - Line inside box = Median cycle time
  - Whiskers = Min and max (excluding outliers)
  - Dots = Outliers (stories that took unusually long)

- **💡 Example:**
  ```
  Median cycle time: 4 days
  75th percentile: 6 days
  Outlier: 12 days (investigate why this story took so long)
  ```

##### 5. Team Performance Bar Chart
- Shows total story points delivered by each team member across ALL sprints
- **How to read it:**
  - Longer bars = Higher contribution
  - Look for imbalances: Is one person carrying the team?
- **Example:** "Sarah: 78 points, John: 65 points, Mike: 52 points"

##### 6. Predictive Insights Section

**Sprint Health Gauge:**
- Speedometer-style gauge showing health score 0-100
- Color zones:
  - Green (80-100): Excellent - Sprint on track
  - Yellow (60-80): Monitor - Some concerns
  - Red (0-60): At Risk - Intervention needed

**Initiative Risk Distribution Pie Chart:**
- Shows breakdown of all active initiatives by risk level:
  - Low Risk (Green): On track
  - Medium Risk (Yellow): Requires monitoring
  - High Risk (Red): Scope/timeline concerns
- **Example:** "5 Low Risk, 8 Medium Risk, 3 High Risk"

##### 7. Velocity Forecast Chart
- Line chart showing:
  - Historical velocity (solid line, past sprints)
  - Forecasted velocity (dashed line, next 3 sprints)
- **How to read it:**
  - Forecast based on historical trends
  - Use for capacity planning
- **💡 Example:** "Based on trends, expect 42-45 points per sprint for next 3 sprints"

---

### Tab 4: 📚 About the Data

**Purpose:** Understand the dataset and metric definitions

#### Key Components:

##### 1. Data Overview (3 cards)
- Total Sprints: 12
- User Stories: 355+
- Initiatives: 28

##### 2. Sprint Timeline & Context
- Table showing all 12 sprints with:
  - Sprint #
  - Committed points
  - Completed points
  - Completion %
  - Velocity
- **How to use:** Quickly scan performance across all sprints

##### 3. Story Type Breakdown (Pie Chart)
- Distribution of work types:
  - Features (new functionality)
  - Bugs (defects)
  - Technical Debt (refactoring, upgrades)
  - Spikes (research, proof-of-concept)

##### 4. Initiative Status (Bar Chart)
- Shows how many initiatives are:
  - Completed
  - Active (in progress)
  - Backlog (not started)
  - Deprioritized (cancelled/paused)

##### 5. Key Terms & Metrics (2 columns)

**Sprint Metrics:**
- **Velocity:** Total story points completed in a sprint
- **Completion Rate:** % of committed points actually completed
- **Sprint Health Score:** Composite metric (0-100) combining velocity consistency, completion rate, and estimation accuracy
- **Cycle Time:** Days from story start to completion

**Team Metrics:**
- **Capacity Utilization:** % of team capacity used
- **Estimation Accuracy:** How close final points are to initial estimates

**Portfolio Metrics:**
- **Impact Score:** Business value rating (0-10)
- **Effort Score:** Complexity & time required (0-10)
- **Priority Score:** Calculated as (Impact × 10) / Effort
- **ROI Estimate:** Expected return on investment (High/Medium/Low)

**Risk Levels:**
- **High Risk:** Initiatives with scope/timeline concerns
- **Medium Risk:** Requires monitoring
- **Low Risk:** On track for delivery

##### 6. How to Use This Dashboard
- Step-by-step navigation guide
- Tips for each tab

---

## Key Metrics Explained

### Sprint Metrics

#### 1. Velocity
**Definition:** Total story points completed in a single sprint

**How it's calculated:**
```
Velocity = Sum of all "Completed" story points in a sprint
```

**Example:**
```
Sprint 12:
- Story A: 8 points (Completed)
- Story B: 5 points (Completed)
- Story C: 13 points (Completed)
- Story D: 3 points (In Progress)

Velocity = 8 + 5 + 13 = 26 points
(Story D not counted because it's not completed)
```

**What "good" looks like:**
- Consistent velocity (±10% variation) = Predictable team
- Increasing velocity over time = Team is improving
- Velocity of 30-50 points is typical for a mid-size team

---

#### 2. Completion Rate
**Definition:** Percentage of committed work that was actually completed

**How it's calculated:**
```
Completion Rate = (Completed Points / Committed Points) × 100
```

**Example:**
```
Sprint 8:
- Committed: 50 points
- Completed: 42 points

Completion Rate = (42 / 50) × 100 = 84%
```

**What "good" looks like:**
- 80-100% = Excellent (good planning, realistic commitments)
- 60-80% = Acceptable (room for improvement)
- Below 60% = Poor (overcommitting or blockers)

---

#### 3. Sprint Health Score
**Definition:** Composite metric (0-100) that combines multiple factors

**How it's calculated:**
```
Components (weighted):
1. Velocity Consistency (30%): Lower variance = higher score
2. Completion Rate (40%): Higher rate = higher score
3. Estimation Accuracy (30%): Closer to estimates = higher score

Sprint Health = Weighted average of all components
```

**Example:**
```
Sprint 10:
- Velocity Consistency: 85/100 (low variance from average)
- Completion Rate: 90/100 (90% completion)
- Estimation Accuracy: 75/100 (final points close to estimates)

Sprint Health = (85×0.3) + (90×0.4) + (75×0.3) = 83.5 ≈ 84/100
```

**What "good" looks like:**
- 80-100 = Excellent (Green): Sprint on track
- 60-80 = Monitor (Yellow): Some concerns
- 0-60 = At Risk (Red): Intervention needed

---

#### 4. Cycle Time
**Definition:** Average number of days from when a story starts to when it's completed

**How it's calculated:**
```
Cycle Time = Completion Date - Start Date

Average Cycle Time = Mean of all completed story cycle times
```

**Example:**
```
Story A: Started June 1, Completed June 5 = 4 days
Story B: Started June 2, Completed June 8 = 6 days
Story C: Started June 3, Completed June 7 = 4 days

Average Cycle Time = (4 + 6 + 4) / 3 = 4.67 days
```

**What "good" looks like:**
- 2-5 days = Excellent (stories moving quickly)
- 5-8 days = Acceptable (within sprint)
- Above 10 days = Concern (may span multiple sprints)

---

### Portfolio Metrics

#### 5. Impact Score
**Definition:** Business value rating from 0-10

**How it's determined:**
- Based on expected revenue impact, user satisfaction, strategic alignment
- Typically assigned by product managers or stakeholders

**Scale:**
- 9-10 = Critical (must-have, high revenue/user impact)
- 7-8 = High (significant value)
- 4-6 = Medium (nice-to-have)
- 0-3 = Low (minimal business value)

**Example:**
```
Initiative: "Payment System Integration"
Impact Score: 10/10
Reasoning: Required for revenue generation, blocks other features
```

---

#### 6. Effort Score
**Definition:** Complexity and time required, rated 0-10

**How it's determined:**
- Based on story points, technical complexity, dependencies
- Higher score = more effort required

**Scale:**
- 9-10 = Very High (3+ months, >50 story points)
- 7-8 = High (1-3 months, 30-50 points)
- 4-6 = Medium (2-4 weeks, 15-30 points)
- 0-3 = Low (<2 weeks, <15 points)

**Example:**
```
Initiative: "Email Notification System"
Effort Score: 2/10
Reasoning: Simple feature, 13 story points, no dependencies
```

---

#### 7. Priority Score
**Definition:** Calculated metric that balances impact against effort, with strategic weights

**How it's calculated:**
```
Priority Score = (Impact Score / Effort Score) × Strategic Weight × ROI Multiplier

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

**Example:**
```
Initiative A:
- Impact: 8/10
- Effort: 2/10
- Strategic Category: Customer Experience (1.3×)
- ROI Estimate: High (1.3×)
Priority Score = (8 / 2) × 1.3 × 1.3 = 4.0 × 1.69 = 6.76

Initiative B:
- Impact: 9/10
- Effort: 9/10
- Strategic Category: Process Improvement (1.0×)
- ROI Estimate: Medium (1.0×)
Priority Score = (9 / 9) × 1.0 × 1.0 = 1.0

➡️ Initiative A has higher priority (better ROI with strategic alignment)
```

**What "good" looks like:**
- Above 30 = Excellent ROI (Quick Wins)
- 10-30 = Good ROI (Major Projects or Fill-ins)
- Below 10 = Poor ROI (Time Sinks)

---

#### 8. Capacity Utilization
**Definition:** Percentage of team capacity actually used

**How it's calculated:**
```
Capacity Utilization = (Completed Points / Team Capacity) × 100
```

**Example:**
```
Sprint 11:
- Team Capacity: 45 points (total available)
- Completed Points: 42 points

Capacity Utilization = (42 / 45) × 100 = 93%
```

**What "good" looks like:**
- 85-95% = Optimal (not overloaded, not wasteful)
- 70-85% = Underutilized (capacity available)
- 95-110% = Slightly over (acceptable occasionally)
- Above 110% = Overloaded (burnout risk)

---

## How to Interpret the Data

### Scenario 1: Identifying Performance Trends

**Question:** Is the team's performance improving, declining, or stable?

**Where to look:**
1. Go to **Executive Summary** tab
2. Look at **Velocity Trend Chart**
3. Check the **Velocity Improvement** metric in Portfolio & Strategy tab

**How to interpret:**

**Example A - Improving Team:**
```
Sprint 1-4 average: 32 points
Sprint 9-12 average: 44 points
Velocity Improvement: +37.5%

Trend line: Upward slope
```
**➡️ Interpretation:** Team is accelerating. Possible reasons: better collaboration, reduced technical debt, improved estimation, or increased capacity.

**Example B - Declining Team:**
```
Sprint 1-4 average: 45 points
Sprint 9-12 average: 35 points
Velocity Improvement: -22%

Trend line: Downward slope
```
**➡️ Interpretation:** Team is slowing down. Investigate: capacity changes, increased technical debt, process issues, or scope creep.

**Example C - Stable Team:**
```
All sprints: 38-42 points
Velocity Improvement: +5%

Trend line: Relatively flat
```
**➡️ Interpretation:** Consistent performance. Good for forecasting, but limited growth.

---

### Scenario 2: Prioritizing the Product Backlog

**Question:** Which initiatives should we work on first?

**Where to look:**
1. Go to **Portfolio & Strategy** tab
2. Review **Impact/Effort Matrix**
3. Check **Top Quick Wins** section

**How to interpret:**

**Step 1: Identify Quick Wins**
```
Look for initiatives in the top-left quadrant:
- High Impact (7-10)
- Low Effort (0-4)
- Status: Backlog

Example:
"Mobile Onboarding Redesign"
Impact: 9/10 | Effort: 3/10 | Priority: 30.00
Status: Backlog | Points: 21
```
**➡️ Action:** Prioritize immediately - delivers high value with minimal investment.

**Step 2: Plan Major Projects**
```
Look for initiatives in the top-right quadrant:
- High Impact (7-10)
- High Effort (7-10)

Example:
"Microservices Migration"
Impact: 10/10 | Effort: 10/10 | Priority: 10.00
Status: Active | Points: 89
```
**➡️ Action:** Important but resource-intensive. Break into smaller phases. Allocate dedicated team capacity.

**Step 3: Deprioritize Time Sinks**
```
Look for initiatives in the bottom-right quadrant:
- Low Impact (0-4)
- High Effort (7-10)

Example:
"Custom Admin Dashboard"
Impact: 3/10 | Effort: 9/10 | Priority: 3.33
Status: Backlog | Points: 55
```
**➡️ Action:** Remove from roadmap or replace with higher-ROI alternatives.

**Recommended Portfolio Mix:**
- 40% capacity: Quick Wins (fast value delivery)
- 35% capacity: Major Projects (strategic investments)
- 20% capacity: Fill-ins (technical debt, small improvements)
- 5% capacity: Time Sinks (only if business-critical)

---

### Scenario 3: Assessing Sprint Health

**Question:** Is the current sprint on track?

**Where to look:**
1. Go to **Delivery & Performance** tab
2. Select the current sprint (Sprint 12)
3. Review **Sprint Health Gauge**
4. Check **Completion Rate** and **Capacity Utilization**

**How to interpret:**

**Example A - Healthy Sprint:**
```
Sprint Health Score: 85/100 (Green)
Completion Rate: 92%
Capacity Utilization: 88%
Blocked Stories: 0

Gauge color: Green
Message: "Excellent - Sprint on track"
```
**➡️ Interpretation:** Sprint is executing well. No intervention needed. Team is delivering on commitments.

**Example B - At-Risk Sprint:**
```
Sprint Health Score: 54/100 (Red)
Completion Rate: 58%
Capacity Utilization: 125%
Blocked Stories: 3

Gauge color: Red
Message: "At Risk - Intervention needed"
```
**➡️ Interpretation:** Major issues. Actions needed:
- Investigate blocked stories (remove blockers or descope)
- Team is overcommitted (reduce scope for this sprint)
- Review capacity allocation (are resources overscheduled?)

**Example C - Monitor Sprint:**
```
Sprint Health Score: 72/100 (Yellow)
Completion Rate: 78%
Capacity Utilization: 102%
Blocked Stories: 1

Gauge color: Yellow
Message: "Monitor - Some concerns"
```
**➡️ Interpretation:** Minor concerns. Actions:
- Monitor daily: Is completion rate improving?
- Address the 1 blocked story
- Slightly overcommitted but manageable

---

### Scenario 4: Forecasting Future Capacity

**Question:** How many story points can we commit to in the next 3 sprints?

**Where to look:**
1. Go to **Delivery & Performance** tab
2. Review **Velocity Forecast Chart**
3. Check **Avg Velocity 12M** in Executive Summary

**How to interpret:**

**Example:**
```
Historical velocity (last 6 sprints): 38, 42, 40, 45, 43, 47
Average: 42.5 points

Forecast (next 3 sprints):
Sprint 13: 44 points (predicted)
Sprint 14: 45 points (predicted)
Sprint 15: 46 points (predicted)

Standard deviation: ±5 points
```

**➡️ Interpretation:**
- **Conservative estimate:** Use lower bound (44 - 5 = 39 points per sprint)
- **Realistic estimate:** Use predicted value (44-46 points per sprint)
- **Aggressive estimate:** Use upper bound (46 + 5 = 51 points per sprint)

**Capacity Planning:**
```
If you have 100 story points of work planned:
- Conservative: 100 / 39 = 2.6 sprints ≈ 3 sprints
- Realistic: 100 / 45 = 2.2 sprints ≈ 2-3 sprints
- Aggressive: 100 / 51 = 2.0 sprints ≈ 2 sprints

➡️ Commit to: 2-3 sprints (with medium confidence)
```

---

### Scenario 5: Identifying Team Bottlenecks

**Question:** Are there team members overloaded or underutilized?

**Where to look:**
1. Go to **Executive Summary** tab
2. Review **Team Performance Heatmap**
3. Check **Team Performance Bar Chart** in Delivery & Performance tab

**How to interpret:**

**Team Performance Heatmap Example:**
```
         Sprint 7  Sprint 8  Sprint 9  Sprint 10  Sprint 11  Sprint 12
Sarah      95%      110%      118%      105%       112%       115%  (🔴 Red)
John       88%       92%       85%       90%        88%        91%  (🟢 Green)
Mike       65%       68%       72%       70%        66%        69%  (🟡 Yellow)
```

**➡️ Interpretation:**

**Sarah (Overloaded):**
- Consistently above 100% utilization (red cells)
- Burnout risk
- **Actions:**
  - Redistribute work to other team members
  - Reduce commitments for Sarah
  - Check if Sarah is blocking others

**John (Optimal):**
- Consistently 85-95% utilization (green cells)
- Healthy workload
- **Actions:** Maintain current allocation

**Mike (Underutilized):**
- Consistently below 80% utilization (yellow cells)
- Capacity available
- **Actions:**
  - Increase Mike's workload
  - Check if Mike has skills gaps (training opportunity)
  - Ensure Mike isn't blocked by dependencies

**Team Performance Bar Chart Example:**
```
Total Points Delivered (All Sprints):
Sarah: 95 points
John: 78 points
Emily: 72 points
Mike: 54 points
```

**➡️ Interpretation:**
- Sarah is carrying the team (potential single point of failure)
- Mike's lower contribution aligns with underutilization in heatmap
- Consider redistributing work for better balance

---

### Scenario 6: Evaluating Initiative Risk

**Question:** Which initiatives are at risk of missing deadlines?

**Where to look:**
1. Go to **Delivery & Performance** tab
2. Review **Initiative Risk Distribution** pie chart
3. Check **Strategic Insights** in Executive Summary (red alert boxes)

**How to interpret:**

**Risk Distribution Example:**
```
Total Active Initiatives: 16

Low Risk: 5 initiatives (31%)
Medium Risk: 8 initiatives (50%)
High Risk: 3 initiatives (19%)
```

**High Risk Initiative Example:**
```
Initiative: "API Integration Platform"
Risk Level: High
Reasons:
- Scope increased by 30% since start
- Currently 60% over timeline
- Velocity below historical average

Alert: "🚨 ALERT: 3 initiatives flagged high-risk - realign scope or extend timeline"
```

**➡️ Actions for High-Risk Initiatives:**
1. **Descope:** Remove non-critical features to meet deadline
2. **Extend Timeline:** Negotiate deadline extension with stakeholders
3. **Add Capacity:** Allocate additional team members (if available)
4. **Increase Prioritization:** Move to front of backlog, delay other work

**Medium Risk Initiative Example:**
```
Initiative: "User Dashboard Redesign"
Risk Level: Medium
Reasons:
- On schedule but minimal buffer
- 1 dependency on external team
```

**➡️ Actions for Medium-Risk Initiatives:**
- Monitor closely
- Prepare contingency plans
- Communicate with dependency teams

---

## Common Use Cases

### Use Case 1: Executive Stakeholder Update

**Scenario:** You need to present sprint performance to executives in a quarterly review.

**Dashboard Path:**
1. Start at **Executive Summary** tab
2. Note the 5 KPI metrics at the top
3. Show **Velocity Trend** to demonstrate improvement
4. Highlight **Strategic Insights** (green strengths, red alerts)
5. Show **Project Results & Business Value** (yellow box)

**Talking Points:**
```
"Over the past 6 months:
- Our team velocity improved by 15%, from an average of 38 to 44 points per sprint
- We maintain an 85% completion rate, indicating strong planning discipline
- Sprint health score is 78/100, well within the healthy range
- We've completed 12 of 28 strategic initiatives, with 6 Quick Wins ready for immediate delivery
- However, we've identified 3 high-risk initiatives that require scope realignment"
```

**Follow-up:** Switch to **Portfolio & Strategy** to show ROI analysis.

---

### Use Case 2: Sprint Planning Meeting

**Scenario:** Planning the next sprint and deciding how many story points to commit.

**Dashboard Path:**
1. Go to **Delivery & Performance** tab
2. Select the most recent completed sprint
3. Review **Velocity** and **Completion Rate**
4. Check **Velocity Forecast Chart**
5. Review **Team Performance Heatmap** for capacity constraints

**Decision Process:**
```
Step 1: Check historical velocity
- Last sprint: 42 points
- 3-sprint average: 43 points

Step 2: Check forecast
- Next sprint prediction: 44 points ± 5

Step 3: Check team capacity
- Sarah: 115% utilized (overloaded) - reduce allocation
- Mike: 69% utilized (underutilized) - increase allocation
- Adjusted capacity: ~40 points (accounting for Sarah's reduction)

Step 4: Commitment
➡️ Commit to 40 points (conservative, accounts for team constraints)
```

---

### Use Case 3: Product Roadmap Prioritization

**Scenario:** Deciding which features to include in the next quarter's roadmap.

**Dashboard Path:**
1. Go to **Portfolio & Strategy** tab
2. Review **Impact/Effort Matrix**
3. Identify initiatives in **Top Quick Wins** section
4. Check **Time Sinks to Deprioritize**
5. Review **ROI Scatter Plot** for completed initiatives

**Prioritization Framework:**
```
Quarter capacity: 3 months = 6 sprints × 42 points avg = 252 points

Allocation:
1. Quick Wins (40% = 100 points):
   - Mobile Onboarding Redesign (21 pts, Impact 9/10)
   - Email Notification System (13 pts, Impact 8/10)
   - Search Filter Enhancement (18 pts, Impact 8/10)
   - Profile Settings Update (15 pts, Impact 7/10)
   - Social Media Sharing (12 pts, Impact 7/10)
   Total: 79 points

2. Major Projects (35% = 88 points):
   - API Integration Platform (89 pts, Impact 10/10)
   Total: 89 points (slightly over, acceptable)

3. Fill-ins & Technical Debt (20% = 50 points):
   - Database Optimization (25 pts)
   - Test Coverage Improvement (22 pts)
   Total: 47 points

4. Reserve/Buffer (5% = 13 points)

➡️ Total Planned: 215 points (85% of capacity - realistic)
```

**Deprioritized (Time Sinks):**
- Custom Admin Dashboard (55 pts, Impact 3/10, Effort 9/10)
- Legacy Report Migration (34 pts, Impact 2/10, Effort 7/10)

---

### Use Case 4: Retrospective Analysis

**Scenario:** Conducting a sprint retrospective to identify what went well and what needs improvement.

**Dashboard Path:**
1. Go to **Delivery & Performance** tab
2. Select the sprint you're retrospecting
3. Review **Sprint Overview Metrics**
4. Check **Story Status Pie Chart**
5. Analyze **Cycle Time Box Plot**
6. Review **Sprint Health Gauge**

**Retrospective Template:**
```
Sprint 11 Retrospective:

✅ What Went Well:
- Completion Rate: 88% (above 80% target)
- Capacity Utilization: 91% (optimal range)
- No blocked stories
- Median cycle time: 4 days (efficient)

⚠️ What Needs Improvement:
- Sprint Health: 72/100 (yellow, down from 78 last sprint)
- 2 stories had cycle times over 10 days (outliers)
- John was at 115% utilization (overloaded)

🎯 Action Items for Next Sprint:
1. Investigate the 2 outlier stories - what caused delays?
2. Reduce John's allocation to 85-95% range
3. Improve estimation for large stories (break down into smaller tasks)
4. Target Sprint Health of 80+ by improving velocity consistency
```

---

### Use Case 5: Capacity Planning for New Initiative

**Scenario:** A stakeholder wants to know if you can deliver a new 50-point initiative in the next 2 sprints.

**Dashboard Path:**
1. Go to **Executive Summary** tab - check **Avg Velocity 12M**
2. Go to **Delivery & Performance** tab - check **Velocity Forecast**
3. Review **Team Performance Heatmap** for capacity constraints
4. Check **Initiative Risk Distribution** for current workload

**Analysis:**
```
Current State:
- Average velocity: 42 points/sprint
- Forecast for next 2 sprints: 44 + 45 = 89 points total
- Current active initiatives: 16 (8 are medium/high risk)
- Team utilization: 92% on average

New Initiative Request:
- Effort: 50 points
- Timeline: 2 sprints

Calculation:
Option 1 - Dedicated Capacity:
- Allocate 50 points across 2 sprints (25 points/sprint)
- Remaining capacity: (89 - 50) = 39 points for other work
- Feasibility: ✅ Yes, but reduces capacity for existing initiatives

Option 2 - Parallel Work:
- Continue current work (89 points) + new initiative (50 points) = 139 points
- Team capacity: 89 points
- Feasibility: ❌ No, would require 156% utilization (overload)

➡️ Recommendation:
"We can deliver this initiative in 2 sprints, but we'll need to deprioritize
or defer ~50 points of currently planned work. Based on our Time Sinks analysis,
I recommend descoping the 'Custom Admin Dashboard' (55 points, low impact) to
make room for this higher-priority request."
```

---

## Troubleshooting

### Issue 1: Dashboard Won't Load

**Symptoms:**
- Blank screen
- Error message: "Error loading data"

**Solutions:**
1. **Check if data exists:**
   - Navigate to `data/` folder
   - Ensure these files exist:
     - `sprints.csv`
     - `stories.csv`
     - `initiatives.csv`
     - `team.csv`

2. **Regenerate data:**
   ```bash
   python data/generate_data.py
   ```

3. **Restart the dashboard:**
   ```bash
   streamlit run app.py
   ```

---

### Issue 2: Charts Not Displaying

**Symptoms:**
- Empty chart areas
- Error: "No data available"

**Solutions:**
1. **Check data completeness:**
   - Open `data/sprints.csv` in Excel or text editor
   - Verify data has multiple rows (should have 12 sprints)

2. **Clear Streamlit cache:**
   - In the dashboard, press `C` key
   - Select "Clear cache"
   - Refresh the page

3. **Check browser console:**
   - Press F12 (developer tools)
   - Look for JavaScript errors
   - Try a different browser

---

### Issue 3: Metrics Show Unexpected Values

**Symptoms:**
- Velocity is 0
- Completion rate is 100% for all sprints
- Health score is always the same

**Solutions:**
1. **Verify data quality:**
   - Open `data/stories.csv`
   - Check that `status` column has variety (Completed, In Progress, etc.)
   - Check that `final_story_points` has numeric values

2. **Regenerate with different seed:**
   ```bash
   python data/generate_data.py
   ```

3. **Check for data corruption:**
   - Look for null values or malformed entries
   - Ensure CSV format is correct (comma-delimited, proper headers)

---

### Issue 4: Slow Performance

**Symptoms:**
- Dashboard takes >10 seconds to load
- Tab switching is slow
- Charts lag when hovering

**Solutions:**
1. **Reduce data size (if using custom data):**
   - Limit to most recent 6-12 sprints
   - Remove unnecessary columns

2. **Enable caching:**
   - Caching is already enabled via `@st.cache_data`
   - Ensure you're not clearing cache frequently

3. **Use a faster browser:**
   - Chrome/Edge perform better than Firefox for Plotly charts
   - Close other browser tabs to free memory

4. **Check system resources:**
   - Dashboard requires ~200MB RAM
   - Ensure Python is not throttled

---

### Issue 5: Sprint Selector Doesn't Update Charts

**Symptoms:**
- Change sprint number in dropdown
- Charts don't refresh with new sprint data

**Solutions:**
1. **Wait for processing:**
   - Give it 2-3 seconds after selecting
   - Look for "Running..." indicator in top-right

2. **Force refresh:**
   - Press `R` key to rerun the app
   - Or click the hamburger menu → "Rerun"

3. **Check browser console:**
   - May be a JavaScript error preventing updates

---

### Issue 6: Contact Links Don't Work

**Symptoms:**
- Clicking email/LinkedIn/GitHub buttons does nothing
- Links go to wrong URL

**Solutions:**
1. **Check popup blockers:**
   - Browser may be blocking new tabs
   - Allow popups for the dashboard URL

2. **Copy link manually:**
   - Right-click button → "Copy link address"
   - Paste in new browser tab

3. **Verify URLs in code:**
   - Email: noahgallagher1@gmail.com
   - LinkedIn: https://www.linkedin.com/in/noahgallagher/
   - GitHub: https://github.com/noahgallagher1/sprint-portfolio-analytics

---

## Appendix: Data Schema Reference

### Sprints Table (`data/sprints.csv`)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| sprint_number | Integer | Unique sprint ID (1-12) | 8 |
| committed_points | Integer | Story points committed at sprint start | 50 |
| completed_points | Integer | Story points completed by sprint end | 42 |
| completion_rate | Float | Completed / Committed | 0.84 |
| velocity | Integer | Total completed points | 42 |
| team_capacity | Integer | Total team capacity in points | 45 |
| velocity_rolling_avg | Float | 3-sprint rolling average | 40.5 |

### Stories Table (`data/stories.csv`)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| story_id | String | Unique story identifier | STORY-1234 |
| sprint_number | Integer | Sprint this story belongs to | 8 |
| story_type | String | Feature, Bug, Technical Debt, Spike | Feature |
| status | String | Completed, In Progress, Not Started, Blocked | Completed |
| initial_story_points | Integer | Original estimate | 8 |
| final_story_points | Integer | Actual points (may differ due to rescoping) | 8 |
| assignee_id | String | Team member ID | TM-001 |
| cycle_time_days | Float | Days from start to completion | 4.5 |

### Initiatives Table (`data/initiatives.csv`)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| initiative_id | String | Unique initiative identifier | INIT-001 |
| name | String | Initiative name | Email Notification System |
| status | String | Completed, Active, Backlog, Deprioritized | Backlog |
| impact_score | Integer | Business value (0-10) | 8 |
| effort_score | Integer | Complexity/time (0-10) | 2 |
| total_story_points | Integer | Sum of all story points | 13 |
| priority_score | Float | (Impact × 10) / Effort | 40.0 |
| quadrant | String | Quick Wins, Major Projects, Fill-ins, Time Sinks | Quick Wins |
| roi_estimate | String | High, Medium, Low | High |

### Team Table (`data/team.csv`)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| member_id | String | Unique team member ID | TM-001 |
| name | String | Team member name | Sarah Johnson |
| role | String | Engineer, Designer, QA, etc. | Senior Engineer |
| avg_capacity_per_sprint | Integer | Typical capacity in points | 8 |

---

## Quick Reference Card

**Top 5 KPIs to Monitor:**
1. ✅ **Current Velocity** - Is it above or below average?
2. ✅ **Sprint Health Score** - Is it in the green zone (80+)?
3. ✅ **Completion Rate** - Is it above 80%?
4. ✅ **Capacity Utilization** - Is it in the 85-95% range?
5. ✅ **Quick Wins Count** - How many high-ROI initiatives are ready?

**Tab Navigation Shortcuts:**
- **Executive Summary** - Overall health, trends, recommendations
- **Portfolio & Strategy** - Prioritization, ROI analysis
- **Delivery & Performance** - Sprint deep-dive, forecasts
- **About the Data** - Definitions, data overview

**Color Coding:**
- 🟢 **Green** - Good/Healthy (Quick Wins, Low Risk, High Health)
- 🟡 **Yellow** - Monitor (Medium Risk, Moderate Health)
- 🔴 **Red** - Alert (Time Sinks, High Risk, Poor Health)
- 🔵 **Blue** - Strategic (Major Projects, Important but high effort)
- ⚪ **Gray** - Neutral (Fill-ins, Low priority)

**Key Formulas:**
```
Velocity = Sum of completed story points
Completion Rate = (Completed / Committed) × 100
Priority Score = (Impact × 10) / Effort
Capacity Utilization = (Completed / Capacity) × 100
```

---

## Additional Resources

### Learn More About Agile Metrics
- [Scrum Guide](https://scrumguides.org/) - Official Scrum framework
- [Agile Metrics](https://www.atlassian.com/agile/project-management/metrics) - Atlassian's guide
- [Forecasting with Monte Carlo](https://www.mountaingoatsoftware.com/blog/monte-carlo-simulations-for-agile-project-forecasting) - Advanced techniques

### Contact & Support
- **Email:** noahgallagher1@gmail.com
- **LinkedIn:** [Noah Gallagher](https://www.linkedin.com/in/noahgallagher/)
- **GitHub:** [Repository](https://github.com/noahgallagher1/sprint-portfolio-analytics)

### Dashboard Version History
- **v1.0** - Initial release with 4 tabs, portfolio prioritization, predictive analytics

---

**End of User Guide**

*Last Updated: 2024*
*Created by Noah Gallagher for Data Science & Analytics Portfolio*
