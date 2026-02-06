"""
Preview Module
Fungsi untuk preview data sebelum generate SQL
"""

import pandas as pd


def preview_data(df, max_rows=5):
    """
    Preview DataFrame
    
    Args:
        df (pandas.DataFrame): Data to preview
        max_rows (int): Max rows to display
        
    Returns:
        pandas.DataFrame: Full dataframe (unchanged)
    """
    print("\n" + "=" * 60)
    print("  PREVIEW DATA")
    print("=" * 60)
    
    print(f"\n📊 Total Data: {len(df)} rows × {len(df.columns)} columns")
    
    # Show column names
    print(f"\n📋 Kolom ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:3d}. {col}")
    
    # Show sample data
    print(f"\n🔍 Sample Data (first {min(max_rows, len(df))} rows):")
    print("-" * 60)
    
    # Show key columns only for preview
    key_columns = []
    for col in ['No', 'Nama Lengkap', 'Jenjang Yg Dipilih ( RA-MI-MTs-MA)', 
                'NIK', 'Tempat Lahir ', 'Tanggal Lahir', 'Jenis Kelamin']:
        if col in df.columns:
            key_columns.append(col)
    
    if key_columns:
        preview_df = df[key_columns].head(max_rows)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 30)
        print(preview_df.to_string(index=False))
    else:
        # Fallback: show first few columns
        preview_df = df.iloc[:max_rows, :5]
        print(preview_df.to_string(index=False))
    
    print("-" * 60)
    
    # Return full dataframe (tidak diubah)
    return df