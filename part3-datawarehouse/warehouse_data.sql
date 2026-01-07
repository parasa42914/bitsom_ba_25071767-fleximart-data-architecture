-- Insert Sample Dates
INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend) VALUES
(20240101, '2024-01-01', 'Monday', 1, 1, 'January', 'Q1', 2024, FALSE),
(20240106, '2024-01-06', 'Saturday', 6, 1, 'January', 'Q1', 2024, TRUE),
(20240214, '2024-02-14', 'Wednesday', 14, 2, 'February', 'Q1', 2024, FALSE);

-- Insert Sample Products
INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
('ELEC001', 'Samsung Galaxy S21 Ultra', 'Electronics', 'Smartphones', 79999.00),
('ELEC002', 'Apple MacBook Pro', 'Electronics', 'Laptops', 189999.00),
('FASH001', 'Levis 511 Jeans', 'Fashion', 'Clothing', 3499.00);

-- Insert Sample Customers
INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
('C001', 'John Doe', 'Mumbai', 'Maharashtra', 'Corporate'),
('C002', 'Jane Smith', 'Bangalore', 'Karnataka', 'Consumer');

-- Insert Sample Fact Sales
INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, total_amount) VALUES
(20240101, 1, 1, 1, 79999.00, 79999.00),
(20240106, 2, 2, 1, 189999.00, 189999.00),
(20240214, 3, 1, 2, 3499.00, 6998.00);