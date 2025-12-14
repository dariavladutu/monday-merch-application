-- SQLite
-- CATEGORIES
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PRODUCTS
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price_per_unit DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    sku VARCHAR(100) UNIQUE,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- USERS
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    company_name VARCHAR(255),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ORDERS
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_number VARCHAR(50) UNIQUE,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    
    -- PACKING DECISION
    packing_decision VARCHAR(20),  -- 'decide_later', 'decide_now'
    packing_type VARCHAR(20),      -- 'bulk', 'merch_packs', NULL if decide_later
    
    -- WAREHOUSING DECISION
    warehousing_decision VARCHAR(20),  -- 'decide_later', 'decide_now'
    warehousing_option VARCHAR(20),    -- 'no_warehousing', 'warehousing', NULL
    warehouse_distribution VARCHAR(20), -- 'all_to_warehouse', 'some_to_warehouse', NULL
    
    -- SHIPPING DECISION
    shipping_decision VARCHAR(20),  -- 'decide_later', 'decide_now'
    shipping_option VARCHAR(20),    -- 'one_location', 'multiple_locations', NULL
    
    -- SHIPPING ADDRESS (only if one_location)
    shipping_address_line1 VARCHAR(255),
    shipping_address_line2 VARCHAR(255),
    shipping_city VARCHAR(100),
    shipping_state VARCHAR(100),
    shipping_postal_code VARCHAR(20),
    shipping_country VARCHAR(100),
    
    -- ORDER DETAILS (end of 'Your Quote' page)
    project_type VARCHAR(50),  -- 'employee_gifts', 'onboarding', 'office_merch', 'event', 'corporate_gifts', 'christmas', 'other'
    required_delivery_date DATE,
    logo_file_url VARCHAR(500),
    notes TEXT,
    
    -- CONTACT INFO (can differ from user account)
    contact_company VARCHAR(255),
    contact_first_name VARCHAR(100),
    contact_last_name VARCHAR(100),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    
    -- PRICING
    subtotal DECIMAL(10,2) NOT NULL,
    packing_cost DECIMAL(10,2) DEFAULT 0.00,
    warehousing_cost DECIMAL(10,2) DEFAULT 0.00,
    shipping_cost DECIMAL(10,2) DEFAULT 0.00,
    total_amount DECIMAL(10,2) NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ORDER ITEMS
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_at_purchase DECIMAL(10,2) NOT NULL,
    merch_pack_number INTEGER,
    send_to_warehouse BOOLEAN DEFAULT FALSE,
    warehouse_quantity INTEGER DEFAULT 0,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- INSEERT DATA
INSERT INTO categories (name, description) VALUES
('Apparel', 'T-shirts, hoodies, and clothing'),
('Packaging', 'Boxes, Add-ons, Bags, and others'),
('Drinkware', 'Mugs, bottles, and cups');

INSERT INTO products (category_id, name, description, price_per_unit, stock_quantity, sku) VALUES
(2, 'Tissue Paper Sticker', 'A sticker designed to seal the tissue paper for elegant packaging. Fully customizable to match your brand vision. Sticker only – tissue paper not included.', 0.43, 100, 'MM-STKR-001'),
(1, 'Premium Hoodie', "A comfortable, Premium Hoodie with a modern fit. Ideal for casual branding with a twist. We'll help create the perfect design for your brand.", 47.85, 50, 'MM-HOOD-001'),
(1, 'Trucker Cap', "This Premium Trucker Cap is a must-have for a casual vibe. Ready for your logo or design, it's perfect for showing off your swag. Our team is ready to assist in making your design vision a reality.", 9.95, 75, 'MM-CAP-001'),
(3, 'Ceramic Compact Mug', "A ceramic compact Mug made for sipping your favorite drinks. It's a great canvas for showcasing your brand. Our team is ready to help you bring your ideas to life.", 6.32, 200, 'MM-MUG-001');

INSERT INTO users (email, password_hash, first_name, last_name, company_name, phone) VALUES
('john.doe@example.com', '$2b$10$hashedpassword123', 'John', 'Doe', 'TechCorp B.V.', '555-0100'),
('jane.smith@example.com', '$2b$10$hashedpassword456', 'Jane', 'Smith', 'StartupXYZ', '555-0200');

INSERT INTO orders (
    user_id, order_number, status,
    packing_decision, packing_type,
    warehousing_decision, warehousing_option,
    shipping_decision, shipping_option,
    shipping_address_line1, shipping_city, shipping_postal_code, shipping_country,
    project_type, required_delivery_date,
    contact_company, contact_first_name, contact_last_name, contact_email, contact_phone,
    subtotal, total_amount
) VALUES 
(1, 'MM-2024-0001', 'completed',
'decide_now', 'bulk',
'decide_now', 'no_warehousing',
'decide_now', 'one_location',
'Paralellweg 123', 'Amsterdam', '2678NT', 'NL',
'employee_gifts', '2025-01-15',
'TechCorp B.V.', 'John', 'Doe', 'john.doe@example.com', '555-0100',
7.18, 7.18),
(2, 'MM-2024-0002', 'pending',
'decide_later', NULL,
'decide_later', NULL,
'decide_later', NULL,
'Kirklaan 2', 'Den Haag', '7890PL', 'NL',
'onboarding', '2025-02-01',
'StartupXYZ', 'Jane', 'Smith', 'jane.smith@example.com', '555-0200',
10.38, 10.38);

INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES
(1, 1, 2, 0.43),
(1, 4, 1, 6.32),
(2, 3, 1, 9.95),
(2, 1, 1, 0.43);

SELECT * FROM categories;
SELECT * FROM products;
SELECT * FROM users;
SELECT * FROM orders;
SELECT * FROM order_items;


-- VALIDATION
SELECT * FROM products 
WHERE category_id = 1;

-- Find John's order total
SELECT SUM(total_amount) AS total_spent
FROM orders
WHERE user_id = 1;

-- See what items are in order #1
SELECT 
    products.name,
    order_items.quantity,
    order_items.price_at_purchase
FROM order_items
JOIN products ON order_items.product_id = products.id
WHERE order_items.order_id = 1;

-- Find best-selling product
SELECT 
    products.name,
    SUM(order_items.quantity) AS total_sold
FROM order_items
JOIN products ON order_items.product_id = products.id
GROUP BY products.id
ORDER BY total_sold DESC
LIMIT 1;