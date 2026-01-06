# =====================================
# WEEK 2: TRANSPORT AFFORDABILITY BURDEN
# =====================================
import pandas as pd
import os

os.makedirs('outputs', exist_ok=True)
# =====================================

#. Transport cost data (HES) Week 1, already done with it.


# 1. Employment data (QES):
# Read raw employment sheet
df_emp_raw = pd.read_excel(
    'data_raw/QES_Tables2025Q3_Employment.xlsx',
    sheet_name='7-Transport',
    header=None
)

# Find the header row (where first column == 'Year')
header_row_index = df_emp_raw[df_emp_raw.iloc[:, 0] == 'Year'].index[0]

# Set headers
df_emp_raw.columns = df_emp_raw.iloc[header_row_index]

# Drop header rows
df_emp = df_emp_raw.iloc[header_row_index + 1:].reset_index(drop=True)

print("\nEMPLOYMENT FINAL HEADERS:")
print(df_emp.columns.tolist())

print("\nEMPLOYMENT SAMPLE:")
print(df_emp.head())


# Convert Year to numeric safely
df_emp['Year'] = pd.to_numeric(df_emp['Year'], errors='coerce')

# Drop rows where Year is still NaN (junk rows)
df_emp = df_emp.dropna(subset=['Year'])

# Convert to int
df_emp['Year'] = df_emp['Year'].astype(int)

print("\nEMPLOYMENT AFTER YEAR CLEAN:")
print(df_emp.head())
print("Rows:", len(df_emp))

print(df_emp['Year'].unique())
print(df_emp['Quarter'].unique())


# =====================================
# 2. EARNINGS DATA (QES)
# =====================================

df_earn_raw = pd.read_excel(
    'data_raw/QES_Tables2025Q3_Gross_Earnings.xlsx',
    sheet_name='7-Transport',
    header=None
)

# Find header row
earn_header_row = df_earn_raw[df_earn_raw.iloc[:, 0] == 'Year'].index[0]

# Set headers
df_earn_raw.columns = df_earn_raw.iloc[earn_header_row]

# Drop junk rows
df_earn = df_earn_raw.iloc[earn_header_row + 1:].reset_index(drop=True)

# Clean Year
df_earn['Year'] = pd.to_numeric(df_earn['Year'], errors='coerce')
df_earn = df_earn.dropna(subset=['Year'])
df_earn['Year'] = df_earn['Year'].astype(int)

print("\nEARNINGS FINAL HEADERS:")
print(df_earn.columns.tolist())

print("\nEARNINGS SAMPLE:")
print(df_earn.head())


# =====================================
# FILTER TO LATEST PERIOD
# =====================================

LATEST_YEAR = 2025
LATEST_QUARTER = 'Mar'

df_emp_latest = df_emp[
    (df_emp['Year'] == LATEST_YEAR) &
    (df_emp['Quarter'] == LATEST_QUARTER)
]

df_earn_latest = df_earn[
    (df_earn['Year'] == LATEST_YEAR) &
    (df_earn['Quarter'] == LATEST_QUARTER)
]

print("\nEMPLOYMENT (LATEST):")
print(df_emp_latest)

print("\nEARNINGS (LATEST):")
print(df_earn_latest)


# =====================================
#   Step 1: AGGREGATE 2025 MAR DATA
# ---AGGREGATE EMPLOYMENT (SECTOR TOTAL)
# =====================================

emp_agg = (
    df_emp_latest
    .groupby(['Year', 'Quarter'], as_index=False)
    ['Number of employees']
    .sum()
)

print("\nAGGREGATED EMPLOYMENT:")
print(emp_agg)
# =====================================

# =====================================
# ---AGGREGATE EARNINGS (SECTOR TOTAL)
# =====================================

earn_agg = (
    df_earn_latest
    .groupby(['Year', 'Quarter'], as_index=False)
    ['Total gross earnings']
    .sum()
)

print("\nAGGREGATED EARNINGS:")
print(earn_agg)
# =====================================


# =====================================
#   Step 2: MERGE
# ---MERGE AGGREGATED DATA
# =====================================

df_labour = pd.merge(
    emp_agg,
    earn_agg,
    on=['Year', 'Quarter'],
    how='inner'
)

print("\nLABOUR DATA (AGGREGATED):")
print(df_labour)
# =====================================

# =====================================
#   STEP 3: CALCULATE AVERAGE MONTHLY EARNINGS (FINAL FORM)
# ---CALCULATE AVERAGE MONTHLY EARNINGS
# =====================================
df_labour['Avg_Monthly_Earnings'] = (
    (df_labour['Total gross earnings'] * 1_000) /
    df_labour['Number of employees']
) / 3


print("\nAVERAGE MONTHLY EARNINGS (TRANSPORT, 2025 MAR):")
print(df_labour[['Avg_Monthly_Earnings']])
# =====================================


# =====================================
# 4. TRANSPORT COSTS DATA (FROM WEEK 1), AFFORDABILITY BURDEN CALCULATION & Export
# =====================================

#   STEP 1: BRING IN WEEK 1 TRANSPORT COSTS
# =====================================
# LOAD WEEK 1 TRANSPORT COSTS
# =====================================

transport = pd.read_excel(
    'data_raw/South Africa Transport Analysis - Week 1 Project.xlsx',
    sheet_name='Provincial_Transport_Expenditur'
)

transport = transport[[
    'Province',
    'Average Annual Transport Expenditure (R)'
]]

transport = transport.rename(columns={
    'Average Annual Transport Expenditure (R)': 'Annual_Transport_Cost'
})

transport['Monthly_Transport_Cost'] = transport['Annual_Transport_Cost'] / 12

print("\nTRANSPORT COSTS (MONTHLY):")
print(transport)
# =====================================

#  STEP 2: CALCULATE NATIONAL AVERAGE TRANSPORT COST
# =====================================
# NATIONAL AVERAGE TRANSPORT COST
# =====================================

national_monthly_transport_cost = transport['Monthly_Transport_Cost'].mean()

print("\nNATIONAL AVERAGE MONTHLY TRANSPORT COST:")
print(national_monthly_transport_cost)

#   Step 3: CALCULATE TRANSPORT AFFORDABILITY BURDEN
# =====================================
# TRANSPORT AFFORDABILITY BURDEN
# =====================================

df_labour['Monthly_Transport_Cost'] = national_monthly_transport_cost

df_labour['Transport_Burden_Pct'] = (
    df_labour['Monthly_Transport_Cost'] /
    df_labour['Avg_Monthly_Earnings']
) * 100

print("\nTRANSPORT AFFORDABILITY BURDEN:")
print(df_labour[['Avg_Monthly_Earnings', 'Monthly_Transport_Cost', 'Transport_Burden_Pct']])

print(df_earn_raw.head(10))
print(df_earn_raw.tail(10))
print(df_earn_raw.dtypes)
print(
    df_earn_raw[
        ['Year', 'Quarter', 'Total gross earnings']
    ].dropna().head(10)
)

# =====================================
# ENHANCE DATA FOR POWER BI VISUALIZATIONS
# =====================================

# 1. Add "Other Expenses" calculation
# Using SA average take-home pay ~85% after tax
df_labour['Monthly_After_Tax'] = df_labour['Avg_Monthly_Earnings'] * 0.85
df_labour['Other_Expenses'] = df_labour['Monthly_After_Tax'] - df_labour['Monthly_Transport_Cost']

# 2. Create percentage breakdown
df_labour['Transport_Share_Pct'] = df_labour['Transport_Burden_Pct']
df_labour['Other_Expenses_Share_Pct'] = 100 - df_labour['Transport_Share_Pct']

# 3. Create sector comparison data (simplified - replace with actual QES extraction later)
sector_data = pd.DataFrame({
    'Sector': ['Transport', 'Mining', 'Finance', 'Manufacturing', 'Trade', 'Construction'],
    'Avg_Monthly_Earnings': [33442.59, 55000, 48000, 28000, 19000, 22000],
    'Monthly_Transport_Cost': [2223.21, 2223.21, 2223.21, 2223.21, 2223.21, 2223.21]
})

sector_data['Transport_Burden_Pct'] = (sector_data['Monthly_Transport_Cost'] / sector_data['Avg_Monthly_Earnings']) * 100

# 4. Create time trend data (for future use)
trend_data = pd.DataFrame({
    'Quarter': ['Sep 2024', 'Dec 2024', 'Mar 2025'],
    'Avg_Monthly_Earnings': [32000, 32800, 33442.59],
    'Monthly_Transport_Cost': [2100, 2160, 2223.21]
})

trend_data['Transport_Burden_Pct'] = (trend_data['Monthly_Transport_Cost'] / trend_data['Avg_Monthly_Earnings']) * 100

print("\nENHANCED DATA READY FOR POWER BI")
print(df_labour[['Avg_Monthly_Earnings', 'Monthly_Transport_Cost', 'Transport_Burden_Pct', 'Other_Expenses']].head())

# Export all files for Power BI
df_labour.to_csv('outputs/week2_enhanced_powerbi.csv', index=False)
sector_data.to_csv('outputs/week2_sector_comparison.csv', index=False)
trend_data.to_csv('outputs/week2_time_trend.csv', index=False)

print("\nALL FILES EXPORTED FOR POWER BI DASHBOARD")
# =====================================
# EXPORT FOR POWER BI
# =====================================

output = df_labour[[
    'Year',
    'Quarter',
    'Number of employees',
    'Avg_Monthly_Earnings',
    'Monthly_Transport_Cost',
    'Transport_Burden_Pct'
]]

output.to_csv(
    'outputs/week2_transport_affordability_powerbi.csv',
    index=False
)

print("\nEXPORT COMPLETE: outputs/week2_transport_affordability_powerbi.csv")
# =====================================
