# Entity-Relationship Description

## ENTITY: customers

**Purpose:** Stores profile and contact details for registered users.

**Attributes:** customer_id (PK), first_name, last_name, email (Unique), phone, city, registration_date.

**Relationships:** 1:M with orders.


## ENTITY: products

**Purpose:** Catalog of items available for sale.

**Attributes:** product_id (PK), product_name, category, price, stock_quantity.

**Relationships:** 1:M with order_items.


## ENTITY: orders

**Purpose:** Records the header information of a transaction.

**Attributes:** order_id (PK), customer_id (FK), order_date, total_amount, status.

**Relationships:** M:1 with customers, 1:M with order_items.


## ENTITY: order_items

**Purpose:** Line-item details for each product within an order.

**Attributes:** order_item_id (PK), order_id (FK), product_id (FK), quantity, unit_price, subtotal.

##
##
# Normalization Explanation (3NF)
This design adheres to the **Third Normal Form (3NF)** for the following reasons:

1. **1NF:** All attributes contain atomic values, and each record is unique via Primary Keys.

2. **2NF:** Every non-key attribute is fully functionally dependent on the primary key. For example, in order_items, the unit_price at the time of sale is dependent on that specific line item, not just the product (to account for historical price changes).

3. **3NF:** There are no transitive dependencies. The city depends on the customer_id, and category depends on the product_id. No non-prime attribute depends on another non-prime attribute.


## Anomalies Avoided:

**Insert Anomaly:** We can add a new customer without them having to make an order immediately.

**Update Anomaly:** Changing a product name only requires an update in one place (products table) rather than every sales record.

**Delete Anomaly:** Deleting an order item does not result in losing the customer’s profile information.