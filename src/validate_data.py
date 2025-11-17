import pymysql
from config import DB_CONFIG

def validate_data():
    print("Validating loaded data\n")
    
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        tables = ['property', 'Leads', 'LeadsInfo', 'Valuation', 'HOA', 'Rehab', 'Taxes']
        
        print("Record counts:")
        print("-"*60)
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table:15} : {count:,} records")
        
        print("\nSample data from property table (first 3 records):")
        print("-"*60)
        cursor.execute("SELECT property_id, Property_Title, City, State, Year_Built FROM property LIMIT 3")
        rows = cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1][:40]}, Location: {row[2]}, {row[3]}, Built: {row[4]}")
        
        print("\nChecking foreign key relationships:")
        print("-"*60)
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM property) as properties,
                (SELECT COUNT(DISTINCT property_id) FROM Leads) as leads_links,
                (SELECT COUNT(DISTINCT property_id) FROM Valuation) as valuation_links
        """)
        row = cursor.fetchone()
        print(f"Properties: {row[0]:,}")
        print(f"Linked in Leads: {row[1]:,}")
        print(f"Linked in Valuation: {row[2]:,}")
        
        cursor.close()
        connection.close()
        
        print("\nValidation complete!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    validate_data()