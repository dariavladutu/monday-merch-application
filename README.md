# Monday Merch API

RESTful API for Monday Merch ecommerce platform built with FastAPI.

## Features

- **GET /products** endpoint with filtering and pagination
- Search products by name or description
- Filter products by category
- Pagination support
- SQLite database backend
- Full API documentation (Swagger/OpenAPI)

## Tech Stack
- **Framework**: FastAPI 0.104.1
- **Database**: SQLite3
- **Validation**: Pydantic 2.5.0
- **Server**: Uvicorn 0.24.0
- **Language**: Python 3.11+

## Setup Instructions

###
 Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- clone repository (or download files)
  ```bash
  git clone https://github.com/dariavladutu/monday-merch-application.git
  cd monday-merch-application
   ```

Recommended (but not required)
- cretae a virtual environment (best practice for keeping everything neat and organised):
   ```bash
   python3 -m venv venv
   source venv\Scripts\activate
   ```
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

1. categories -> products (one-to-many)
   - One category can have many products
   - Each product belongs to one category

2. users -> orders (one-to-many)
   - One user can place many orders
   - Each order belongs to one user

3. orders <-> products (many-to-many via order_items)
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

## Future Improvements

### High Priority (Production Requirements)

1.**Authentication & Authorization**
- Authentication
- Role-based access control (admin, customer)
- Password hashing 

2.**Input Validation**
- String length limits on search queries
- Email format validation
- Price range validation

3.**Comprehensive Error Handling**
- Structured logging (logging module)
- Error tracking (Sentry)
- Request ID tracking
- User-friendly error messages

4.**Testing**
- Unit tests with pytest
- Integration tests
- API endpoint tests

5.**Database Migration**
- PostgreSQL for production
- Connection pooling
- Database indexes on frequently queried fields

### Medium Priority

6.**Docker Containerization**

7.**CI/CD Pipeline**
- GitHub Actions
- Automated testing
- Code quality checks (black, flake8)
- Automated deployment

### Long-term Improvements

10.**Monitoring & Observability**

## Project Structure

```
monday_merch_api/
├── main.py              # FastAPI application
├── init_db.py           # Database initialization
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── monday_merch.db     # SQLite database (created by init_db.py)
```

## License

Created for graduation project - Monday Merch API

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Install dependencies with `pip install -r requirements.txt`

### Issue: `Database is locked`
**Solution**: Close any SQLite browser connections and restart the server

### Issue: `Address already in use`
**Solution**: Kill the process on port 8000 or use a different port:
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8080
```

### Issue: `Database not found`
**Solution**: Run `python init_db.py` to create the database

### Issue: `Port 8000 shows "Connection refused"`
**Solution**: Make sure the server is running with `uvicorn main:app --reload`