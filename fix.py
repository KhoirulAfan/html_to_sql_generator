"""
HTML Table Fixer
Memperbaiki HTML table yang missing </tr> tags
"""
import re
import sys


def fix_html_table(html_content):
    """
    Fix malformed HTML table by adding missing </tr> tags
    
    Args:
        html_content (str): Raw HTML content
    
    Returns:
        str: Fixed HTML content
    """
    print("🔧 Fixing HTML table...")
    
    # Split by lines
    lines = html_content.split('\n')
    fixed_lines = []
    
    inside_tr = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Check if opening <tr>
        if stripped.startswith('<tr'):
            # If we were already inside a <tr>, close it first
            if inside_tr:
                fixed_lines.append('</tr>')
            
            fixed_lines.append(line)
            inside_tr = True
        
        # Check if closing </tr>
        elif '</tr>' in stripped:
            fixed_lines.append(line)
            inside_tr = False
        
        # Check if it's a table tag or other non-data tag
        elif stripped.startswith('<table') or stripped.startswith('</table>'):
            # Close any open <tr> before table end
            if inside_tr and stripped.startswith('</table>'):
                fixed_lines.append('</tr>')
                inside_tr = False
            fixed_lines.append(line)
        
        # Regular content (th, td, etc)
        else:
            fixed_lines.append(line)
    
    # Close final <tr> if still open
    if inside_tr:
        fixed_lines.append('</tr>')
    
    fixed_html = '\n'.join(fixed_lines)
    
    # Count fixes
    original_tr_count = html_content.count('<tr')
    original_close_count = html_content.count('</tr>')
    fixed_close_count = fixed_html.count('</tr>')
    
    added = fixed_close_count - original_close_count
    
    print(f"📊 Statistics:")
    print(f"   Original <tr>: {original_tr_count}")
    print(f"   Original </tr>: {original_close_count}")
    print(f"   Fixed </tr>: {fixed_close_count}")
    print(f"   ✅ Added {added} closing tags")
    
    return fixed_html


def fix_html_from_file(input_file, output_file=None):
    """
    Fix HTML from file
    
    Args:
        input_file (str): Input HTML file path
        output_file (str): Output file path (optional)
    """
    try:
        # Read input
        with open(input_file, 'r', encoding='utf-8') as f:
            html = f.read()
        
        print(f"📖 Reading: {input_file}")
        
        # Fix
        fixed = fix_html_table(html)
        
        # Determine output file
        if not output_file:
            output_file = input_file.replace('.html', '_fixed.html')
        
        # Save
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fixed)
        
        print(f"✅ Saved to: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """Main function"""
    print("\n" + "="*60)
    print("  HTML TABLE FIXER")
    print("="*60)
    
    if len(sys.argv) > 1:
        # Command line mode
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        fix_html_from_file(input_file, output_file)
    else:
        # Interactive mode
        print("\nOptions:")
        print("1. Fix from file")
        print("2. Fix from clipboard/paste")
        
        choice = input("\nChoice (1/2): ").strip()
        
        if choice == "1":
            input_file = input("Input HTML file: ").strip()
            output_file = input("Output file (Enter for auto): ").strip() or None
            fix_html_from_file(input_file, output_file)
        
        elif choice == "2":
            print("\n📋 Paste HTML below. Type 'END' when done:\n")
            lines = []
            while True:
                try:
                    line = input()
                    if line.strip().upper() == 'END':
                        break
                    lines.append(line)
                except EOFError:
                    break
            
            html = '\n'.join(lines)
            fixed = fix_html_table(html)
            
            output_file = input("\nSave to file: ").strip()
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(fixed)
                print(f"✅ Saved to: {output_file}")
            else:
                print("\n📄 Fixed HTML:")
                print("="*60)
                print(fixed[:1000], "...")  # Preview


if __name__ == "__main__":
    main()