# Deployment Guide: Dolly's & Noah's Dashboards

This guide explains how to deploy both versions of the Sprint Analytics Dashboard.

---

## 📋 Current Branch Status

### 1. **dolly-main** branch
- Contact: Dolly Dang (dolly.u.dang@gmail.com)
- Focus: Product Management & Strategy Operations
- Status: ✅ Ready for Dolly's GitHub

### 2. **noah-portfolio-version** branch
- Contact: Noah Gallagher (noah@datadrivenmgmt.com)
- Focus: Data Science & Analytics Engineering
- Status: ✅ Ready for deployment

---

## 🚀 Phase 1: Deploy Dolly's Version

### Step 1: Have Dolly create GitHub repository
1. Dolly creates new repository: `sprint-portfolio-analytics` (or any name)
2. Get the repository URL: `https://github.com/dollydang/sprint-portfolio-analytics.git`

### Step 2: Push to Dolly's repository
```bash
# Switch to Dolly's branch
git checkout dolly-main

# Add Dolly's repository as remote
git remote add dolly https://github.com/dollydang/sprint-portfolio-analytics.git

# Push to Dolly's main branch
git push dolly dolly-main:main
```

### Step 3: Deploy on Dolly's Streamlit Cloud
1. Dolly logs into https://streamlit.io
2. Click "New app"
3. Repository: `dollydang/sprint-portfolio-analytics`
4. Branch: `main`
5. Main file: `app.py`
6. Click "Deploy"

**Dolly's Dashboard URL:** Will be `https://[app-name].streamlit.app`

---

## 🧪 Phase 2: Deploy Noah's Data Science Portfolio

### Option A: Use existing repository (RECOMMENDED)

Your repository already has the `noah-portfolio-version` branch! Just deploy from it:

```bash
# Push Noah's branch to your origin
# (You may need to push from a session-specific branch or manually push later)
git checkout noah-portfolio-version
git push origin noah-portfolio-version
```

### Step 1: Deploy on YOUR Streamlit Cloud
1. Go to https://streamlit.io
2. Click "New app"
3. Repository: `noahgallagher1/sprint-portfolio-analytics`
4. Branch: `noah-portfolio-version`
5. Main file: `app.py`
6. Click "Deploy"

**Noah's Dashboard URL:** Will be `https://[app-name].streamlit.app`

### Option B: Create separate repository

If you want complete separation:

```bash
# Create new repo on GitHub: sprint-analytics-datascience
# Then:
git checkout noah-portfolio-version
git remote add noah-datascience https://github.com/noahgallagher1/sprint-analytics-datascience.git
git push noah-datascience noah-portfolio-version:main
```

---

## 📊 Key Differences Between Versions

### Dolly's Version (PM/Strategy Focus)
- **Subtitle:** "Strategic Project Management & Operations Portfolio Project"
- **Skills:** Portfolio Prioritization, Cross-functional Rollups, Strategic Planning
- **Footer:** Target roles: Sr. PM, Strategy & Operations
- **Focus:** Business value, strategic insights, portfolio management

### Noah's Version (Data Science Focus)
- **Subtitle:** "Data Science & Analytics Engineering Portfolio Project"
- **Skills:** Statistical Modeling, Monte Carlo Simulations, Python Development, ETL
- **Footer:** Target roles: Data Scientist, Analytics Engineer, ML Engineer
- **Focus:** Technical implementation, algorithms, data engineering
- **Bonus:** GitHub button added for code showcase

---

## 🔄 Future Updates

### To update Dolly's version:
```bash
git checkout dolly-main
# Make changes
git add .
git commit -m "Update description"
git push dolly dolly-main:main
```

### To update Noah's version:
```bash
git checkout noah-portfolio-version
# Make changes
git add .
git commit -m "Update description"
git push origin noah-portfolio-version
```

---

## ✅ Verification Checklist

### Dolly's Dashboard:
- [ ] Contact info shows Dolly Dang
- [ ] Email: dolly.u.dang@gmail.com
- [ ] LinkedIn: linkedin.com/in/dollydang
- [ ] Subtitle: "Strategic Project Management..."
- [ ] Footer: "DIRECTOR ALIGNMENT"

### Noah's Dashboard:
- [ ] Contact info shows Noah Gallagher
- [ ] Email: noah@datadrivenmgmt.com
- [ ] LinkedIn + GitHub buttons
- [ ] Subtitle: "Data Science & Analytics Engineering..."
- [ ] Footer: "DATA SCIENCE & ANALYTICS PORTFOLIO"

---

## 📝 Notes

- Both versions use the same underlying data and analytics
- The difference is in the **presentation and emphasis**
- Dolly's version highlights **business/PM value**
- Noah's version highlights **technical/data science skills**
- Both are production-ready and fully functional

---

**Questions?** Contact Noah at noah@datadrivenmgmt.com
