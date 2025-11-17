import re
import json

def fix_json_completely():
    print("Fixing entire JSON file\n")
    
    try:
        with open('../data/fake_property_data_new.json', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"File size: {len(content):,} characters")
        print(f"Lines: {content.count(chr(10)):,}")
        
        print("\nFixing unquoted values...")
        content = re.sub(r':\s*(\d+)\s+sqfts?\s*([,\n])', r': "\1 sqfts"\2', content)
        
        print("Fixing unquoted text like 'Five', 'Three', etc...")
        content = re.sub(r':\s*(Five|Four|Three|Two|One|Six|Seven|Eight|Nine|Ten)\s*,', r': "\1",', content)
        
        print("Removing stray values without keys...")
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and stripped.replace(',', '').isdigit() and ':' not in line:
                continue
            if stripped and not any(c in stripped for c in ['{', '}', ':', '[', ']']) and stripped not in [',']:
                continue
            fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        print("Fixing trailing commas...")
        content = re.sub(r',(\s*[}\]])', r'\1', content)
        
        print("Fixing missing commas...")
        content = re.sub(r'"\s*\n\s*"', '",\n    "', content)
        
        print("Converting None to null...")
        content = re.sub(r':\s*None\s*([,\n}])', r': null\1', content)
        
        print("\nAttempting to parse fixed JSON...")
        
        try:
            data = json.loads(content)
            print(f"SUCCESS!")
            print(f"Total records: {len(data):,}")
            
            with open('../data/property_data_clean.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            print(f"Saved clean JSON: property_data_clean.json")
            
            if len(data) > 0:
                first = data[0]
                print(f"\nFirst record sample:")
                print(f"   Fields: {len(first)}")
                for key in list(first.keys())[:10]:
                    print(f"   - {key}: {first[key]}")
            
            return data
            
        except json.JSONDecodeError as e:
            print(f"Error: {e}")
            return None
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    data = fix_json_completely()
    
    if data and len(data) > 0:
        print(f"\nSuccessfully processed {len(data):,} records!")
    else:
        print("\nFailed to process JSON completely")