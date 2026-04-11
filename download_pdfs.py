import requests
import os

# ACCC/Scamwatch annual report PDFs - direct links
pdfs = {
    '2025': 'https://www.accc.gov.au/system/files/targeting-scams-report-2025.pdf',
    '2024': 'https://www.accc.gov.au/system/files/targeting-scams-report-2024.pdf',
    '2023': 'https://www.accc.gov.au/system/files/targeting-scams-report-activity-2023.pdf',
    '2022': 'https://www.accc.gov.au/system/files/Targeting+scams+2022.pdf',
}

os.makedirs('pdfs', exist_ok=True)

for year, url in pdfs.items():
    print(f"Downloading {year} report...")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            filepath = f'pdfs/scamwatch_{year}.pdf'
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Saved: {filepath} ({len(response.content) / 1024:.0f} KB)")
        else:
            print(f"Failed {year}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error {year}: {e}")

print("\nDownload complete.")