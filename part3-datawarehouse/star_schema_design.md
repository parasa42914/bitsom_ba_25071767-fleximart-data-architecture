# Section 1: Schema Overview
## FACT TABLE: fact_sales

**Grain:** One row per product per order line item.

**Measures:** quantity_sold, unit_price, discount_amount, total_amount.

**Foreign Keys:** date_key, product_key, customer_key.

## 
## DIMENSION TABLE: dim_date

**Purpose:** Provides a time-based context for sales.

**Attributes:** date_key (YYYYMMDD), full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend.

##
## DIMENSION TABLE: dim_product

**Purpose:** Descriptive data for all products sold.

**Attributes:** product_key (PK), product_id, product_name, category, subcategory, unit_price.

##
## DIMENSION TABLE: dim_customer

**Purpose:** Descriptive data for demographic analysis.

**Attributes:** customer_key (PK), customer_id, customer_name, city, state, customer_segment.

##
# Section 2: Design Decisions
**Granularity:** Choosing the transaction line-item level ensures maximum flexibility. It allows users to query data at the finest level of detail or aggregate it up to any level, preventing information loss that occurs with summary-level grains.

**Surrogate Keys:** We use system-generated integers (product_key) rather than business keys (product_id). This shields the warehouse from changes in source systems (e.g., if a product ID is recycled) and improves join performance due to integer indexing.

**Drill-down and Roll-up:** The hierarchical attributes in dimensions (e.g., Date -> Month -> Quarter -> Year) support drill-down (navigating from year to month for detail) and roll-up (summarizing daily sales into quarterly revenue) through simple GROUP BY operations.

##
# Section 3: Sample Data Flow
**Source:** Order #501, 2024-02-14, "Alice Smith" (ID: C10), "Sony Headphones" (ID: P99), Qty: 1, Price: 29990.

**Warehouse Fact:** fact_sales: {date_key: 20240214, product_key: 105, customer_key: 42, quantity_sold: 1, unit_price: 29990, total_amount: 29990}.

**Warehouse Dimension:** dim_product: {product_key: 105, product_id: 'P99', product_name: 'Sony Headphones', category: 'Electronics'}.