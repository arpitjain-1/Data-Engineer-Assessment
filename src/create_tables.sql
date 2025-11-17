USE data_engineer_db;

DROP TABLE IF EXISTS HOA;
DROP TABLE IF EXISTS Leads;
DROP TABLE IF EXISTS Rehab;
DROP TABLE IF EXISTS Taxes;
DROP TABLE IF EXISTS Valuation;
DROP TABLE IF EXISTS leads;
DROP TABLE IF EXISTS property;

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
);

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
);

CREATE TABLE leads (
    leads_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    Selling_Reason VARCHAR(100),
    Seller_Retained_Broker VARCHAR(255),
    Final_Reviewer VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
);

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
);

CREATE TABLE HOA (
    HOA_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    HOA DECIMAL(10,2),
    HOA_Flag BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
);

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
);

CREATE TABLE Taxes (
    Taxes_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    Taxes DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
);
