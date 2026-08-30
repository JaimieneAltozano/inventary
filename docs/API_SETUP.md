# API Server Setup Guide

## Overview
The inventory application now includes a built-in API server that provides pre-configured products that can be imported into your local inventory database.

## Prerequisites

You need to install Flask and requests:

```bash
pip install flask requests
```

## Running the API Server

### Step 1: Open a terminal in the project directory

Navigate to the folder containing `api_server.py`:

```bash
cd c:\Users\violy\OneDrive\Desktop\M5\prueba
```

### Step 2: Start the API server

```bash
python api_server.py
```

You should see output like:

```
============================================================
Product Inventory API Server
============================================================
Starting server on http://localhost:5000
API endpoint: http://localhost:5000/api/products
Available products: 10

Endpoints:
  GET /api/products          - Get all products
  GET /api/products/<id>     - Get specific product
  GET /api/health            - Health check
  GET /                      - API documentation

Press CTRL+C to stop the server
============================================================
```

### Step 3: Keep this terminal open

The API server must be running while you use the main application.

## Using the API in the Application

### Running the main application

Open another terminal and run:

```bash
python main.py
```

### Importing products from API

In the main menu, choose option **5. Import from API**

```
Menu:
0. Exit
1. Product register
2. Find product
3. Filter products
4. Show product list
5. Import from API

Option: 5
```

You'll be prompted to enter the API URL. Press Enter to use the default:
- Default URL: `http://localhost:5000/api/products`

The application will:
1. Connect to the API server
2. Fetch all available products
3. Import them into your local inventory
4. Display the number of products successfully imported

## Available Products in the API

The API server comes with 10 pre-configured products:

| ID | Name | Price | Stock | Status |
|---|---|---|---|---|
| DELL-001 | Laptop Dell XPS 15 | $1299.99 | 15 | active |
| LOG-001 | Mouse Logitech MX | $99.99 | 45 | active |
| KEY-001 | Keyboard Mechanical RGB | $159.99 | 32 | active |
| MON-001 | Monitor LG 27 inch | $349.99 | 8 | active |
| CABLE-001 | USB-C Cable | $19.99 | 120 | active |
| WEB-001 | Webcam Logitech C920 | $79.99 | 25 | inactive |
| SSD-001 | External SSD 1TB | $129.99 | 18 | active |
| HEAD-001 | Wireless Headphones | $199.99 | 12 | active |
| HUB-001 | USB Hub 7 Ports | $49.99 | 35 | active |
| STAND-001 | Laptop Stand | $39.99 | 42 | active |

## API Endpoints

### 1. Get All Products
```
GET http://localhost:5000/api/products
```

Returns all products in JSON format.

### 2. Get Specific Product
```
GET http://localhost:5000/api/products/DELL-001
```

Replace `DELL-001` with any product ID.

### 3. Health Check
```
GET http://localhost:5000/api/health
```

Returns server status and product count.

### 4. API Documentation
```
GET http://localhost:5000/
```

Returns API documentation and usage examples.

## Testing with cURL (Command Line)

If you have cURL installed, you can test the API:

```bash
# Get all products
curl http://localhost:5000/api/products

# Get specific product
curl http://localhost:5000/api/products/DELL-001

# Health check
curl http://localhost:5000/api/health
```

## Troubleshooting

### "Could not connect to API"
- Make sure the API server is running in another terminal
- Verify the URL is correct: `http://localhost:5000/api/products`
- Check that port 5000 is not in use by another application

### "requests library is required"
Install requests:
```bash
pip install requests
```

### "API response is not a list"
Check that you're using the correct API endpoint: `/api/products` (not other endpoints)

## Next Steps

After importing products:
1. Search for imported products (option 2)
2. Filter products (option 3)
3. Update or delete products as needed
4. Later, this data will be connected to a database for persistent storage

## Notes

- The API server stores products in memory only. Restarting the server won't affect your local inventory.
- Your local inventory (in the main.py application) is separate from the API.
- In the future, you can connect this to a real database (PostgreSQL, MySQL, etc.)
