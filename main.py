"""
HTML to SQL Converter
Main entry point untuk aplikasi
"""

from modules.html_parser import input_html, parse_html_table
from modules.preview import preview_data
from modules.sql_generator import generate_sql
from modules.output import output_sql


def print_header():
    """Print header aplikasi"""
    print("=" * 60)
    print("  HTML TABLE TO SQL CONVERTER")
    print("  Version 2.0 - Bug Fixed Edition")
    print("=" * 60)


def main():
    """Main function"""
    print_header()
    
    # Input HTML
    html_content = input_html()
    
    # Parse HTML
    print("\n Parsing HTML...")
    df = parse_html_table(html_content)
    
    if df is None or df.empty:
        print(" Tidak ada data yang ditemukan.")
        return
    
    print(f"✓ Berhasil parse {len(df)} baris data")
    
    # Preview data (simpan FULL dataframe)
    full_df = preview_data(df)
    
    # Konfirmasi generate SQL
    confirm = input("\nLanjut ke generate SQL? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("✓ Dibatalkan.")
        return
    
    # Generate SQL dari SEMUA data
    print(f"\n  Generating SQL untuk {len(full_df)} baris...")
    sql_queries = generate_sql(full_df)
    
    # Output SQL
    output_sql(sql_queries)
    
    print("\n✓ Selesai!")
    print(f" Total {len(sql_queries)} query SQL berhasil di-generate")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Program dihentikan oleh user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()