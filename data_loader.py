
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# --- STEP 1: CONFIGURATION ---
num_records = 10000
products = ['Microwave', 'Fridge', 'Washing Machine', 'AC', 'TV']
channels = ['Retail Store', 'Dealer', 'Online']
dealers = ['Dealer1', 'Dealer2', 'Dealer3', 'Dealer4']
geographies = ['North', 'South', 'East', 'West', 'Central']
campaigns = ['Camp1', 'Camp2', 'Camp3', None]

print("Generating 10,000 records...")

# --- STEP 2: RANDOM DATA GENERATION ---
data = {
    'sale_date': [datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(num_records)],
    'product': np.random.choice(products, num_records),
    'channel': np.random.choice(channels, num_records),
    'dealer': np.random.choice(dealers, num_records),
    'geography': np.random.choice(geographies, num_records),
    'quantity': np.random.randint(1, 10, num_records),
    'unit_price': np.random.uniform(5000, 50000, num_records).round(2),
    'customer_id': [f'CUST{i}' for i in np.random.randint(1000, 5000, num_records)],
    'campaign_id': np.random.choice(campaigns, num_records),
    'is_repeat': np.random.choice([0, 1], num_records, p=[0.7, 0.3])
}

df = pd.DataFrame(data)

# --- STEP 3: CALCULATE TOTAL AMOUNT ---
df['total_amount'] = df['quantity'] * df['unit_price']

# --- STEP 4: DATABASE CONNECTION SETUP ---
# IMPORTANT: .
# Example: 'my@pass' -> 'my%40pass'
DB_USER = 'postgres'
DB_PASSWORD = 'password'  # <---   password  
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'sales_db'  # <--- Ensure database pgAdmin  

# Connection String
conn_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(conn_string)

# --- STEP 5: INSERT INTO POSTGRESQL ---
try:
    print("Connecting to PostgreSQL and inserting data...")
     
    df.to_sql('sales_data', engine, if_exists='replace', index=False)
    
    print("-" * 30)
    print("SUCCESS: 10,000 records inserted into PostgreSQL!")
    print(f"Table Name: sales_data")
    print("-" * 30)
    
except Exception as e:
    print("-" * 30)
    print(f"ERROR: check mistake!\n{e}")
    print("-" * 30)

# Dashboard ke liye sample view
print("\nFirst 5 records of generated data:")
print(df.head())