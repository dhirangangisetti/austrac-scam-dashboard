import pdfplumber
import pandas as pd

# ── helpers ──────────────────────────────────────────────────────────────────

def clean_cell(val):
    """Strip whitespace and newlines from a cell value."""
    if val is None:
        return ''
    return str(val).replace('\n', ' ').strip()

def clean_table(table):
    """Apply clean_cell to every cell in a table."""
    return [[clean_cell(c) for c in row] for row in table]

def extract_page_tables(pdf_path, page_num):
    """Extract and clean all tables from a specific page (1-indexed)."""
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num - 1]
        tables = page.extract_tables()
        return [clean_table(t) for t in tables]

# ── 2022 ─────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("EXTRACTING 2022")
print("="*60)

# Organisation summary - page 15, table 1
tables = extract_page_tables('pdfs/scamwatch_2022.pdf', 15)
print("\n[2022] Page 15 - Organisation Summary:")
for row in tables[0]:
    print(row)

# Scam type breakdown - page 15, table 2
print("\n[2022] Page 15 - Scam Type Breakdown:")
for row in tables[1]:
    print(row)

# Age group - page 26, table 3
tables = extract_page_tables('pdfs/scamwatch_2022.pdf', 26)
print("\n[2022] Page 26 - Age Group:")
for row in tables[2]:
    print(row)

# Scam type losses - page 27
tables = extract_page_tables('pdfs/scamwatch_2022.pdf', 27)
print("\n[2022] Page 27 - Scam Type Losses:")
for row in tables[0]:
    print(row)

# ── 2023 ─────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("EXTRACTING 2023")
print("="*60)

# Organisation summary - page 8
tables = extract_page_tables('pdfs/scamwatch_2023.pdf', 8)
print("\n[2023] Page 8 - Organisation Summary:")
for row in tables[0]:
    print(row)

# Scam type breakdown - page 9
tables = extract_page_tables('pdfs/scamwatch_2023.pdf', 9)
print("\n[2023] Page 9 - Scam Type Breakdown:")
for row in tables[0]:
    print(row)

# Contact method - page 17
tables = extract_page_tables('pdfs/scamwatch_2023.pdf', 17)
print("\n[2023] Page 17 - Contact Method:")
for row in tables[0]:
    print(row)

# Age group - page 16, table 2
tables = extract_page_tables('pdfs/scamwatch_2023.pdf', 16)
print("\n[2023] Page 16 - Age Group:")
for row in tables[1]:
    print(row)

# ── 2024 ─────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("EXTRACTING 2024")
print("="*60)

# Organisation summary - page 6
tables = extract_page_tables('pdfs/scamwatch_2024.pdf', 6)
print("\n[2024] Page 6 - Organisation Summary:")
for row in tables[0]:
    print(row)

# Scam type breakdown - page 7, table 2
tables = extract_page_tables('pdfs/scamwatch_2024.pdf', 7)
print("\n[2024] Page 7 - Scam Type Breakdown:")
for row in tables[1]:
    print(row)

# Age group - page 32
tables = extract_page_tables('pdfs/scamwatch_2024.pdf', 32)
print("\n[2024] Page 32 - Age Group:")
for row in tables[0]:
    print(row)

# ── 2025 ─────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("EXTRACTING 2025")
print("="*60)

# Organisation summary - page 7
tables = extract_page_tables('pdfs/scamwatch_2025.pdf', 7)
print("\n[2025] Page 7 - Organisation Summary:")
for row in tables[0]:
    print(row)

# Scam type breakdown - page 8, table 2
tables = extract_page_tables('pdfs/scamwatch_2025.pdf', 8)
print("\n[2025] Page 8 - Scam Type Breakdown:")
for row in tables[1]:
    print(row)

# Age group - page 43
tables = extract_page_tables('pdfs/scamwatch_2025.pdf', 43)
print("\n[2025] Page 43 - Age Group:")
for row in tables[0]:
    print(row)

print("\n\nExtraction complete.")