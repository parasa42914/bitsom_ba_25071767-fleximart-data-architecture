# Part 1: Database Design and ETL Pipeline
## Overview
This section addresses the foundational step of the FlexiMart data journey: converting "dirty" raw CSV data into a clean, structured, and normalized Relational Database Management System (RDBMS). It focuses on data quality, schema integrity, and operational reporting.

## Files in this Section
`etl_pipeline.py`: A Python script using Pandas and SQLAlchemy to automate data cleaning and ingestion.

`schema_documentation.md`: Detailed technical documentation of the database entities, relationships, and 3NF normalization justification.

`business_queries.sql`: SQL scripts designed to answer core business questions regarding customer behavior and sales trends.

`data_quality_report.txt`: An automatically generated log detailing the results of the ETL process.

## The ETL Process
**1. Extract**</br>
The pipeline reads three primary source files containing intentional data quality issues:

* `customers_raw.csv`: Contained missing emails and inconsistent phone formats.

* `products_raw.csv`: Addressed null stock values and varying case sensitivity in categories.

* `sales_raw.csv`: Resolved date format inconsistencies and duplicate transactions.

**2. Transform (Data Cleaning)**</br>
* **Standardization:** Converted all phone numbers to a uniform format (e.g., `+91-XXXXXXXXXX`) using Regular Expressions.

* **Categorization:** Standardized product categories (e.g., "electronics", "ELECTRONICS" → "Electronics") to ensure grouping accuracy.

* **Deduplication:** Removed duplicate records based on unique identifiers like email and transaction_id.

* **Data Integrity:** Implemented strategies for missing values, such as using median imputation for prices and dropping records missing critical Foreign Keys.

**3. Load**</br>
Cleaned data is pushed into a **MySQL/PostgreSQL** database using SQLAlchemy. The load process respects the relational constraints defined in the schema, ensuring all foreign keys are valid.

## Database Schema Highlights
The database is designed in **Third Normal Form (3NF)** to ensure zero data redundancy and prevent anomalies:

* **Customers:** Stores unique profiles and contact details.

* **Products:** Stores the catalog, unit prices, and inventory levels.

* **Orders:** Captures the "Header" of the transaction (Date, Status, Total).

* **Order_Items:** Captures the "Line-Item" detail, allowing for multiple products per order.

## Business Insights
The `business_queries.sql` file provides answers to:

**1. High-Value Customers:** Identifying users who spent >₹5,000 across at least 2 orders.

**2. Category Revenue:** Discovering which product categories drive the most profit.

**3. Sales Trends:** Tracking monthly revenue and cumulative totals for the year 2024.