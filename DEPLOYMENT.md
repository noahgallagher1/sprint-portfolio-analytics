# 🚀 Streamlit Cloud Deployment Guide

Deploy your dashboard to the web in 5 minutes - **completely FREE**!

## Overview

Streamlit Cloud provides:
- ✅ **Free hosting** for public repositories
- ✅ **Automatic updates** when you push to GitHub
- ✅ **Custom URL**: `https://your-app-name.streamlit.app`
- ✅ **No server management** required
- ✅ **Built-in authentication** (optional)

---

## Prerequisites

- [x] GitHub account
- [x] This repository pushed to GitHub (already done ✅)
- [x] Streamlit Cloud account (we'll create this)

---

## Step-by-Step Deployment

### Step 1: Create Streamlit Cloud Account

1. Go to **https://streamlit.io/cloud**
2. Click **"Sign up"**
3. Choose **"Continue with GitHub"**
4. Authorize Streamlit to access your GitHub repositories

### Step 2: Deploy Your App

1. Once logged in, click **"New app"**

2. Fill in the deployment form:
   - **Repository**: `noahgallagher1/sprint-portfolio-analytics`
   - **Branch**: `claude/sprint-portfolio-analytics-dashboard-011CUxxLe8kVYFuJ9zkow5cu` (or your main branch)
   - **Main file path**: `app.py`

3. Click **"Advanced settings"** (optional but recommended):
   - **Python version**: `3.9` (or higher)
   - **App URL**: Choose a custom subdomain (e.g., `sprint-analytics-dashboard`)

4. Click **"Deploy!"**

### Step 3: Wait for Deployment

- Initial deployment takes 2-5 minutes
- You'll see a progress screen showing:
  - Installing dependencies
  - Running data generation
  - Starting app

- **Common deployment message**: "Please run: python data/generate_data.py"
  - Don't worry! The data files are already included in your repo

### Step 4: Access Your Dashboard

Once deployed, you'll get a URL like:
```
https://sprint-analytics-dashboard.streamlit.app
```

Share this URL with:
- Interviewers
- Portfolio reviewers
- Potential employers
- Your network on LinkedIn

---

## Troubleshooting Deployment Issues

### Issue 1: "Data files not found"

**Solution**: The CSV files are already in your repo. If they're not showing up:

```bash
# Locally, ensure data files are committed
git add data/*.csv
git commit -m "Add generated data files"
git push
```

### Issue 2: "Module not found" errors

**Solution**: Streamlit Cloud auto-installs from `requirements.txt` (already included ✅)

If you see errors, check that `requirements.txt` has all dependencies:
```
streamlit==1.29.0
pandas==2.1.4
numpy==1.26.2
plotly==5.18.0
scipy==1.11.4
scikit-learn==1.3.2
```

### Issue 3: App loads slowly

**First load**: May take 10-20 seconds (installing packages)
**Subsequent loads**: Should be instant (cached)

**To improve performance**, add this to your app:
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    # ... your data loading code
```
(Already implemented in the app ✅)

### Issue 4: App goes to sleep

**Free tier**: Apps sleep after 7 days of inactivity
**Solution**: Just visit the URL to wake it up (takes 30 seconds)

**To prevent sleep**: Upgrade to Streamlit Cloud Teams (optional)

---

## Post-Deployment Checklist

Once deployed, verify:

- [ ] All 6 pages load correctly
- [ ] Charts render properly
- [ ] Filters and interactions work
- [ ] Mobile view looks good (Streamlit is responsive)
- [ ] Data shows realistic values

**Test each page:**
1. 🎯 Executive Summary
2. 📋 Portfolio Prioritization
3. 🔍 Sprint Deep Dive
4. 👥 Team Performance
5. 🔮 Predictive Insights
6. 📈 Strategic Trends

---

## Customization Options

### Change App Theme

Create `.streamlit/config.toml` in your repo:

```toml
[theme]
primaryColor = "#2E86AB"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Add Authentication (Optional)

For private apps or team access:

1. In Streamlit Cloud settings, click **"Sharing"**
2. Options:
   - **Public**: Anyone can access
   - **Private**: Only invited users
   - **Email domains**: Restrict by email domain

### Custom Domain (Optional)

**Free tier**: `your-app.streamlit.app`
**Teams tier**: Custom domain like `analytics.yourcompany.com`

---

## Updating Your Deployed App

Streamlit Cloud automatically redeploys when you push to GitHub:

```bash
# Make changes locally
nano app.py

# Test locally
streamlit run app.py

# Commit and push
git add .
git commit -m "Update dashboard feature"
git push

# Streamlit Cloud auto-deploys in 1-2 minutes!
```

**To force a redeploy:**
1. Go to Streamlit Cloud dashboard
2. Click on your app
3. Click **"Reboot app"**

---

## Monitoring & Analytics

### Built-in Metrics

Streamlit Cloud provides:
- **Visitor count** (anonymous)
- **Resource usage** (CPU, memory)
- **Error logs** (if app crashes)

Access via: Streamlit Cloud → Your App → **"Analytics"** tab

### View Logs

To debug issues:
1. Go to your app on Streamlit Cloud
2. Click **"Manage app"** (bottom right)
3. View **"Logs"** tab
4. See real-time console output

---

## Sharing Your Dashboard

### For Job Applications

**In your resume/portfolio:**
```
Sprint Analytics Dashboard
🔗 https://sprint-analytics-dashboard.streamlit.app
Built with Python, Streamlit, Plotly | Portfolio management & predictive analytics
```

**In cover letters:**
```
"I built a comprehensive analytics dashboard demonstrating portfolio management
and predictive modeling capabilities. View it live at: [URL]"
```

**On LinkedIn:**
```
🚀 Just deployed a Sprint Performance & Portfolio Analytics Dashboard!

Features:
📊 6 interactive pages with 20+ visualizations
🔮 Monte Carlo simulations for sprint planning
⚡ Initiative prioritization with Impact/Effort matrix
📈 Predictive risk assessment

Built with Python, Streamlit, Plotly
View live: [URL]

#DataAnalytics #ProductManagement #Python #Dashboard
```

### For Interviews

**Include in interview prep email:**
```
Hi [Interviewer],

I'm excited about our conversation on [date]. I've built a portfolio project
that's relevant to the role - a comprehensive sprint analytics dashboard.

You can explore it here: [Streamlit URL]

Key features aligned with the role:
- Portfolio prioritization (Impact/Effort framework)
- Predictive risk assessment
- Data-driven recommendations

Looking forward to discussing!
```

**During interview:**
- Share screen with live URL (no "localhost" hassles!)
- Let interviewer interact with filters
- Show how data drives insights

---

## Alternatives to Streamlit Cloud

If you need more control or features:

### Option 1: Heroku (Free tier)
```bash
# Install Heroku CLI
heroku create sprint-analytics

# Deploy
git push heroku main
```

### Option 2: AWS EC2 (More control)
- Launch EC2 instance
- Install Python & requirements
- Run `streamlit run app.py --server.port 80`
- Configure security groups

### Option 3: Docker + Cloud Run (GCP)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD streamlit run app.py
```

### Option 4: Railway.app (Simple alternative)
- Connect GitHub repo
- Auto-detects Python
- One-click deploy

---

## Cost Comparison

| Platform | Free Tier | Paid Options |
|----------|-----------|--------------|
| **Streamlit Cloud** | ✅ 1 private app<br>✅ Unlimited public | $20/mo for 3 apps |
| **Heroku** | ⚠️ Limited hours | $7/mo per app |
| **AWS EC2** | ✅ 12 months free | $5-20/mo |
| **Railway** | $5 credit/month | $10/mo |
| **Vercel** | ✅ Unlimited | $20/mo teams |

**Recommendation**: Start with Streamlit Cloud (free, easiest, built for this)

---

## Security Best Practices

### For Public Dashboards:

✅ **Use sample data** (already done - no real company data)
✅ **No API keys in code** (use Streamlit secrets)
✅ **No PII** (personally identifiable information)
✅ **Add disclaimer**: "Demo data for portfolio purposes"

### For Private Dashboards:

If using real company data:
1. Set app to **Private** in Streamlit Cloud
2. Use **Streamlit secrets** for API keys:

```python
# In Streamlit Cloud settings, add secrets
api_key = st.secrets["API_KEY"]

# Access in code
jira = JIRA(server=st.secrets["jira"]["url"],
            token=st.secrets["jira"]["token"])
```

3. Enable **authentication**
4. Consider **data encryption**

---

## Performance Optimization

To make your deployed app faster:

### 1. Optimize Data Loading
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour ✅
def load_all_data():
    # ... data loading
```

### 2. Lazy Load Large Components
```python
# Only load when page selected
if page == "Predictive Insights":
    # Load heavy calculations here
```

### 3. Reduce Data Size
```python
# For demo, limit to last 3 months instead of 6
sprints_df = sprints_df.tail(6)  # Instead of all 12
```

### 4. Optimize Images/Charts
```python
# Use static charts for unchanging data
fig = create_chart()
st.plotly_chart(fig, config={'staticPlot': True})
```

---

## FAQ

**Q: Is Streamlit Cloud really free?**
A: Yes! Free tier includes 1 private app and unlimited public apps.

**Q: Can employers see my code?**
A: Only if your GitHub repo is public. Private repos = private app.

**Q: How much traffic can it handle?**
A: Free tier handles ~10-50 concurrent users comfortably.

**Q: Can I monetize my dashboard?**
A: Not directly on Streamlit Cloud, but you can use it for:
- Portfolio/job applications ✅
- Demos to clients ✅
- Internal company tools ✅

**Q: What if I exceed free tier limits?**
A: Upgrade to Teams ($20/mo) for more apps and custom domains.

**Q: Can I use a custom domain?**
A: Teams tier only. Free tier gets `your-app.streamlit.app`

**Q: How do I delete my app?**
A: Streamlit Cloud → App → Settings → Delete app

---

## Next Steps

### Immediate (5 minutes)
1. [ ] Deploy to Streamlit Cloud
2. [ ] Test all pages work
3. [ ] Copy your deployment URL

### Short-term (today)
4. [ ] Add URL to resume/portfolio
5. [ ] Share on LinkedIn
6. [ ] Include in job applications

### Optional Enhancements
7. [ ] Add authentication for private version
8. [ ] Connect to real Jira data (if available)
9. [ ] Create video walkthrough
10. [ ] Write blog post about building it

---

## Support Resources

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-cloud
- **Community Forum**: https://discuss.streamlit.io
- **Status Page**: https://streamlit.statuspage.io
- **Discord**: https://discord.gg/streamlit

---

## Deployment Checklist Summary

**Pre-deployment:**
- [x] Code pushed to GitHub ✅
- [x] requirements.txt present ✅
- [x] Data files included ✅
- [x] README.md complete ✅

**Deployment:**
- [ ] Streamlit Cloud account created
- [ ] App deployed
- [ ] All pages tested
- [ ] URL copied

**Post-deployment:**
- [ ] Added to portfolio/resume
- [ ] Shared with network
- [ ] Included in job applications
- [ ] Prepared demo talking points

---

**Your dashboard is ready to share with the world! 🚀**

Deployment URL will be: `https://[your-chosen-name].streamlit.app`
