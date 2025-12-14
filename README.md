# Monday Merch API

RESTful API for Monday Merch ecommerce platform built with FastAPI.

## Features

- ✅ **GET /products** endpoint with filtering and pagination
- ✅ Search products by name or description
- ✅ Filter products by category
- ✅ Pagination support
- ✅ SQLite database backend
- ✅ Full API documentation (Swagger/OpenAPI)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python init_db.py
```

This creates `monday_merch.db` with:
- 3 categories (Apparel, Packaging, Drinkware)
- 4 products from Monday Merch
- 2 sample users
- 2 sample orders

### 3. Run the API

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### Root
- **GET /** - API information

### Products
- **GET /products** - Get all products with optional filtering
  - Query parameters:
    - `search` - Search in product name/description
    - `category` - Filter by category ID
    - `page` - Page number (default: 1)
    - `page_size` - Items per page (default: 10, max: 100)

- **GET /products/{product_id}** - Get single product by ID

### Categories
- **GET /categories** - Get all categories with product counts

### Health
- **GET /health** - Health check endpoint

## Example API Calls

### Get all products
```bash
curl http://localhost:8000/products
```

### Search for "hoodie"
```bash
curl "http://localhost:8000/products?search=hoodie"
```

### Get products in category 1 (Apparel)
```bash
curl "http://localhost:8000/products?category=1"
```

### Get page 2 with 5 items per page
```bash
curl "http://localhost:8000/products?page=2&page_size=5"
```

### Get single product
```bash
curl http://localhost:8000/products/1
```

### Get all categories
```bash
curl http://localhost:8000/categories
```

## Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Schema

### Products Table
```sql
- id (PRIMARY KEY)
- category_id (FOREIGN KEY → categories)
- name
- description
- price_per_unit
- stock_quantity
- sku (UNIQUE)
- image_url
- created_at
```

### Categories Table
```sql
- id (PRIMARY KEY)
- name
- description
- created_at
```

### Users Table
```sql
- id (PRIMARY KEY)
- email (UNIQUE)
- password_hash
- first_name
- last_name
- company_name
- phone
- created_at
```

### Orders Table
```sql
- id (PRIMARY KEY)
- user_id (FOREIGN KEY → users)
- order_number (UNIQUE)
- status
- packing_decision
- packing_type
- warehousing_decision
- warehousing_option
- shipping_decision
- shipping_option
- shipping_address_*
- project_type
- required_delivery_date
- contact_*
- subtotal
- total_amount
```

### Order Items Table (Junction)
```sql
- id (PRIMARY KEY)
- order_id (FOREIGN KEY → orders)
- product_id (FOREIGN KEY → products)
- quantity
- price_at_purchase
- merch_pack_number
- send_to_warehouse
- warehouse_quantity
```

RELATIONSHIPS:

1. categories → products (one-to-many)
   - One category can have many products
   - Each product belongs to one category

2. users → orders (one-to-many)
   - One user can place many orders
   - Each order belongs to one user

3. orders ↔ products (many-to-many via order_items)
   - One order can contain many products
   - One product can appear in many orders
   - Junction table: order_items

## Design Decisions

### 1. Database Choice: SQLite
- **Why**: Simple, no server setup needed, perfect for development/assignment
- **Production alternative**: PostgreSQL or MySQL

### 2. Pagination
- **Why**: Essential for large product catalogs, improves performance
- **Implementation**: LIMIT/OFFSET with total count

### 3. Search Functionality
- **Why**: Users need to find products quickly
- **Implementation**: SQL LIKE queries on name and description
- **Production improvement**: Full-text search index

### 4. Category Filtering
- **Why**: Users browse by product type
- **Implementation**: Simple WHERE clause on category_id

### 5. Price Field: `price_per_unit`
- **Why**: Monday Merch shows unit pricing on website
- **Matches**: Real product data from Monday Merch

## Response Format

### Products List Response
```json
{
  "total": 4,
  "page": 1,
  "page_size": 10,
  "products": [
    {
      "id": 1,
      "category_id": 2,
      "name": "Tissue Paper Sticker",
      "description": "A sticker designed to seal...",
      "price_per_unit": 0.43,
      "stock_quantity": 100,
      "sku": "MM-STKR-001",
      "image_url": null,
      "created_at": "2024-12-13 10:00:00"
    }
  ]
}
```

## For Production System

To make this production-ready, you'd add:

### Security
- ✅ API key authentication
- ✅ Rate limiting
- ✅ HTTPS/TLS encryption
- ✅ Input validation and sanitization
- ✅ SQL injection prevention (using parameterized queries ✅)

### Features
- ✅ Full CRUD operations (POST, PUT, DELETE)
- ✅ Order management endpoints
- ✅ User authentication/authorization
- ✅ Image upload handling
- ✅ Payment processing integration
- ✅ Email notifications
- ✅ Inventory management

### Performance
- ✅ Database connection pooling
- ✅ Caching (Redis)
- ✅ Full-text search indexing
- ✅ Query optimization
- ✅ Load balancing

### Monitoring
- ✅ Logging (structured logging)
- ✅ Error tracking (Sentry)
- ✅ Performance monitoring (APM)
- ✅ Health checks
- ✅ Metrics (Prometheus)

### Testing
- ✅ Unit tests
- ✅ Integration tests
- ✅ Load testing
- ✅ API contract testing

## Project Structure

```
monday_merch_api/
├── main.py              # FastAPI application
├── init_db.py           # Database initialization
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── monday_merch.db     # SQLite database (created by init_db.py)
```

## Assignment Completion

This implementation fulfills the B2 requirements:

✅ **GET /products endpoint** - Implemented with full functionality
✅ **Returns product list** - From SQLite database schema
✅ **Query parameters** - search, category, page, page_size
✅ **Real database** - SQLite with proper schema
✅ **Clear schema** - All 5 required tables with relationships
✅ **Documentation** - This README + Swagger docs

## License

Created for graduation project - Monday Merch API
