# Part 3: Data Warehouse and Analytics
## Overview
This final section shifts from operational data management to **Strategic Analytics**. By implementing a **Star Schema**, we have optimized FlexiMart’s data for high-speed analytical querying. This architecture allows the business to perform complex trend analysis, customer segmentation, and product performance tracking with minimal computational overhead.

## Files in this Section
`star_schema_design.md:`</br> Technical documentation explaining the Dimensional Modeling approach, granularity choices, and the transition from source to warehouse.

`warehouse_schema.sql:`</br> Data Definition Language (DDL) script to build the fleximart_dw database.

`warehouse_data.sql:`</br> Data Manipulation Language (DML) script containing representative sample data (40+ sales transactions) for testing.

`analytics_queries.sql:`</br> Advanced OLAP queries using Window Functions and Common Table Expressions (CTEs).

## Architectural Design
**1. The Fact Table (`fact_sales`)**</br>
The central table in our schema captures the business process of "Sales."

* **Grain:** Line-item level (one row per product per order).

* **Measures:** Quantitative data including `quantity_sold`, `unit_price`, and `total_amount`.

**2. Dimension Tables**</br>
Dimensions provide the "who, what, and when" context for every sale:

* `dim_date`: A conformed dimension allowing for time-series analysis by Day, Month, Quarter, and Year.

* `dim_product`: Contains the product hierarchy (Category > Subcategory).

* `dim_customer`: Enables demographic analysis by City and Segment.

## Analytical Capabilities
The queries implemented in this section demonstrate the following BI (Business Intelligence) capabilities:

* **Drill-Down Analysis:** Navigating from high-level yearly revenue down to specific monthly performance.

* **Market Share Analysis:** Using Window Functions to calculate a product's percentage contribution to total company revenue.

* **RFM Segmentation:** Using CASE statements to categorize customers into High, Medium, and Low-Value segments based on their total lifetime spend.

## Setup and Testing
To build the warehouse and run the analytical reports, execute the following in your SQL environment:

**1. Build Schema:**

>Bash

>mysql -u root -p < part3-datawarehouse/warehouse_schema.sql

**2. Populate Data:**

>Bash

>mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql

**3. Run Analytics:**

>Bash

>mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql