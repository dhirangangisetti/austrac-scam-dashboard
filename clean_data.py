import pdfplumber
import pandas as pd
import re

def clean_cell(val):
    if val is None:
        return ''
    return str(val).replace('\n', ' ').strip()

def clean_table(table):
    return [[clean_cell(c) for c in row] for row in table]

def parse_money(val):
    """Convert $318.8m or $2.7b to float in millions."""
    if not val:
        return None
    val = val.replace('$', '').replace(',', '').strip()
    val = re.sub(r'[^\d.mb]', '', val.lower())
    if val.endswith('b'):
        return float(val[:-1]) * 1000
    elif val.endswith('m'):
        return float(val[:-1])
    try:
        return float(val)
    except:
        return None

def parse_number(val):
    """Convert '301,778' to int."""
    if not val:
        return None
    val = re.sub(r'[^\d]', '', val)
    try:
        return int(val)
    except:
        return None

# ── 2024 Organisation Summary ─────────────────────────────────────────────────
with pdfplumber.open('pdfs/scamwatch_2024.pdf') as pdf:
    raw = clean_table(pdf.pages[5].extract_tables()[0])

orgs_2024 = []
org_names = ['Scamwatch', 'ReportCyber', 'AFCX', 'ASIC', 'IDCARE', 'Adjustments']
data_rows = [r for r in raw if r[0] in org_names]

for row in data_rows:
    orgs_2024.append({
        'year': 2024,
        'organisation': row[0],
        'reports_2023': parse_number(row[1]),
        'losses_2023_m': parse_money(row[2]),
        'reports_2024': parse_number(row[3]),
        'losses_2024_m': parse_money(row[4]),
        'pct_change': row[5].replace('\uf071', '↓').replace('p', '↑').strip()
    })

df_orgs = pd.DataFrame(orgs_2024)

# AFCX and IDCARE dropped due to formatting - add manually from report
manual_orgs = pd.DataFrame([
    {'year': 2024, 'organisation': 'AFCX', 'reports_2023': 217284,
     'losses_2023_m': 1182.4, 'reports_2024': 169184, 'losses_2024_m': 812.3, 'pct_change': '-31.3% ↓'},
    {'year': 2024, 'organisation': 'IDCARE', 'reports_2023': 30553,
     'losses_2023_m': 366.7, 'reports_2024': 42193, 'losses_2024_m': 513.6, 'pct_change': '40.1% ↑'},
])
df_orgs = pd.concat([df_orgs, manual_orgs], ignore_index=True)

print("Organisation Summary 2024:")
print(df_orgs.to_string())

# ── 2024 Scam Type Breakdown ──────────────────────────────────────────────────
with pdfplumber.open('pdfs/scamwatch_2024.pdf') as pdf:
    raw = clean_table(pdf.pages[6].extract_tables()[1])

scam_names_2024 = [
    'Investment', 'Payment redirection', 'Romance',
    'Phishing', 'Remote access', 'Other'
]

# Investment total is in row index 1, others from index 2 onwards
investment_total_2024 = parse_money('$945.0m')
investment_scamwatch_2024 = parse_money('$192.3m')

other_rows = [r for r in raw[2:] if r[7] != '']

totals_2024 = [investment_total_2024] + [parse_money(r[7]) for r in other_rows]
scamwatch_2024 = [investment_scamwatch_2024] + [parse_money(r[1]) for r in other_rows]

df_scams_2024 = pd.DataFrame({
    'year': 2024,
    'scam_type': scam_names_2024[:len(totals_2024)],
    'scamwatch_m': scamwatch_2024,
    'total_m': totals_2024
})
print("\nScam Type Breakdown 2024:")
print(df_scams_2024.to_string())

# ── 2025 Scam Type Breakdown ──────────────────────────────────────────────────
with pdfplumber.open('pdfs/scamwatch_2025.pdf') as pdf:
    raw = clean_table(pdf.pages[7].extract_tables()[1])

scam_names_2025 = [
    'Investment', 'Payment redirection', 'Romance',
    'Phishing', 'Remote access', 'Other'
]

investment_total_2025 = parse_money('$837.7m')
investment_scamwatch_2025 = parse_money('$172.2m')

other_rows_2025 = [r for r in raw[2:] if r[7] != '']

totals_2025 = [investment_total_2025] + [parse_money(r[7]) for r in other_rows_2025]
scamwatch_2025 = [investment_scamwatch_2025] + [parse_money(r[1]) for r in other_rows_2025]

df_scams_2025 = pd.DataFrame({
    'year': 2025,
    'scam_type': scam_names_2025[:len(totals_2025)],
    'scamwatch_m': scamwatch_2025,
    'total_m': totals_2025
})
print("\nScam Type Breakdown 2025:")
print(df_scams_2025.to_string())

# ── Combined scam types 2022 and 2023 (manually verified from reports) ────────
df_scams_2022 = pd.DataFrame([
    {'year': 2022, 'scam_type': 'Investment', 'scamwatch_m': 377.1, 'total_m': 1500.0},
    {'year': 2022, 'scam_type': 'Payment redirection', 'scamwatch_m': 16.2, 'total_m': 229.0},
    {'year': 2022, 'scam_type': 'Romance', 'scamwatch_m': 40.6, 'total_m': 142.0},
    {'year': 2022, 'scam_type': 'Phishing', 'scamwatch_m': 24.6, 'total_m': 24.6},
    {'year': 2022, 'scam_type': 'Remote access', 'scamwatch_m': 21.7, 'total_m': 21.7},
    {'year': 2022, 'scam_type': 'Other', 'scamwatch_m': 88.8, 'total_m': 1182.7},
])

df_scams_2023 = pd.DataFrame([
    {'year': 2023, 'scam_type': 'Investment', 'scamwatch_m': 293.8, 'total_m': 1300.0},
    {'year': 2023, 'scam_type': 'Payment redirection', 'scamwatch_m': 16.8, 'total_m': 232.0},
    {'year': 2023, 'scam_type': 'Romance', 'scamwatch_m': 33.9, 'total_m': 201.1},
    {'year': 2023, 'scam_type': 'Phishing', 'scamwatch_m': 11.3, 'total_m': 11.3},
    {'year': 2023, 'scam_type': 'Remote access', 'scamwatch_m': 19.5, 'total_m': 256.0},
    {'year': 2023, 'scam_type': 'Other', 'scamwatch_m': 101.5, 'total_m': 739.6},
])

# ── Yearly combined totals ────────────────────────────────────────────────────
yearly = pd.DataFrame([
    {'year': 2022, 'total_losses_b': 3.1, 'total_reports': 507000, 'scamwatch_losses_m': 569.0},
    {'year': 2023, 'total_losses_b': 2.74, 'total_reports': 601803, 'scamwatch_losses_m': 476.8},
    {'year': 2024, 'total_losses_b': 2.03, 'total_reports': 494732, 'scamwatch_losses_m': 318.8},
    {'year': 2025, 'total_losses_b': 2.18, 'total_reports': 481523, 'scamwatch_losses_m': 334.8},
])
print("\nYearly Combined Losses:")
print(yearly.to_string())

# ── Combine all scam type data ────────────────────────────────────────────────
df_scams_all = pd.concat(
    [df_scams_2022, df_scams_2023, df_scams_2024, df_scams_2025],
    ignore_index=True
)
print("\nAll Scam Types Combined:")
print(df_scams_all.to_string())

# ── Export all ────────────────────────────────────────────────────────────────
df_orgs.to_csv('org_summary_2024.csv', index=False)
df_scams_all.to_csv('scam_types_all_years.csv', index=False)
yearly.to_csv('yearly_totals.csv', index=False)

print("\nAll CSVs exported successfully.")