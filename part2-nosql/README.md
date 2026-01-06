# Part 2: NoSQL Product Catalog Analysis
## Overview
This section focuses on the transition from a rigid relational schema to a flexible NoSQL document store. As FlexiMart expands into diverse product categories (Electronics, Fashion, etc.), the data requirements evolve to include nested reviews and varied product specifications.

## Files in this Section
`nosql_analysis.md:`</br> A theoretical report justifying the move to MongoDB, discussing RDBMS limitations, and identifying architectural trade-offs.

`products_catalog.json:`</br> A sample dataset containing highly diverse products with nested specifications and review arrays.

`mongodb_operations.js:`</br> A comprehensive script containing 5 key MongoDB operations, including complex aggregation pipelines and atomic updates.

## Key Features Implemented
**1. Flexible Schema Design : </br>**
Unlike the MySQL schema in Part 1, the MongoDB collection allows for "Polymorphic" data.

**Electronics** include fields like processor and ram.

**Fashion** items include material, fit, and sizes_available. Both exist in the same products collection without requiring NULL-heavy columns.

**2. Embedded Document Model : </br>**
Reviews are stored directly within the product document.

* Benefit: Retrieves product details and all 20+ reviews in a single I/O operation.

* Implementation: Used the $unwind and $group aggregation stages to calculate real-time average ratings from these nested arrays.

**3. Advanced Aggregation : </br>**
The implementation includes a Category Performance Report that calculates:

* Average price per category.

* Total stock volume.

* Product count per category.

## Setup and Execution
**Prerequisites </br>**
* MongoDB Server (Community Edition)

* MongoDB Shell (mongosh)</br></br>

**Importing Data </br>**
To import the provided JSON catalog into your local MongoDB instance:

>Bash

>mongoimport --db fleximart --collection products --file products_catalog.json --jsonArray</br>

**Running Operations </br>**
To execute the query and aggregation scripts:

>Bash

>mongosh fleximart mongodb_operations.js

## Business Insights Generated
The scripts in this section provide the following insights for FlexiMart:

**1. Affordability Filter:** Identifies mid-range electronics (under ₹50,000) for targeted marketing.

**2. Quality Control:** Identifies top-rated products (Avg > 4.0) to feature on the homepage.

**3. Inventory Health:** Summarizes stock distribution across diverse categories.