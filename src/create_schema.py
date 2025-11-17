import pymysql
from config import DB_CONFIG

def execute_schema():
    print("Executing database schema...\n")
    
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("Connected to MySQL\n")
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        print("Dropping ALL existing tables")
        cursor.execute("SHOW TABLES")
        existing_tables = cursor.fetchall()
        for table in existing_tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
            print(f"Dropped {table[0]}")
        
        connection.commit()
        
        print("\nCreating property table")
        cursor.execute("""
        CREATE TABLE property (
            property_id INT AUTO_INCREMENT PRIMARY KEY,
            Property_Title VARCHAR(500),
            Address VARCHAR(500),
            Market VARCHAR(255),
            Flood VARCHAR(255),
            Street_Address VARCHAR(500),
            City VARCHAR(255),
            State VARCHAR(255),
            Zip VARCHAR(255),
            Property_Type VARCHAR(255),
            Highway VARCHAR(255),
            Train VARCHAR(255),
            Tax_Rate DECIMAL(6,2),
            SQFT_Basement INT,
            HTW VARCHAR(255),
            Pool VARCHAR(255),
            Commercial VARCHAR(255),
            Water VARCHAR(255),
            Sewage VARCHAR(255),
            Year_Built INT,
            SQFT_MU INT,
            SQFT_Total VARCHAR(255),
            Parking VARCHAR(255),
            Bed INT,
            Bath DECIMAL(3,1),
            BasementYesNo VARCHAR(10),
            Layout VARCHAR(255),
            Rent_Restricted VARCHAR(255),
            Neighborhood_Rating INT,
            Latitude DECIMAL(10,6),
            Longitude DECIMAL(10,6),
            Subdivision VARCHAR(255),
            School_Average DECIMAL(4,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """)
        print("Created property")
        
        print("Creating Leads table...")
        cursor.execute("""
        CREATE TABLE Leads (
            Leads_id INT AUTO_INCREMENT PRIMARY KEY,
            property_id INT NOT NULL,
            Reviewed_Status VARCHAR(100),
            Most_Recent_Status VARCHAR(100),
            Source VARCHAR(255),
            Occupancy VARCHAR(255),
            Net_Yield DECIMAL(6,2),
            IRR DECIMAL(6,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
        )
        """)
        print("Created Leads")
        
        print("Creating Valuation table")
        cursor.execute("""
        CREATE TABLE Valuation (
            Valuation_id INT AUTO_INCREMENT PRIMARY KEY,
            property_id INT NOT NULL,
            Previous_Rent DECIMAL(10,2),
            List_Price DECIMAL(12,2),
            Zestimate DECIMAL(12,2),
            ARV DECIMAL(12,2),
            Expected_Rent DECIMAL(10,2),
            Rent_Zestimate DECIMAL(10,2),
            Low_FMR DECIMAL(10,2),
            High_FMR DECIMAL(10,2),
            Redfin_Value DECIMAL(12,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
        )
        """)
        print("Created Valuation")
        
        print("Creating HOA table...")
        cursor.execute("""
        CREATE TABLE HOA (
            HOA_id INT AUTO_INCREMENT PRIMARY KEY,
            property_id INT NOT NULL,
            HOA DECIMAL(10,2),
            HOA_Flag BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
        )
        """)
        print("Created HOA")
        
        print("Creating Rehab table")
        cursor.execute("""
        CREATE TABLE Rehab (
            Rehab_id INT AUTO_INCREMENT PRIMARY KEY,
            property_id INT NOT NULL,
            Underwriting_Rehab DECIMAL(12,2),
            Rehab_Calculation VARCHAR(255),
            Paint VARCHAR(255),
            Flooring_Flag BOOLEAN,
            Foundation_Flag BOOLEAN,
            Roof_Flag BOOLEAN,
            HVAC_Flag BOOLEAN,
            Kitchen_Flag BOOLEAN,
            Bathroom_Flag BOOLEAN,
            Appliances_Flag BOOLEAN,
            Windows_Flag BOOLEAN,
            Landscaping_Flag BOOLEAN,
            Trashout_Flag BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
        )
        """)
        print("Created Rehab")
        
        print("Creating Taxes table")
        cursor.execute("""
        CREATE TABLE Taxes (
            Taxes_id INT AUTO_INCREMENT PRIMARY KEY,
            property_id INT NOT NULL,
            Taxes DECIMAL(12,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
        )
        """)
        print("Created Taxes")
        
        print("Creating LeadsInfo table")
        cursor.execute("""
        CREATE TABLE LeadsInfo (
            LeadsInfo_id INT AUTO_INCREMENT PRIMARY KEY,
            property_id INT NOT NULL,
            Selling_Reason VARCHAR(100),
            Seller_Retained_Broker VARCHAR(255),
            Final_Reviewer VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
        )
        """)
        print("Created LeadsInfo")
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        connection.commit()
        
        print("\nVerifying tables")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\nSuccessfully created {len(tables)} tables:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f" {table[0]:20} ({count} records)")
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*80)
        print("SCHEMA CREATED SUCCESSFULLY!")
        print("="*80)
        
        return True
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    execute_schema()