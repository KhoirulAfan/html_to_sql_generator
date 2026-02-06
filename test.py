"""
Test script untuk mengecek parsing dan SQL generation
"""

import pandas as pd
from bs4 import BeautifulSoup

# Copy fungsi dari modules
def escape_sql_value(value):
    """Escape value untuk SQL INSERT"""
    if pd.isna(value) or value is None:
        return "NULL"
    
    value_str = str(value).strip()
    
    if value_str == "":
        return "NULL"
    
    # Remove leading apostrophe
    if value_str.startswith("'"):
        value_str = value_str[1:]
    
    # Handle numeric values
    try:
        float_val = float(value_str)
        return str(float_val)
    except ValueError:
        pass
    
    # Escape single quotes
    value_str = value_str.replace("'", "''")
    
    return f"'{value_str}'"


def parse_html_table(html_content):
    """Parse HTML table"""
    soup = BeautifulSoup(html_content, 'lxml')
    table = soup.find('table')
    
    if not table:
        return None
    
    # Extract headers
    headers = []
    header_row = table.find('tr')
    if header_row:
        for th in header_row.find_all('th'):
            header_text = th.get_text(strip=True)
            headers.append(header_text)
    
    # Extract data rows
    rows = []
    all_trs = table.find_all('tr')
    
    for i, tr in enumerate(all_trs[1:], 1):
        cells = []
        tds = tr.find_all('td')
        
        for td in tds:
            cell_text = td.get_text(strip=True)
            cells.append(cell_text)
        
        if not cells or all(c == '' for c in cells):
            continue
        
        # Pad atau trim
        if len(cells) < len(headers):
            cells.extend([''] * (len(headers) - len(cells)))
        elif len(cells) > len(headers):
            cells = cells[:len(headers)]
        
        rows.append(cells)
    
    df = pd.DataFrame(rows, columns=headers)
    df = df.replace('', None)
    df = df.replace('0000-00-00', None)
    df = df.replace('0000-00-00 00:00:00', None)
    
    # Clean leading apostrophes
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: x[1:] if isinstance(x, str) and x.startswith("'") else x)
    
    return df


# HTML sample dari user
html_content = """<table id='mytable' width="100%" border="1">
<tr>
    <th>No</th>
    <th>Jalur ppdb</th>
    <th>Nomor pendaftaran</th>
    <th>Jenjang Yg Dipilih ( RA-MI-MTs-MA)</th>
    <th>Nama Lengkap</th>
    <th>NISN ( Jenjang TK Boleh Di Kosongkan )</th>
    <th>Status  ( Mondok / Pulang Pergi ) Khusus  MTs & MA </th>
    <th>Bahasa</th>
    <th>Jenjang  ( RA-MI-MTs-MA)</th>
    <th>NIK</th>
    <th>Nomor KK</th>
</tr>
<tr>
    <td>1</td>
    <td></td>
    <td></td>
    <td>RA</td>
    <td>Wibisana kautsarrazky</td>
    <td>1234567891</td>
    <td></td>
    <td></td>
    <td>dwimaulidasani@gmail.com</td>
    <td>'3509110301200003</td>
    <td>'3509111509150005</td>
</tr>
</table>"""

print("=" * 80)
print("TESTING HTML PARSER & SQL GENERATOR")
print("=" * 80)

# Parse HTML
df = parse_html_table(html_content)

print(f"\n1. PARSING RESULT:")
print(f"   Rows: {len(df)}")
print(f"   Columns: {len(df.columns)}")
print(f"\n   Headers:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i:2d}. {col}")

print(f"\n2. SAMPLE DATA (First Row):")
for col in df.columns:
    value = df.iloc[0][col]
    print(f"   {col}: {repr(value)}")

# Check specific problematic columns
print(f"\n3. CRITICAL COLUMNS CHECK:")
print(f"   Jenjang Yg Dipilih: {repr(df.iloc[0]['Jenjang Yg Dipilih ( RA-MI-MTs-MA)'])}")
print(f"   Jenjang (email): {repr(df.iloc[0]['Jenjang  ( RA-MI-MTs-MA)'])}")
print(f"   NIK: {repr(df.iloc[0]['NIK'])}")
print(f"   Nomor KK: {repr(df.iloc[0]['Nomor KK'])}")
print(f"   NISN: {repr(df.iloc[0]['NISN ( Jenjang TK Boleh Di Kosongkan )'])}")

# Test SQL escape
print(f"\n4. SQL ESCAPING TEST:")
test_values = [
    ('3509110301200003', 'NIK after clean'),
    ('3509111509150005', 'Nomor KK after clean'),
    ('dwimaulidasani@gmail.com', 'Email'),
    ('RA', 'Jenjang'),
    (None, 'NULL value'),
    ('', 'Empty string'),
    ('1234567891', 'NISN'),
]

for val, desc in test_values:
    escaped = escape_sql_value(val)
    print(f"   {desc:20s}: {repr(val):30s} → {escaped}")

print("\n" + "=" * 80)