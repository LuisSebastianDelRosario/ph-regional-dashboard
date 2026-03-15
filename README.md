# 🇵🇭 Philippines Regional Data Dashboard

An interactive data dashboard exploring the correlation between **poverty rate**, **GDP (GRDP)**, and **unemployment rate** across all 17 Philippine regions.

---

## 📊 Features

- Regional breakdown of poverty, GRDP, and unemployment
- Pearson correlation analysis with significance testing
- Interactive scatter plots with OLS trend lines
- Correlation heatmap
- Region filter via sidebar
- CSV export of filtered data

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Dashboard UI |
| Plotly | Interactive charts |
| Pandas | Data wrangling |
| SciPy | Correlation statistics |
| Statsmodels | OLS trendlines |

---

## 🚀 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/ph-regional-dashboard.git
cd ph-regional-dashboard
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Project Structure
```
ph-regional-dashboard/
│
├── data/
│   ├── raw/
│   │   ├── poverty.csv
│   │   ├── gdp.csv
│   │   └── unemployment.csv
│   └── processed/
│
├── src/
│   ├── data_loader.py
│   ├── charts.py
│   └── correlation.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 📌 Data Sources

- **PSA Philippines** — Poverty incidence and unemployment by region (2021)
- **NSCB Regional Accounts** — Gross Regional Domestic Product (2021)

---

## 💡 Key Findings

| Pair | Pearson r | Interpretation |
|---|---|---|
| Poverty vs GRDP | -0.63 | Richer regions tend to have less poverty |
| Poverty vs Unemployment | -0.76 | Informal/underemployment drives poverty more than unemployment |
| GRDP vs Unemployment | +0.80 | Urban hubs (NCR) have high GDP and high formal unemployment |

---

## 👤 Author

Built by Luis Sebastian Del Rosario (March 2026)