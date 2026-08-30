products = []

def validate_statement(statement):
    """Validate that statement is either 'active' or 'inactive'
    
    Args:
        statement (str): The statement to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return statement.lower() in ["active", "inactive"]


def get_valid_statement():
    """Get a valid statement input from user"""
    while True:
        statement = input("Statement product (active/inactive): ").lower()
        if validate_statement(statement):
            return statement
        print("Invalid input. Please enter 'active' or 'inactive'.")


def product(info1, info2, info3, info4, info5):
    """Add a new product to the inventory"""
    products.append({
        "Name": info1,
        "ID": info2,
        "Prize": info3,
        "Stock": info4,
        "Statement": info5.lower() if isinstance(info5, str) else info5,
    })


def find_by_id(product_id):
    """Search for a product by ID
    
    Args:
        product_id (str): The product ID to search
        
    Returns:
        dict or None: The product dictionary if found, None otherwise
    """
    for product_item in products:
        if product_item["ID"] == product_id:
            return product_item
    return None


def find_by_name(product_name):
    """Search for products by name (case-insensitive, partial match)
    
    Args:
        product_name (str): The product name to search
        
    Returns:
        list: List of products matching the search
    """
    results = []
    name_lower = product_name.lower()
    for product_item in products:
        if name_lower in product_item["Name"].lower():
            results.append(product_item)
    return results


def filter_products(key, value):
    """Filter products by a specific attribute
    
    Args:
        key (str): The attribute to filter by (Name, ID, Prize, Stock, Statement)
        value: The value to filter by
        
    Returns:
        list: List of products matching the filter criteria
    """
    results = []
    for product_item in products:
        if key == "Prize" or key == "Stock":
            # For numeric comparisons
            try:
                if float(product_item[key]) == float(value):
                    results.append(product_item)
            except (ValueError, KeyError):
                continue
        else:
            # For string comparisons (case-insensitive)
            if str(product_item.get(key, "")).lower() == str(value).lower():
                results.append(product_item)
    return results


def filter_by_statement(statement):
    """Filter products by status (active/inactive)
    
    Args:
        statement (str): The statement to filter (active/inactive)
        
    Returns:
        list: List of products with the specified statement
    """
    return filter_products("Statement", statement)


def filter_by_stock_range(min_stock, max_stock):
    """Filter products by stock range
    
    Args:
        min_stock (int): Minimum stock quantity
        max_stock (int): Maximum stock quantity
        
    Returns:
        list: List of products within the stock range
    """
    results = []
    for product_item in products:
        try:
            stock = int(product_item["Stock"])
            if min_stock <= stock <= max_stock:
                results.append(product_item)
        except (ValueError, KeyError):
            continue
    return results


def sync_products_from_api(api_url="http://localhost:5000/api/products"):
    """Synchronize products from external API to local inventory
    
    Args:
        api_url (str): The API endpoint URL to fetch products from
        
    Returns:
        bool: True if sync was successful, False otherwise
    """
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library is required.")
        print("Install it with: pip install requests")
        return False
    
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        api_products = response.json()
        
        if not isinstance(api_products, list):
            print("Error: API response is not a list of products")
            return False
        
        imported_count = 0
        for item in api_products:
            try:
                product(
                    info1=str(item.get("name", "")),
                    info2=str(item.get("id", "")),
                    info3=str(item.get("prize", "")),
                    info4=str(item.get("stock", "")),
                    info5=str(item.get("statement", "active"))
                )
                imported_count += 1
            except Exception as e:
                print(f"Warning: Could not import product: {e}")
                continue
        
        print(f"✓ Successfully imported {imported_count} products from API")
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to API at {api_url}")
        print("Make sure the API server is running: python api_server.py")
        return False
    except requests.exceptions.Timeout:
        print("Error: API request timed out")
        return False
    except Exception as e:
        print(f"Error syncing from API: {e}")
        return False