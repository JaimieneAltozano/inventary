"""
Simple API server for product inventory
Run with: python api_server.py
Access at: http://localhost:5000/api/products
"""

from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

# Preconfigured products in the API
PRODUCTS_DATABASE = [
    {
        "name": "Laptop Dell XPS 15",
        "id": "DELL-001",
        "prize": "1299.99",
        "stock": "15",
        "statement": "active"
    },
    {
        "name": "Mouse Logitech MX",
        "id": "LOG-001",
        "prize": "99.99",
        "stock": "45",
        "statement": "active"
    },
    {
        "name": "Keyboard Mechanical RGB",
        "id": "KEY-001",
        "prize": "159.99",
        "stock": "32",
        "statement": "active"
    },
    {
        "name": "Monitor LG 27 inch",
        "id": "MON-001",
        "prize": "349.99",
        "stock": "8",
        "statement": "active"
    },
    {
        "name": "USB-C Cable",
        "id": "CABLE-001",
        "prize": "19.99",
        "stock": "120",
        "statement": "active"
    },
    {
        "name": "Webcam Logitech C920",
        "id": "WEB-001",
        "prize": "79.99",
        "stock": "25",
        "statement": "inactive"
    },
    {
        "name": "External SSD 1TB",
        "id": "SSD-001",
        "prize": "129.99",
        "stock": "18",
        "statement": "active"
    },
    {
        "name": "Wireless Headphones",
        "id": "HEAD-001",
        "prize": "199.99",
        "stock": "12",
        "statement": "active"
    },
    {
        "name": "USB Hub 7 Ports",
        "id": "HUB-001",
        "prize": "49.99",
        "stock": "35",
        "statement": "active"
    },
    {
        "name": "Laptop Stand",
        "id": "STAND-001",
        "prize": "39.99",
        "stock": "42",
        "statement": "active"
    }
]


@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products from the API"""
    return jsonify(PRODUCTS_DATABASE)


@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    for product in PRODUCTS_DATABASE:
        if product["id"] == product_id:
            return jsonify(product)
    return jsonify({"error": "Product not found"}), 404


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "products_count": len(PRODUCTS_DATABASE)
    })


@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        "message": "Product Inventory API Server",
        "version": "1.0",
        "endpoints": {
            "GET /api/products": "Get all products",
            "GET /api/products/<id>": "Get specific product by ID",
            "GET /api/health": "Health check",
            "GET /": "This help message"
        },
        "example_usage": {
            "get_all": "curl http://localhost:5000/api/products",
            "get_one": "curl http://localhost:5000/api/products/DELL-001",
            "sync_in_app": "Choose option 5 in the main menu after starting the app"
        }
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Product Inventory API Server")
    print("=" * 60)
    print(f"Starting server on http://localhost:5000")
    print(f"API endpoint: http://localhost:5000/api/products")
    print(f"Available products: {len(PRODUCTS_DATABASE)}")
    print("\nEndpoints:")
    print("  GET /api/products          - Get all products")
    print("  GET /api/products/<id>     - Get specific product")
    print("  GET /api/health            - Health check")
    print("  GET /                      - API documentation")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60)
    
    app.run(debug=False, host='localhost', port=5000)
