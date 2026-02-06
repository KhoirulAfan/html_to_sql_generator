"""
SQL Generator - FINAL FIX (Series-proof)
"""
import pandas as pd
import numpy as np


def sanitize_column_name(col_name):
    """Clean column name"""
    s = col_name.lower().replace(' ', '_').replace('/', '_')
    s = ''.join(c for c in s if c.isalnum() or c == '_')
    while '__' in s:
        s = s.replace('__', '_')
    return s.strip('_')


def escape_value(val):
    """Escape SQL value - SERIES-PROOF"""
    # Handle Series (extract first value)
    if isinstance(val, pd.Series):
        if len(val) == 0:
            return 'NULL'
        val = val.iloc[0]
    
    # Handle None/NaN
    if val is None:
        return 'NULL'
    
    if isinstance(val, float) and np.isnan(val):
        return 'NULL'
    
    # Handle pandas NA types
    try:
        if pd.isna(val):
            return 'NULL'
    except:
        pass
    
    # Convert to string
    s = str(val).strip()
    
    if s == '' or s == 'nan' or s == 'None':
        return 'NULL'
    
    # Try numeric
    try:
        float(s)
        return s
    except:
        pass
    
    # String - escape quotes
    s = s.replace("'", "''")
    return f"'{s}'"


def generate_sql(df, table_name="students"):
    """Generate SQL"""
    print(f"\n🔧 Generating SQL...")
    
    # Sanitize columns
    cols = [sanitize_column_name(c) for c in df.columns]
    
    # CREATE TABLE
    create = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n"
    create += "  `id` INT AUTO_INCREMENT PRIMARY KEY,\n"
    for col in cols:
        create += f"  `{col}` VARCHAR(500),\n"
    create = create.rstrip(',\n') + "\n);\n\n"
    
    # INSERT statements
    inserts = []
    
    # METHOD 1: Use itertuples (faster & safer)
    for row in df.itertuples(index=False):
        values = []
        
        for i, cell in enumerate(row):
            values.append(escape_value(cell))
        
        cols_str = ', '.join([f'`{c}`' for c in cols])
        vals_str = ', '.join(values)
        
        sql = f"INSERT INTO `{table_name}` ({cols_str}) VALUES ({vals_str});\n"
        inserts.append(sql)
        
        if len(inserts) % 10 == 0:
            print(f"  ✓ {len(inserts)}/{len(df)} rows...")
    
    print(f"✅ Done! {len(inserts)} INSERT statements")
    
    return {
        'create_table': create,
        'inserts': inserts,
        'full_sql': create + '\n'.join(inserts)
    }


def save_sql(sql_dict, filename="output.sql"):
    """Save to file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(sql_dict['full_sql'])
        print(f"✅ Saved: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False