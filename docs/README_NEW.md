# Inventory Management System

A professional Python application for managing product inventory with **SQLite database** support. Users can register, search, update, and delete products with complete information tracking. Now available in both simple and **production-ready scalable architecture** versions.

## 🌟 Features

- **Product Registration**: Add one or more products with complete validation
- **Product Search**: Find products by ID or name with intelligent filtering
- **Product Update**: Modify product details with automatic timestamp tracking
- **Product Deletion**: Remove products from inventory
- **Advanced Filtering**: Filter by status (active/inactive) or stock range
- **Product List**: Display all products with inventory statistics
- **API Integration**: Import products from external REST API
- **Database Persistence**: SQLite with automatic schema creation
- **Data Validation**: Comprehensive validation (active/inactive status, numeric checks)
- **Professional Architecture**: Modular, testable, enterprise-ready codebase

## 📦 Technology Stack

- **Language**: Python 3.7+
- **Database**: SQLite 3 (local, file-based, no server required)
- **API Framework**: Flask 2.3.3+
- **HTTP Client**: Requests 2.31.0+
- **Architecture Pattern**: Clean Architecture + Repository Pattern

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Navigate to the project directory:
```bash
cd c:\Users\violy\OneDrive\Desktop\M5\prueba
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Simple Version (Original)
```bash
python main.py
```
- ✓ Easy to understand
- ✓ Good for learning
- ✗ Data stored in memory (lost on exit)

#### Option 2: Professional Version (Refactored) ⭐ **RECOMMENDED**
```bash
python main_refactored.py
```
- ✓ SQLite database (persistent storage)
- ✓ Clean, modular architecture
- ✓ Production-ready
- ✓ Easy to test and extend

#### Option 3: Full Stack with API
Terminal 1:
```bash
python api_server.py
```

Terminal 2:
```bash
python main_refactored.py
```

Then use menu option 5 to import products from API.

## 📊 Database

### SQLite Schema
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

### Product Attributes
- **ID**: Unique identifier (required, primary key)
- **Name**: Product name (required)
- **Price**: Decimal price (must be >= 0)
- **Stock**: Integer quantity (must be >= 0)
- **Statement**: Status - only 'active' or 'inactive' (case-insensitive)
- **Created_at**: Auto-generated creation timestamp
- **Updated_at**: Auto-generated last update timestamp

### Data Persistence
- Database file: `inventory.db` (auto-created)
- Data survives application restarts
- ACID compliance for data integrity
- Automatic constraint enforcement

## 🏗️ Architecture

### Two Implementation Options

#### Version 1: Simple (Traditional)
```
main.py → functions.py → Memory
```
- Best for: Learning, quick prototypes
- Storage: In-memory (ephemeral)

#### Version 2: Professional (Refactored)
```
CLI → Service Layer → Repository → SQLite DB
```
- Best for: Production, enterprise use
- Storage: SQLite (persistent)

### Layered Architecture
```
┌─────────────────────────────────────┐
│   Presentation Layer (CLI)          │
│   main_refactored.py                │
├─────────────────────────────────────┤
│   Business Logic Layer              │
│   service_product.py                │
├─────────────────────────────────────┤
│   Data Access Layer (Repository)    │
│   repository_product.py             │
├─────────────────────────────────────┤
│   Data Model Layer                  │
│   models_product.py                 │
├─────────────────────────────────────┤
│   Database Connection Layer         │
│   config_db.py                      │
├─────────────────────────────────────┤
│   SQLite Database                   │
│   inventory.db                      │
└─────────────────────────────────────┘
```

## 📝 Usage

### Menu Options
```
0. Exit                    - Quit the application
1. Product register        - Add new products
2. Find product            - Search by ID or name
3. Filter products         - Filter by status or stock range
4. Show product list       - Display all products
5. Import from API         - Sync products from API server
```

### Example: Register a Product
```
Option: 1
How many products to register? 1

--- Product 1 ---
Product ID: LAPTOP-001
Product name: Dell XPS 15
Price: 1299.99
Stock: 15
Status (active/inactive): active
✓ Product 'Dell XPS 15' registered successfully
```

### Example: Search by Name
```
Option: 2
Search by:
1. ID
2. Name
Choice: 2
Enter product name: Laptop

Found 1 product(s):
1. Dell XPS 15 (ID: LAPTOP-001)

Select product number to edit (0 to cancel): 1
```

### Example: Filter Products
```
Option: 3
Filter by:
1. Status (active/inactive)
2. Stock range
3. Low stock (< 10)
Choice: 2
Enter minimum stock: 10
Enter maximum stock: 50

Products with stock between 10 and 50:
┌─────────────────────────────────────┐
│ LAPTOP-001  Dell XPS 15      1299.99  15  active │
└─────────────────────────────────────┘
Total inventory value: $19499.85
```

## 📁 Project Structure

```
proyecto/
├── main.py                  # Simple version
├── main_refactored.py       # ⭐ Professional version (recommended)
├── api_server.py            # REST API server
│
├── config_db.py            # SQLite configuration
├── models_product.py       # Product data model
├── repository_product.py   # Data access operations
├── service_product.py      # Business logic
│
├── functions.py            # Original utilities
│
├── requirements.txt        # Dependencies
│
├── docs/
│   └── README.md          # This file
│
├── ARCHITECTURE.md         # Detailed architecture guide
├── REFACTORING_GUIDE.md   # Migration guide to new version
├── PROJECT_STRUCTURE.md   # Visual structure overview
├── API_SETUP.md           # API server documentation
│
└── inventory.db           # SQLite database (auto-created)
```

## 🔌 API Server

### Starting the API
```bash
python api_server.py
```

### Endpoints
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get specific product by ID
- `GET /api/health` - Server health check
- `GET /` - API documentation

### Pre-loaded Sample Products
The API includes 10 sample products ready to import:
1. Laptop Dell XPS 15 ($1299.99)
2. Mouse Logitech MX ($99.99)
3. Keyboard Mechanical RGB ($159.99)
4. Monitor LG 27 inch ($349.99)
5. USB-C Cable ($19.99)
6. Webcam Logitech C920 ($79.99)
7. External SSD 1TB ($129.99)
8. Wireless Headphones ($199.99)
9. USB Hub 7 Ports ($49.99)
10. Laptop Stand ($39.99)

## ✅ Data Validation

### Strict Validation Rules
- **ID**: Non-empty, unique across database
- **Name**: Non-empty string
- **Price**: Numeric, non-negative
- **Stock**: Integer, non-negative
- **Status**: Must be exactly 'active' or 'inactive' (case-insensitive)

### Validation in Action
```python
# Invalid inputs are rejected
service.add_product('', 'Product', 10, 5, 'active')  # ✗ Empty ID
service.add_product('001', '', 10, 5, 'active')      # ✗ Empty name
service.add_product('001', 'Product', -10, 5, 'active')  # ✗ Negative price
service.add_product('001', 'Product', 10, -5, 'active')  # ✗ Negative stock
service.add_product('001', 'Product', 10, 5, 'pending')  # ✗ Invalid status

# Valid input
service.add_product('001', 'Product', 10.50, 5, 'active')  # ✓ Success
```

## 📚 Documentation

### [ARCHITECTURE.md](../ARCHITECTURE.md)
Complete guide to the professional architecture:
- Design patterns and principles
- Benefits of modularization
- How to extend the system
- Testing strategies
- Migration path to more advanced frameworks

### [REFACTORING_GUIDE.md](../REFACTORING_GUIDE.md)
Step-by-step guide for transitioning to the new version:
- Before/after comparison
- How each component works
- Real code examples
- Data migration strategies

### [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md)
Visual overview of the project:
- File organization
- Data flow diagrams
- Architecture benefits
- Scalability roadmap

### [API_SETUP.md](../API_SETUP.md)
Complete API server documentation:
- Installation and setup
- Available endpoints
- Testing with cURL
- Troubleshooting guide

## 🔄 Comparison: Simple vs Professional

| Feature | Simple | Professional |
|---------|--------|--------------|
| Storage | Memory | SQLite DB |
| Persistence | ❌ No | ✅ Yes |
| Architecture | Monolithic | Layered |
| Testability | Hard | Easy |
| Scalability | Limited | Excellent |
| Validation | Basic | Comprehensive |
| Code Quality | Learning | Production |
| Performance | Fast | Optimized |
| Maintenance | Difficult | Simple |

## 🎯 Use Cases

### Use Simple Version When:
- Learning Python basics
- Building quick prototypes
- Running one-time scripts
- Minimal data requirements

### Use Professional Version When:
- Building production applications
- Need data persistence
- Testing requirements exist
- Team collaboration
- Long-term maintenance needed
- Enterprise deployment

## 🚀 Future Enhancements

The refactored architecture supports easy additions:
- [ ] Unit tests with pytest
- [ ] Full REST API (FastAPI/Django)
- [ ] User authentication (JWT)
- [ ] Advanced SQL queries
- [ ] Data export (CSV, Excel, PDF)
- [ ] Docker containerization
- [ ] PostgreSQL support
- [ ] Async operations
- [ ] Redis caching
- [ ] Web dashboard

## 💡 Best Practices

1. **Always validate input** - The service layer handles automatic validation
2. **Use the service layer** - Never access repository directly from UI
3. **Handle exceptions** - All operations may raise ValueError
4. **Keep connections clean** - Context managers handle automatic cleanup
5. **Regular backups** - Copy `inventory.db` for backup
6. **Use the refactored version** - Better for new work

## 📋 Requirements

```
Python >= 3.7
Flask >= 2.3.3
Requests >= 2.31.0
SQLite >= 3.0
```

Install with:
```bash
pip install -r requirements.txt
```

## 🤝 Contributing

To extend this project:
1. Follow the existing architecture layers
2. Add validation in the service layer
3. Implement CRUD in the repository
4. Update documentation
5. Test thoroughly before committing

## 👤 Author
Violy De La Rosa

## 📄 License
MIT

---

## 🎓 Learning Paths

### For Beginners
1. Start with `main.py` to understand the concept
2. Review [REFACTORING_GUIDE.md](../REFACTORING_GUIDE.md) for architecture benefits
3. Try `main_refactored.py` with SQLite
4. Read [ARCHITECTURE.md](../ARCHITECTURE.md) for deeper understanding

### For Developers
1. Review the layered architecture in [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md)
2. Study the code separation in repository/service/model patterns
3. Understand SQLite schema and transactions
4. Extend with new features following the same patterns

### For Enterprise Use
1. Implement comprehensive test suite
2. Consider migration to PostgreSQL
3. Add authentication and authorization
4. Containerize with Docker
5. Deploy to cloud platform

---

**Recommendation**: Use `main_refactored.py` for all new development. The SQLite database ensures data persistence and the clean architecture makes the code professional, maintainable, and scalable for enterprise applications.
