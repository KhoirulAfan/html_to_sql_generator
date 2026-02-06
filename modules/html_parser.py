"""
HTML Parser Module - FIXED VERSION
Fungsi untuk parsing HTML table ke pandas DataFrame
"""

import pandas as pd
from bs4 import BeautifulSoup


def input_html():
    """
    Input HTML content dari user
    Returns: string HTML
    """
    print("\n📋 Paste HTML table Anda di bawah ini.")
    print("Ketik 'END' pada baris baru untuk selesai:\n")
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    
    html_content = '\n'.join(lines)
    return html_content


def parse_html_table(html_content):
    """
    Parse HTML table menjadi pandas DataFrame
    FIXED: Handle column count mismatch
    
    Args:
        html_content (str): HTML string containing table
        
    Returns:
        pandas.DataFrame: Parsed table data
    """
    try:
        # Parse dengan BeautifulSoup
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Cari table
        table = soup.find('table')
        if not table:
            print("❌ Tidak ditemukan tag <table> dalam HTML")
            return None
        
        # Extract headers dari <th>
        headers = []
        header_row = table.find('tr')
        if header_row:
            for th in header_row.find_all('th'):
                header_text = th.get_text(strip=True)
                headers.append(header_text)
        
        if not headers:
            print("❌ Tidak ditemukan header (<th>) dalam table")
            return None
        
        print(f"📊 Ditemukan {len(headers)} kolom header")
        
        # Extract data rows
        rows = []
        all_trs = table.find_all('tr')
        
        for i, tr in enumerate(all_trs[1:], 1):  # Skip header row
            cells = []
            tds = tr.find_all('td')
            
            # Ambil semua cell
            for td in tds:
                cell_text = td.get_text(strip=True)
                cells.append(cell_text)
            
            # Skip empty rows
            if not cells or all(c == '' for c in cells):
                continue
            
            # FIX: Pad atau trim cells agar sesuai dengan jumlah headers
            if len(cells) < len(headers):
                # Pad dengan empty string jika kurang
                cells.extend([''] * (len(headers) - len(cells)))
                print(f"⚠️  Row {i}: Padded {len(headers) - len(cells)} missing columns")
            elif len(cells) > len(headers):
                # Trim jika lebih
                print(f"⚠️  Row {i}: Trimmed {len(cells) - len(headers)} extra columns")
                cells = cells[:len(headers)]
            
            rows.append(cells)
        
        if not rows:
            print("❌ Tidak ada data rows ditemukan")
            return None
        
        # Buat DataFrame
        df = pd.DataFrame(rows, columns=headers)
        
        # Clean data
        df = df.replace('', None)  # Empty string jadi NULL
        df = df.replace('0000-00-00', None)  # Invalid date jadi NULL
        df = df.replace('0000-00-00 00:00:00', None)  # Invalid datetime jadi NULL
        
        # Clean leading apostrophes (from Excel-style text formatting)
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(lambda x: x[1:] if isinstance(x, str) and x.startswith("'") else x)
        
        print(f"✓ Berhasil parse {len(df)} baris × {len(df.columns)} kolom")
        
        return df
        
    except Exception as e:
        print(f"❌ Error parsing HTML: {e}")
        import traceback
        traceback.print_exc()
        return None


def parse_html_from_file(file_path):
    """
    Parse HTML table dari file
    
    Args:
        file_path (str): Path ke file HTML
        
    Returns:
        pandas.DataFrame: Parsed table data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        return parse_html_table(html_content)
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None