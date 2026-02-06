"""
HTML Parser Module - Parse HTML tables to DataFrame
"""
import pandas as pd
from bs4 import BeautifulSoup


def input_html():
    """Input HTML dari user via console"""
    print("\n📋 Paste HTML table di bawah ini.")
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
    
    return '\n'.join(lines)


def auto_fix_html(html_content):
    """Auto-fix HTML table - add missing </tr> tags"""
    lines = html_content.split('\n')
    fixed = []
    in_tr = False
    
    for line in lines:
        s = line.strip()
        
        # Opening <tr>
        if s.startswith('<tr'):
            if in_tr:  # Close previous unclosed <tr>
                fixed.append('</tr>')
            fixed.append(line)
            in_tr = True
        
        # Closing </tr>
        elif '</tr>' in s:
            fixed.append(line)
            in_tr = False
        
        # Table end
        elif s.startswith('</table>'):
            if in_tr:
                fixed.append('</tr>')
                in_tr = False
            fixed.append(line)
        
        # Regular content
        else:
            fixed.append(line)
    
    # Final cleanup
    if in_tr:
        fixed.append('</tr>')
    
    return '\n'.join(fixed)


def parse_html_table(html_content):
    """
    Parse HTML table to DataFrame
    
    Args:
        html_content (str): HTML string containing table
        
    Returns:
        pd.DataFrame or None: Parsed data as DataFrame
    """
    try:
        # Auto-fix HTML first
        print("🔧 Fixing HTML structure...")
        html_content = auto_fix_html(html_content)
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')
        
        if not table:
            print("❌ No <table> found in HTML")
            return None
        
        # Extract headers
        headers = []
        header_row = table.find('tr')
        if header_row:
            for th in header_row.find_all('th'):
                headers.append(th.get_text(strip=True))
        
        if not headers:
            print("❌ No headers (<th>) found in table")
            return None
        
        print(f"📊 Found {len(headers)} columns: {headers[:5]}..." if len(headers) > 5 else f"📊 Found {len(headers)} columns")
        
        # Extract data rows
        rows = []
        all_trs = table.find_all('tr')
        
        for i, tr in enumerate(all_trs[1:], 1):  # Skip header row
            tds = tr.find_all('td')
            
            if not tds:
                continue
            
            # Get cell values
            cells = [td.get_text(strip=True) for td in tds]
            
            # Skip completely empty rows
            if not cells or all(c == '' for c in cells):
                continue
            
            # Adjust cell count to match headers
            if len(cells) < len(headers):
                cells.extend([''] * (len(headers) - len(cells)))
            elif len(cells) > len(headers):
                cells = cells[:len(headers)]
            
            rows.append(cells)
            
            # Progress indicator for first few rows
            if i <= 3:
                print(f"  Row {i}: {len(cells)} cells")
        
        if not rows:
            print("❌ No data rows found")
            return None
        
        print(f"✅ Parsed {len(rows)} data rows\n")
        
        # Create DataFrame
        df = pd.DataFrame(rows, columns=headers)
        
        # Clean data
        df = df.replace('', None)
        df = df.replace('0000-00-00', None)
        df = df.replace('0000-00-00 00:00:00', None)
        
        # Clean leading apostrophes (Excel-style text markers)
        for col in df.columns:
            df[col] = df[col].apply(
                lambda x: x[1:] if isinstance(x, str) and x.startswith("'") else x
            )
        
        return df
        
    except Exception as e:
        print(f"❌ Error parsing HTML: {e}")
        import traceback
        traceback.print_exc()
        return None


def parse_html_from_file(file_path):
    """Parse HTML table from file
    
    Args:
        file_path (str): Path to HTML file
        
    Returns:
        pd.DataFrame or None: Parsed data
    """
    try:
        print(f"📂 Reading file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        return parse_html_table(html)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None


def save_to_csv(df, filename="parsed_data.csv"):
    """Save DataFrame to CSV
    
    Args:
        df (pd.DataFrame): DataFrame to save
        filename (str): Output filename
        
    Returns:
        bool: Success status
    """
    try:
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ Saved to CSV: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")
        return False