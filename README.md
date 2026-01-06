# Week 2: Transport Affordability Burden Analysis (South Africa)

## 📋 Overview
This project is **Week 2 of a 90-Day Data Analytics Execution Plan**. It builds directly on **Week 1: Transport Expenditure Analysis**, extending the analysis from household spending to **labour market affordability**.

**Core Question:** What percentage of a worker's income is consumed by transport costs in South Africa?

---

## 🎯 Core Finding
**Transport sector workers spend 6.65% of their monthly salary on transport costs** (R2,223 out of R33,443 in average monthly earnings).

## 🔍 The Deeper Insight
The analysis reveals a **regressive burden** where lower-income sectors bear a disproportionately higher cost:
- **Trade sector:** 11.7% burden
- **Mining sector:** 4.0% burden
- **Trade workers experience nearly 3x the burden** of mining workers

---

## 📊 Data Sources
- **Quarterly Employment Survey (QES), Q3 2025** – Statistics South Africa  
  - Transport sector employment: 958,000 workers
  - Total gross earnings for the transport sector

- **Household Expenditure Survey (HES)** – Statistics South Africa  
  - Provincial transport expenditure (from Week 1 project)
  - National average: R21,930 annual per household

---

## 🔧 Methodology & Data Pipeline

### 1. Employment Data Processing (`week2_analysis.py`)
- Loaded raw QES employment Excel tables
- Programmatically detected header rows
- Cleaned and standardized: Year, Quarter, Number of employees
- Filtered to latest period: **2025 Q1 (March)**

### 2. Earnings Data Processing
- Applied same cleaning logic to QES gross earnings tables
- Verified earnings scale and converted values appropriately

### 3. Aggregation & Calculation
- Aggregated employment and earnings across all transport subsectors
- Calculated **average monthly earnings**:
  Average Monthly Earnings = (Total Gross Earnings × 1,000) ÷ Number of Employees ÷ 3

*Note: Division by 3 converts quarterly to monthly earnings*

### 4. Affordability Burden Metric
- Imported national average monthly transport cost from Week 1: `R21,930 ÷ 12 = R2,223.21`
- Calculated burden percentage:
  Transport Burden % = (Monthly Transport Cost ÷ Average Monthly Earnings) × 100


---

## 📈 Deliverables & Outputs
The project produces multiple datasets for Power BI visualization:

| File | Purpose |
|------|---------|
| `week2_transport_affordability_powerbi.csv` | Core affordability calculation |
| `week2_enhanced_powerbi.csv` | Enhanced with other expenses breakdown |
| `week2_sector_comparison.csv` | Sector inequality analysis |
| `week2_time_trend.csv` | Quarterly trend data |

---

## 🛠️ Tools & Technologies
- **Python** (Pandas) for data processing
- **Excel** for initial data exploration
- **Power BI** for interactive visualization
- **GitHub** for version control and documentation

---

## 📁 Project Structure:
Week2_Transport_Affordability/

│

├── analysis/

│ └── week2_transport_affordability.py # Main data pipeline

│

├──Asserts (Screenshots)

│ └── 1.png

│ └── 2.png

│

├── data_raw/ # Original Stats SA files

│ ├── QES_Tables2025Q3_Employment.xlsx

│ ├── QES_Tables2025Q3_Gross_Earnings.xlsx

│ └── South Africa Transport Analysis - Week 1 Project.xlsx

│

├── outputs/ # Processed data for visualization

│ ├── week2_transport_affordability_powerbi.csv

│ ├── week2_enhanced_powerbi.csv

│ ├── week2_sector_comparison.csv

│ └── week2_time_trend.csv

│

├── Powerbi/

│ ├── PowerBI_Dashboard

└── README.md # This documentation


---

## 🔗 Connection to Week 1
While **Week 1** answered *"What are the transport patterns?"* (descriptive analysis), **Week 2** answers *"What is the economic impact?"* (diagnostic analysis). This progression shows how data analysis can move from observation to insight.

**Week 1 → Week 2 Transition:**
- **From:** "Transport costs R21,930 per household annually"
- **To:** "This represents 6.65% of a transport worker's salary"

---

## 🚀 Next Steps (Week 3 Potential)
- **Cross-sector comparison** using full QES dataset
- **Provincial breakdown** of burden (using actual provincial costs)
- **Time series analysis** to track burden trends
- **Inflation adjustment** for real wage comparisons

---

## 📝 Reflection
This project successfully bridges labour market data with household expenditure data to create a meaningful affordability metric. The Python pipeline demonstrates robust data extraction and cleaning techniques that can be replicated for other sectors or time periods.

*Part of a 90-day data analysis challenge | Week completed: 20-27 December 2025*
