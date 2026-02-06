"""
Output Module
Fungsi untuk output SQL ke file atau console
"""

import os
from datetime import datetime


def output_sql(sql_queries, output_dir='output'):
    """
    Output SQL queries to file
    
    Args:
        sql_queries (list): List of SQL INSERT statements
        output_dir (str): Directory untuk output files
    """
    # Create output directory if not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'insert_statements_{timestamp}.sql'
    filepath = os.path.join(output_dir, filename)
    
    # Write to file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            # Write header
            f.write("-- SQL INSERT Statements\n")
            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- Total Records: {len(sql_queries)}\n")
            f.write("-" * 80 + "\n\n")
            
            # Write queries
            for i, sql in enumerate(sql_queries, 1):
                f.write(f"-- Record {i}\n")
                f.write(sql + "\n\n")
        
        print(f"\n✓ SQL berhasil disimpan ke: {filepath}")
        print(f"📄 File size: {os.path.getsize(filepath):,} bytes")
        
        # Ask if user wants to see preview
        show_preview = input("\nTampilkan preview query pertama? (y/n): ").strip().lower()
        if show_preview == 'y':
            print("\n" + "=" * 80)
            print("PREVIEW - Query #1:")
            print("=" * 80)
            print(sql_queries[0][:500] + "...")
            print("=" * 80)
        
        return filepath
        
    except Exception as e:
        print(f"❌ Error writing to file: {e}")
        return None