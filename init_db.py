import sqlite3

DATABASE_PATH = "monday_merch.db"

def init_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS order_items")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS categories")
    
    # Create categories table
    cursor.execute("""
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create products table
    cursor.execute("""
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
        )
    """)
    
    # Create users table
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            company_name VARCHAR(255),
            phone VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_number VARCHAR(50) UNIQUE,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50) DEFAULT 'pending',
            packing_decision VARCHAR(20),
            packing_type VARCHAR(20),
            warehousing_decision VARCHAR(20),
            warehousing_option VARCHAR(20),
            warehouse_distribution VARCHAR(20),
            shipping_decision VARCHAR(20),
            shipping_option VARCHAR(20),
            shipping_address_line1 VARCHAR(255),
            shipping_address_line2 VARCHAR(255),
            shipping_city VARCHAR(100),
            shipping_state VARCHAR(100),
            shipping_postal_code VARCHAR(20),
            shipping_country VARCHAR(100),
            project_type VARCHAR(50),
            required_delivery_date DATE,
            logo_file_url VARCHAR(500),
            notes TEXT,
            contact_company VARCHAR(255),
            contact_first_name VARCHAR(100),
            contact_last_name VARCHAR(100),
            contact_email VARCHAR(255),
            contact_phone VARCHAR(20),
            subtotal DECIMAL(10,2) NOT NULL DEFAULT 0.00,
            packing_cost DECIMAL(10,2) DEFAULT 0.00,
            warehousing_cost DECIMAL(10,2) DEFAULT 0.00,
            shipping_cost DECIMAL(10,2) DEFAULT 0.00,
            total_amount DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Create order_items table
    cursor.execute("""
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
        )
    """)
    
    # Insert categories
    cursor.execute("INSERT INTO categories (name, description) VALUES ('Apparel', 'T-shirts, hoodies, and clothing')")
    cursor.execute("INSERT INTO categories (name, description) VALUES ('Packaging', 'Boxes, Add-ons, Bags, and others')")
    cursor.execute("INSERT INTO categories (name, description) VALUES ('Drinkware', 'Mugs, bottles, and cups')")
    
    # Insert products - one by one to avoid syntax issues
    cursor.execute("""
        INSERT INTO products (category_id, name, description, price_per_unit, stock_quantity, sku)
        VALUES (2, 'Tissue Paper Sticker', 'A sticker designed to seal the tissue paper for elegant packaging. Fully customizable to match your brand vision. Sticker only – tissue paper not included.', 0.43, 100, 'MM-STKR-001')
    """)
    
    hoodie_qty = 50
    cursor.execute("""
        INSERT INTO products (category_id, name, description, price_per_unit, stock_quantity, sku)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (1, 'Premium Hoodie', 'A comfortable, Premium Hoodie with a modern fit. Ideal for casual branding with a twist. We will help create the perfect design for your brand.', 47.85, hoodie_qty, 'MM-HOOD-001'))
    
    cursor.execute("""
        INSERT INTO products (category_id, name, description, price_per_unit, stock_quantity, sku)
        VALUES (1, 'Trucker Cap', 'This Premium Trucker Cap is a must-have for a casual vibe. Ready for your logo or design, it is perfect for showing off your swag. Our team is ready to assist in making your design vision a reality.', 9.95, 75, 'MM-CAP-001')
    """)
    
    cursor.execute("""
        INSERT INTO products (category_id, name, description, price_per_unit, stock_quantity, sku)
        VALUES (3, 'Ceramic Compact Mug', 'A ceramic compact Mug made for sipping your favorite drinks. It is a great canvas for showcasing your brand. Our team is ready to help you bring your ideas to life.', 6.32, 200, 'MM-MUG-001')
    """)
    
    # Insert users
    cursor.execute("""
        INSERT INTO users (email, password_hash, first_name, last_name, company_name, phone)
        VALUES ('john.doe@example.com', '$2b$10$hashedpassword123', 'John', 'Doe', 'TechCorp B.V.', '+31-555-0100')
    """)
    
    cursor.execute("""
        INSERT INTO users (email, password_hash, first_name, last_name, company_name, phone)
        VALUES ('jane.smith@example.com', '$2b$10$hashedpassword456', 'Jane', 'Smith', 'StartupXYZ', '+31-555-0200')
    """)
    
    # Insert orders
    cursor.execute("""
        INSERT INTO orders (
            user_id, order_number, status, packing_decision, packing_type,
            warehousing_decision, warehousing_option, shipping_decision, shipping_option,
            shipping_address_line1, shipping_city, shipping_postal_code, shipping_country,
            project_type, required_delivery_date, contact_company, contact_first_name,
            contact_last_name, contact_email, contact_phone, subtotal, total_amount
        )
        VALUES (1, 'MM-2024-0001', 'completed', 'decide_now', 'bulk', 'decide_now', 'no_warehousing',
                'decide_now', 'one_location', 'Paralellweg 123', 'Amsterdam', '2678NT', 'NL',
                'employee_gifts', '2025-01-15', 'TechCorp B.V.', 'John', 'Doe',
                'john.doe@example.com', '+31-555-0100', 7.18, 7.18)
    """)
    
    cursor.execute("""
        INSERT INTO orders (
            user_id, order_number, status, packing_decision, warehousing_decision, shipping_decision,
            shipping_address_line1, shipping_city, shipping_postal_code, shipping_country,
            project_type, required_delivery_date, contact_company, contact_first_name,
            contact_last_name, contact_email, contact_phone, subtotal, total_amount
        )
        VALUES (2, 'MM-2024-0002', 'pending', 'decide_later', 'decide_later', 'decide_later',
                'Kirklaan 2', 'Den Haag', '7890PL', 'NL', 'onboarding', '2025-02-01',
                'StartupXYZ', 'Jane', 'Smith', 'jane.smith@example.com', '+31-555-0200',
                10.38, 10.38)
    """)
    
    # Insert order items
    cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (1, 1, 2, 0.43)")
    cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (1, 4, 1, 6.32)")
    cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (2, 3, 1, 9.95)")
    cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (2, 1, 1, 0.43)")
    
    conn.commit()
    conn.close()
    
    print("Database initialized successfully!")
    print(f"Database location: {DATABASE_PATH}")
    print("\nSummary:")
    print("  - 3 categories")
    print("  - 4 products")
    print("  - 2 users")
    print("  - 2 orders")
    print("  - 4 order items")

if __name__ == "__main__":
    init_database()