"""
Monday Merch API - FastAPI Application
Products endpoint with search, filtering, and pagination
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import sqlite3
from contextlib import contextmanager

app = FastAPI(
    title="Monday Merch API",
    description="API for Monday Merch ecommerce platform",
    version="1.0.0"
)


# DATABASE CONNECTION
DATABASE_PATH = "monday_merch.db"

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


# PYDANTIC MODELS
class Product(BaseModel):
    """Product response model"""
    id: int
    category_id: int
    name: str
    description: Optional[str] = None
    price_per_unit: float
    stock_quantity: int
    sku: Optional[str] = None
    image_url: Optional[str] = None
    created_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "category_id": 2,
                "name": "Tissue Paper Sticker",
                "description": "A sticker designed to seal the tissue paper for elegant packaging.",
                "price_per_unit": 0.43,
                "stock_quantity": 100,
                "sku": "MM-STKR-001",
                "image_url": None,
                "created_at": "2024-12-13 10:00:00"
            }
        }

class ProductsResponse(BaseModel):
    """Response model for products list"""
    total: int
    page: int
    page_size: int
    products: List[Product]


# API ENDPOINTS
@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Monday Merch API",
        "version": "1.0.0",
        "endpoints": {
            "products": "/products",
            "docs": "/docs"
        }
    }

@app.get("/products", response_model=ProductsResponse)
def get_products(
    search: Optional[str] = Query(None, description="Search in product name or description"),
    category: Optional[int] = Query(None, description="Filter by category ID"),
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page")
):
    """
    Get products with optional filtering and pagination
    
    **Query Parameters:**
    - **search**: Search term for product name or description
    - **category**: Filter by category ID (1=Apparel, 2=Packaging, 3=Drinkware)
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 100)
    
    **Returns:**
    - List of products matching the criteria
    - Total count of matching products
    - Pagination information
    """
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Build the query dynamically based on parameters
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        
        # Add search filter
        if search:
            query += " AND (name LIKE ? OR description LIKE ?)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term])
        
        # Add category filter
        if category:
            query += " AND category_id = ?"
            params.append(category)
        
        # Get total count (before pagination)
        count_query = f"SELECT COUNT(*) as total FROM ({query})"
        total = cursor.execute(count_query, params).fetchone()["total"]
        
        # Add pagination
        offset = (page - 1) * page_size
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([page_size, offset])
        
        # Execute query
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Convert to Product models
        products = [
            Product(
                id=row["id"],
                category_id=row["category_id"],
                name=row["name"],
                description=row["description"],
                price_per_unit=float(row["price_per_unit"]),
                stock_quantity=row["stock_quantity"],
                sku=row["sku"],
                image_url=row["image_url"],
                created_at=row["created_at"]
            )
            for row in rows
        ]
        
        return ProductsResponse(
            total=total,
            page=page,
            page_size=page_size,
            products=products
        )

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    """
    Get a single product by ID
    
    **Path Parameters:**
    - **product_id**: The ID of the product to retrieve
    
    **Returns:**
    - Product details
    
    **Raises:**
    - 404: Product not found
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return Product(
            id=row["id"],
            category_id=row["category_id"],
            name=row["name"],
            description=row["description"],
            price_per_unit=float(row["price_per_unit"]),
            stock_quantity=row["stock_quantity"],
            sku=row["sku"],
            image_url=row["image_url"],
            created_at=row["created_at"]
        )

@app.get("/categories")
def get_categories():
    """
    Get all product categories
    
    **Returns:**
    - List of all categories with product counts
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                c.id,
                c.name,
                c.description,
                COUNT(p.id) as product_count
            FROM categories c
            LEFT JOIN products p ON c.id = p.category_id
            GROUP BY c.id
            ORDER BY c.id
        """)
        rows = cursor.fetchall()
        
        categories = [
            {
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "product_count": row["product_count"]
            }
            for row in rows
        ]
        
        return {"categories": categories}


# HEALTH CHECK
@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM products")
            count = cursor.fetchone()["count"]
        
        return {
            "status": "healthy",
            "database": "connected",
            "products_count": count
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)