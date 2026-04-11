import pdfplumber

pdfs = {
    '2022': 'pdfs/scamwatch_2022.pdf',
    '2023': 'pdfs/scamwatch_2023.pdf',
    '2024': 'pdfs/scamwatch_2024.pdf',
    '2025': 'pdfs/scamwatch_2025.pdf',
}

for year, path in pdfs.items():
    print(f"\n{'='*50}")
    print(f"REPORT: {year}")
    print(f"{'='*50}")
    
    with pdfplumber.open(path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if tables:
                print(f"\nPage {i+1} has {len(tables)} table(s)")
                for j, table in enumerate(tables):
                    print(f"  Table {j+1}: {len(table)} rows x {len(table[0]) if table else 0} cols")
                    for row in table[:3]:
                        print(f"    {row}")