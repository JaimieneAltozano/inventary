# Inventory

A Python program for managing a product inventory with SQLite database support. Users can register, search, update, and delete products with complete information tracking.

## Description

The program displays an interactive menu in the console that allows users to manage their inventory efficiently. Each product stores detailed information including name, ID, price, stock quantity, and status (active/inactive).

All data is persisted using SQLite, providing a lightweight but reliable database solution.

## Features

- **Product Registration**: Add one or more products with complete details
- **Product Search**: Find products by ID or name with filtering capabilities
- **Product Update**: Modify product details (name, ID, price, stock, status)
- **Product Deletion**: Remove products from inventory
- **Product Filtering**: Filter products by status (active/inactive) or stock range
- **Product List**: Display all registered products
- **API Import**: Import products from an external REST API
- **Database Persistence**: All data is stored in SQLite database
- **Data Validation**: Ensures data integrity (active/inactive status validation)

## Technology Stack

- **Language**: Python 3.7+
- **Database**: SQLite 3
- **API Framework**: Flask (for API server)
- **HTTP Client**: Requests (for API integration)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or navigate to the project directory:
```bash
cd c:\Users\violy\OneDrive\Desktop\M5\prueba
```

2. Install required dependencies:
```bash
pip install flask requests
```

3. The SQLite database will be created automatically on first run.

## Database Structure

The application uses SQLite with the following schema:

```sql
CREATE TABLE products (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    statement TEXT NOT NULL CHECK(statement IN ('active', 'inactive')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Usage

### Running the Main Application

```bash
python main.py
```

### Menu Options

```
Menu:
0. Exit
1. Product register          - Add new products to inventory
2. Find product              - Search by ID or name and manage
3. Filter products           - Filter by status or stock range
4. Show product list         - Display all products
5. Import from API           - Sync products from external API
```

### Product Attributes

Each product contains:
- **Name**: Product name
- **ID**: Unique product identifier (primary key)
- **Prize**: Product price (decimal)
- **Stock**: Quantity available (integer)
- **Statement**: Status - must be 'active' or 'inactive'

### Running the API Server

To import products from the external API:

```bash
python api_server.py
```

Then in the main application, select option 5 to import products.

## Example Workflow

```
Menu:
0. Exit
1. Product register
2. Find product
3. Filter products
4. Show product list
5. Import from API

Option: 1
Quantity products: 1

Name product: Laptop Dell XPS 15
ID product: DELL-001
Prize product: 1299.99
Stock product: 15
Statement product (active/inactive): active

Show the register?
1. Yes
2. No
Yes

[{'Name': 'Laptop Dell XPS 15', 'ID': 'DELL-001', 'Prize': '1299.99', 'Stock': '15', 'Statement': 'active'}]
```

## Data Persistence

- All products are stored in `inventory.db` (SQLite database)
- Data persists between application sessions
- Database is automatically created on first run
- No manual setup required

## Architecture Overview

### Current Structure
```
main.py           - CLI interface and user interaction
functions.py      - Business logic and database operations
api_server.py     - REST API server for product import
```

## Technologies Used

- **Python 3**: Core language
- **SQLite**: Database
- **Flask**: Web framework for API
- **Requests**: HTTP library for API calls

## Notes

- Data validation ensures only 'active' or 'inactive' values are accepted for product status
- All product IDs must be unique
- Price and stock values are validated as numeric
- The database file is stored locally and can be backed up
Statement product (active/inactive): active

Name product: Chicken
ID product: 002
Prize product: 3.00
Stock product: 15
Statement product (active/inactive): active
```

## Technologies Used

- Python 3
