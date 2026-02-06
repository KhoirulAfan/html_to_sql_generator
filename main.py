
from modules.html_parser import input_html, parse_html_table
from modules.sql_generator_advance import generate_sql_advanced, save_sql


def main():
    print("\n" + "="*60)
    print("  HTML TO SQL GENERATOR")
    print("="*60)
    
    # 1. Input Subdomain
    print("\n🏷️  SUBDOMAIN CONFIGURATION")
    subdomain = input("Masukkan subdomain (contoh: sekolah123): ").strip()
    
    if not subdomain:
        print("❌ Subdomain tidak boleh kosong!")
        return
    
    print(f"✅ Subdomain: {subdomain}")
    
    # 2. Input HTML
    html = input_html()
    if not html:
        print("❌ No HTML")
        return
    
    # 3. Parse
    print("\n📋 Parsing HTML...")
    df = parse_html_table(html)
    
    if df is None or df.empty:
        print("❌ Parse failed")
        return
    
    print(f"✅ Success: {len(df)} rows × {len(df.columns)} columns")
    
    # 4. Add subdomain column to DataFrame
    print(f"\n🔧 Adding subdomain '{subdomain}' to all rows...")
    df.insert(0, 'subdomain', subdomain)
    print(f"✅ Subdomain added to {len(df)} rows")
    
    # 5. Preview
    print(f"\n🔍 Preview (first 3 rows):")
    print(df.head(3).to_string())
    
    # 6. Confirm
    ok = input("\n▶ Generate SQL? (y/n): ").strip().lower()
    if ok != 'y':
        print("❌ Cancelled")
        return
    
    # 7. Generate INSERT statements only
    print("\n🔧 Generating INSERT statements...")
    table = "psb_member"  # Fixed table name
    sql_dict = generate_sql_advanced(df, table_name=table)
    
    # 8. Extract only INSERT statements (no CREATE TABLE)
    insert_only = {
        'inserts': sql_dict['inserts'],
        'full_sql': '\n'.join(sql_dict['inserts'])
    }
    
    print(f"✅ Generated {len(sql_dict['inserts'])} INSERT statements")
    
    # 9. Save
    outfile = input("\nOutput file (default: insert_psb_member.sql): ").strip() or "insert_psb_member.sql"
    
    if not outfile.endswith('.sql'):
        outfile += '.sql'
    
    if save_sql(insert_only, outfile):
        print(f"\n{'='*60}")
        print(f"🎉 SUCCESS!")
        print(f"{'='*60}")
        print(f"📊 Total rows: {len(df)}")
        print(f"📝 INSERT statements: {len(sql_dict['inserts'])}")
        print(f"💾 File saved: {outfile}")
        print(f"🏷️  Subdomain: {subdomain}")
        print(f"{'='*60}")
    else:
        print("\n❌ Save failed")


if __name__ == "__main__":
    main()