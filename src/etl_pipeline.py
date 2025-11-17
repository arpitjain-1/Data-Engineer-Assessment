import json
import pymysql
from config import DB_CONFIG

class ETLPipeline:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect_db(self):
        try:
            self.connection = pymysql.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            print("Connected to MySQL database")
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    def extract_data(self, filepath='../data/property_data_clean.json'):
        try:
            print(f"Extracting data from {filepath}...")
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Extracted {len(data):,} records")
            return data
        except Exception as e:
            print(f"Extraction failed: {e}")
            return None
    
    def transform_data(self, record):
        if isinstance(record.get('SQFT_Total'), str):
            record['SQFT_Total'] = record['SQFT_Total'].replace(' sqft', '').replace(' sqfts', '').replace('sqft', '').strip()
            if not record['SQFT_Total'] or not record['SQFT_Total'].replace('.', '').isdigit():
                record['SQFT_Total'] = None
        
        bool_fields = ['HOA_Flag', 'Flooring_Flag', 'Foundation_Flag', 'Roof_Flag', 
                       'HVAC_Flag', 'Kitchen_Flag', 'Bathroom_Flag', 'Appliances_Flag',
                       'Windows_Flag', 'Landscaping_Flag', 'Trashout_Flag']
        
        for field in bool_fields:
            if field in record:
                val = record[field]
                if val in ['Yes', 'yes', 'Y', 'y', True, 1, '1']:
                    record[field] = True
                elif val in ['No', 'no', 'N', 'n', False, 0, '0']:
                    record[field] = False
                else:
                    record[field] = None
        
        return record
    
    def safe_decimal(self, value):
        if value is None or value == '':
            return None
        try:
            return float(value)
        except:
            return None
    
    def safe_int(self, value):
        if value is None or value == '':
            return None
        try:
            return int(float(value))
        except:
            return None
    
    def load_property(self, record):
        sql = """
        INSERT INTO property (
            Property_Title, Address, Market, Flood, Street_Address, City, State, Zip,
            Property_Type, Highway, Train, Tax_Rate, SQFT_Basement, HTW, Pool, Commercial,
            Water, Sewage, Year_Built, SQFT_MU, SQFT_Total, Parking, Bed, Bath,
            BasementYesNo, Layout, Rent_Restricted, Neighborhood_Rating,
            Latitude, Longitude, Subdivision, School_Average
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        values = (
            record.get('Property_Title'), record.get('Address'), record.get('Market'),
            record.get('Flood'), record.get('Street_Address'), record.get('City'),
            record.get('State'), record.get('Zip'), record.get('Property_Type'),
            record.get('Highway'), record.get('Train'), self.safe_decimal(record.get('Tax_Rate')),
            self.safe_int(record.get('SQFT_Basement')), record.get('HTW'), record.get('Pool'),
            record.get('Commercial'), record.get('Water'), record.get('Sewage'),
            self.safe_int(record.get('Year_Built')), self.safe_int(record.get('SQFT_MU')), 
            record.get('SQFT_Total'), record.get('Parking'), self.safe_int(record.get('Bed')), 
            self.safe_decimal(record.get('Bath')), record.get('BasementYesNo'), record.get('Layout'), 
            record.get('Rent_Restricted'), self.safe_int(record.get('Neighborhood_Rating')), 
            self.safe_decimal(record.get('Latitude')), self.safe_decimal(record.get('Longitude')),
            record.get('Subdivision'), self.safe_decimal(record.get('School_Average'))
        )
        
        self.cursor.execute(sql, values)
        return self.cursor.lastrowid
    
    def load_leads(self, property_id, record):
        """Load Leads data"""
        sql = """
        INSERT INTO Leads (
            property_id, Reviewed_Status, Most_Recent_Status, Source,
            Occupancy, Net_Yield, IRR
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            property_id, record.get('Reviewed_Status'), record.get('Most_Recent_Status'),
            record.get('Source'), record.get('Occupancy'), 
            self.safe_decimal(record.get('Net_Yield')),
            self.safe_decimal(record.get('IRR'))
        )
        
        self.cursor.execute(sql, values)
    
    def load_leads_info(self, property_id, record):
        """Load LeadsInfo data"""
        sql = """
        INSERT INTO LeadsInfo (
            property_id, Selling_Reason, Seller_Retained_Broker, Final_Reviewer
        ) VALUES (%s, %s, %s, %s)
        """
        
        values = (
            property_id, record.get('Selling_Reason'),
            record.get('Seller_Retained_Broker'), record.get('Final_Reviewer')
        )
        
        self.cursor.execute(sql, values)
    
    def load_valuation(self, property_id, valuation_data):
        """Load Valuation data"""
        if not valuation_data:
            sql = """
            INSERT INTO Valuation (
                property_id, Previous_Rent, List_Price, Zestimate, ARV,
                Expected_Rent, Rent_Zestimate, Low_FMR, High_FMR, Redfin_Value
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(sql, (property_id, None, None, None, None, None, None, None, None, None))
            return
        
        if isinstance(valuation_data, dict):
            valuation_data = [valuation_data]
        
        sql = """
        INSERT INTO Valuation (
            property_id, Previous_Rent, List_Price, Zestimate, ARV,
            Expected_Rent, Rent_Zestimate, Low_FMR, High_FMR, Redfin_Value
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for val in valuation_data:
            if isinstance(val, dict):
                values = (
                    property_id, 
                    self.safe_decimal(val.get('Previous_Rent')), 
                    self.safe_decimal(val.get('List_Price')),
                    self.safe_decimal(val.get('Zestimate')), 
                    self.safe_decimal(val.get('ARV')), 
                    self.safe_decimal(val.get('Expected_Rent')),
                    self.safe_decimal(val.get('Rent_Zestimate')), 
                    self.safe_decimal(val.get('Low_FMR')),
                    self.safe_decimal(val.get('High_FMR')), 
                    self.safe_decimal(val.get('Redfin_Value'))
                )
                self.cursor.execute(sql, values)
    
    def load_hoa(self, property_id, record):
        sql = """
        INSERT INTO HOA (property_id, HOA, HOA_Flag)
        VALUES (%s, %s, %s)
        """
        
        values = (property_id, self.safe_decimal(record.get('HOA')), record.get('HOA_Flag'))
        self.cursor.execute(sql, values)
    
    def load_rehab(self, property_id, record):
        sql = """
        INSERT INTO Rehab (
            property_id, Underwriting_Rehab, Rehab_Calculation, Paint,
            Flooring_Flag, Foundation_Flag, Roof_Flag, HVAC_Flag, Kitchen_Flag,
            Bathroom_Flag, Appliances_Flag, Windows_Flag, Landscaping_Flag, Trashout_Flag
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            property_id, self.safe_decimal(record.get('Underwriting_Rehab')), 
            record.get('Rehab_Calculation'),
            record.get('Paint'), record.get('Flooring_Flag'), record.get('Foundation_Flag'),
            record.get('Roof_Flag'), record.get('HVAC_Flag'), record.get('Kitchen_Flag'),
            record.get('Bathroom_Flag'), record.get('Appliances_Flag'),
            record.get('Windows_Flag'), record.get('Landscaping_Flag'), record.get('Trashout_Flag')
        )
        
        self.cursor.execute(sql, values)
    
    def load_taxes(self, property_id, record):
        sql = """
        INSERT INTO Taxes (property_id, Taxes)
        VALUES (%s, %s)
        """
        values = (property_id, self.safe_decimal(record.get('Taxes')))
        self.cursor.execute(sql, values)
    
    def run(self):
        print("="*80)
        print("STARTING ETL PIPELINE")
        print("="*80)
        
        if not self.connect_db():
            return False
        
        data = self.extract_data()
        if not data:
            return False
        
        print(f"\nTransforming and loading {len(data):,} records...")
        print("This may take a few minutes...\n")
        
        success_count = 0
        error_count = 0
        
        for i, record in enumerate(data, 1):
            try:
                record = self.transform_data(record)
                
                property_id = self.load_property(record)
                self.load_leads(property_id, record)
                self.load_leads_info(property_id, record)
                self.load_valuation(property_id, record.get('Valuation'))
                self.load_hoa(property_id, record)
                self.load_rehab(property_id, record)
                self.load_taxes(property_id, record)
                
                success_count += 1
                
                if i % 500 == 0:
                    self.connection.commit()  
                    print(f"   Processed {i:,}/{len(data):,} records...")
                
            except Exception as e:
                error_count += 1
                if error_count <= 5:
                    print(f"\nError on record {i}: {e}")
        
        self.connection.commit()
        
        print(f"\nETL Pipeline Complete!")
        print(f"Success: {success_count:,} records")
        print(f"Errors: {error_count:,} records")
        
        print(f"\nVerifying data in database...")
        tables = ['property', 'Leads', 'LeadsInfo', 'Valuation', 'HOA', 'Rehab', 'Taxes']
        
        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            print(f"   {table:15} : {count:,} records")
        
        self.cursor.close()
        self.connection.close()
        
        print(f"\n{'='*80}")
        print("ETL PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*80)
        
        return True

if __name__ == "__main__":
    pipeline = ETLPipeline()
    pipeline.run()