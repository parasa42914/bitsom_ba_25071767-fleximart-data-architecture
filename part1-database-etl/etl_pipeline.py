import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import re
from datetime import datetime

# --- DATABASE CONFIGURATION ---
# Database Configuration
DB_TYPE = 'postgresql'
DB_DRIVER = 'psycopg2'
DB_USER = 'postgres'
DB_PASS = 'parasa42914'  # Replace with your actual password
DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'fleximart'

# Ensure your password is correct here
DB_URL = f"{DB_TYPE}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

def clean_phone(phone):
    if pd.isna(phone): return None
    # Use raw string r'\D' to avoid SyntaxWarnings
    nums = re.sub(r'\D', '', str(phone))
    return f"+91-{nums[-10:]}"

def clean_date(date_str):
    if pd.isna(date_str) or str(date_str).strip() == "": 
        return None
    try:
        # format='mixed' handles DD/MM and YYYY-MM efficiently
        return pd.to_datetime(date_str, format='mixed', dayfirst=True).date()
    except Exception:
        return pd.to_datetime(date_str, errors='coerce').date()

def run_etl():
    # --- 1. EXTRACTION ---
    try:
        cust_df = pd.read_csv('data\customers_raw.csv')
        prod_df = pd.read_csv('data\products_raw.csv')
        sales_df = pd.read_csv('data\sales_raw.csv')
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        return

    stats = {
        "cust_proc": len(cust_df), "prod_proc": len(prod_df), "sales_proc": len(sales_df),
        "cust_dupes": 0, "prod_dupes": 0, "sales_dupes": 0,
        "fill_email": 0, "fill_price": 0, "fill_stock": 0, "dropped_ids": 0,
        "std_phone": 0, "std_cat": 0, "std_date": 0
    }

    # --- 2. TRANSFORMATION ---

    # Customers
    stats["cust_dupes"] = cust_df.duplicated(subset=['first_name', 'last_name', 'phone']).sum()
    cust_df.drop_duplicates(subset=['first_name', 'last_name', 'phone'], inplace=True)
    stats["fill_email"] = cust_df['email'].isna().sum()
    cust_df['email'] = cust_df.apply(lambda r: f"{str(r['first_name']).lower()}@fleximart.com" if pd.isna(r['email']) else r['email'], axis=1)
    cust_df['phone'] = cust_df['phone'].apply(clean_phone)
    stats["std_phone"] = len(cust_df)
    cust_df['registration_date'] = cust_df['registration_date'].apply(clean_date)

    # Products
    stats["prod_dupes"] = prod_df.duplicated().sum()
    prod_df.drop_duplicates(inplace=True)
    stats["std_cat"] = (prod_df['category'] != prod_df['category'].str.capitalize()).sum()
    prod_df['category'] = prod_df['category'].str.strip().str.capitalize()
    stats["fill_price"] = prod_df['price'].isna().sum()
    prod_df['price'] = pd.to_numeric(prod_df['price'], errors='coerce').fillna(0.0)
    stats["fill_stock"] = prod_df['stock_quantity'].isna().sum()
    prod_df['stock_quantity'] = pd.to_numeric(prod_df['stock_quantity'], errors='coerce').fillna(0).astype(int)

    # Sales
    stats["sales_dupes"] = sales_df.duplicated(subset=['transaction_id']).sum()
    sales_df.drop_duplicates(subset=['transaction_id'], inplace=True)
    stats["dropped_ids"] = sales_df[['customer_id', 'product_id']].isna().any(axis=1).sum()
    sales_df.dropna(subset=['customer_id', 'product_id'], inplace=True)
    stats["std_date"] = len(sales_df)
    sales_df['transaction_date'] = sales_df['transaction_date'].apply(clean_date)
    
    # ID Extraction - Using Raw Strings r'\D'
    sales_df['customer_id'] = sales_df['customer_id'].str.replace(r'\D', '', regex=True).astype(int)
    sales_df['product_id'] = sales_df['product_id'].str.replace(r'\D', '', regex=True).astype(int)

    # --- 3. LOADING ---
    
    try:
        with engine.begin() as conn:
            # Clear old data to prevent UniqueViolations and primary key conflicts
            conn.execute(text("TRUNCATE TABLE order_items, orders, products, customers RESTART IDENTITY CASCADE;"))
            
            # Load Customers
            cust_df.drop(columns=['customer_id']).to_sql('customers', conn, if_exists='append', index=False)
            
            # Load Products
            prod_df.drop(columns=['product_id']).to_sql('products', conn, if_exists='append', index=False)
            
            # Load Orders
            orders_df = sales_df[['customer_id', 'transaction_date', 'unit_price', 'status']].copy()
            orders_df.columns = ['customer_id', 'order_date', 'total_amount', 'status']
            orders_df.to_sql('orders', conn, if_exists='append', index=False)
            
        status_msg = "SUCCESS"
    except Exception as e:
        status_msg = f"FAILED: {e}"

    # --- 4. GENERATE REPORT ---
    report_content = f"""=====================================================
FLEXIMART ETL DATA QUALITY REPORT
Date: {datetime.now().strftime('%Y-%m-%d')}
=====================================================

1. EXTRACTION SUMMARY
-----------------------------------------------------
- customers_raw.csv: {stats['cust_proc']} records processed
- products_raw.csv:  {stats['prod_proc']} records processed
- sales_raw.csv:     {stats['sales_proc']} records processed

2. TRANSFORMATION (CLEANING) SUMMARY
-----------------------------------------------------
- Duplicates Removed:
    * Customers: {stats['cust_dupes']}
    * Products:  {stats['prod_dupes']}
    * Sales:     {stats['sales_dupes']}
    
- Missing Values Handled:
    * Emails (filled with default): {stats['fill_email']}
    * Prices (filled with 0.0): {stats['fill_price']}
    * Stock (filled with 0): {stats['fill_stock']}
    * Customer/Product IDs (dropped): {stats['dropped_ids']}

- Standardizations Applied:
    * Phone Formats: {stats['std_phone']} records standardized to +91-XXXXXXXXXX
    * Category Names: {stats['std_cat']} records normalized to Title Case
    * Date Formats: {stats['std_date']} records converted to YYYY-MM-DD

3. LOADING SUMMARY
-----------------------------------------------------
- Target Database: postgresql ({DB_NAME})
- Records Loaded Successfully:
    * Table 'customers': {len(cust_df)}
    * Table 'products':  {len(prod_df)}
    * Table 'orders':    {len(sales_df)}

- Status: {status_msg}
====================================================="""

    with open('data_quality_report.txt', 'w') as f:
        f.write(report_content)
    
    print(f"ETL Job Finished. Status: {status_msg}")

if __name__ == "__main__":
    run_etl()