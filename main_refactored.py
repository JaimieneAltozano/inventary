"""Main application - Refactored with clean architecture"""
import sys
from config_db import DatabaseManager
from repository_product import ProductRepository
from service_product import ProductService
from models_product import Product

class InventoryApp:
    """Main inventory application with refactored architecture"""
    
    def __init__(self):
        """Initialize application with dependency injection"""
        self.db_manager = DatabaseManager('inventory.db')
        self.repository = ProductRepository(self.db_manager)
        self.service = ProductService(self.repository)
    
    def print_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("INVENTORY MANAGEMENT SYSTEM")
        print("="*60)
        print("\n0. Exit")
        print("1. Register new products")
        print("2. Find product")
        print("3. Filter products")
        print("4. Show all products")
        print("5. Import from API")
        print("\n" + "="*60)
    
    def register_products(self):
        """Register new products"""
        try:
            quantity = int(input("How many products to register? "))
            if quantity <= 0:
                print("Quantity must be positive")
                return
            
            for i in range(quantity):
                print(f"\n--- Product {i+1} ---")
                id_product = input("Product ID: ").strip()
                name_product = input("Product name: ").strip()
                price_product = input("Price: ").strip()
                stock_product = input("Stock: ").strip()
                
                statement = self._get_valid_statement()
                
                try:
                    self.service.add_product(
                        id_product, name_product, price_product, 
                        stock_product, statement
                    )
                    print(f"✓ Product '{name_product}' registered successfully")
                except ValueError as e:
                    print(f"✗ Error: {e}")
        
        except ValueError:
            print("Invalid input")
    
    def find_product(self):
        """Find and manage a product"""
        print("\nSearch by:")
        print("1. ID")
        print("2. Name")
        choice = input("Choice: ").strip()
        
        if choice == "1":
            self._search_by_id()
        elif choice == "2":
            self._search_by_name()
        else:
            print("Invalid option")
    
    def _search_by_id(self):
        """Search product by ID"""
        product_id = input("Enter product ID: ").strip()
        
        try:
            product = self.service.get_product(product_id)
            self._display_product(product)
            self._manage_product(product)
        except ValueError as e:
            print(f"✗ {e}")
    
    def _search_by_name(self):
        """Search products by name"""
        name = input("Enter product name: ").strip()
        
        try:
            products = self.service.search_by_name(name)
            print(f"\nFound {len(products)} product(s):")
            
            for idx, prod in enumerate(products, 1):
                print(f"{idx}. {prod.name} (ID: {prod.id})")
            
            try:
                choice = int(input("\nSelect product number (0 to cancel): "))
                if 1 <= choice <= len(products):
                    selected = products[choice - 1]
                    self._display_product(selected)
                    self._manage_product(selected)
            except ValueError:
                print("Invalid input")
        
        except ValueError as e:
            print(f"✗ {e}")
    
    def _display_product(self, product: Product):
        """Display product details"""
        print("\n" + "-"*50)
        print(f"ID: {product.id}")
        print(f"Name: {product.name}")
        print(f"Price: ${product.price}")
        print(f"Stock: {product.stock}")
        print(f"Status: {product.statement}")
        print("-"*50)
    
    def _manage_product(self, product: Product):
        """Manage (update/delete) a product"""
        print("\n1. Update")
        print("2. Delete")
        print("3. Back to menu")
        choice = input("Choice: ").strip()
        
        if choice == "1":
            self._update_product(product.id)
        elif choice == "2":
            self._delete_product(product.id)
    
    def _update_product(self, product_id: str):
        """Update product details"""
        print("\nEnter new details (or press Enter to keep current):")
        
        current = self.service.get_product(product_id)
        name = input(f"Name [{current.name}]: ").strip() or current.name
        price = input(f"Price [{current.price}]: ").strip() or current.price
        stock = input(f"Stock [{current.stock}]: ").strip() or current.stock
        statement = input(f"Status [{current.statement}]: ").strip() or current.statement
        
        try:
            updated = self.service.update_product(
                product_id, name, price, stock, statement
            )
            print("✓ Product updated successfully")
            self._display_product(updated)
        except ValueError as e:
            print(f"✗ Error: {e}")
    
    def _delete_product(self, product_id: str):
        """Delete a product"""
        confirm = input(f"Confirm deletion of product '{product_id}'? (yes/no): ").lower()
        
        if confirm == 'yes':
            try:
                self.service.delete_product(product_id)
                print("✓ Product deleted successfully")
            except ValueError as e:
                print(f"✗ Error: {e}")
    
    def filter_products(self):
        """Filter products menu"""
        print("\nFilter by:")
        print("1. Status (active/inactive)")
        print("2. Stock range")
        print("3. Low stock (< 10)")
        choice = input("Choice: ").strip()
        
        if choice == "1":
            self._filter_by_status()
        elif choice == "2":
            self._filter_by_stock_range()
        elif choice == "3":
            self._filter_low_stock()
        else:
            print("Invalid option")
    
    def _filter_by_status(self):
        """Filter by active/inactive"""
        status = input("Enter status (active/inactive): ").strip().lower()
        
        try:
            products = self.service.get_products_by_status(status)
            self._display_products_list(products, f"Products with status '{status}'")
        except ValueError as e:
            print(f"✗ {e}")
    
    def _filter_by_stock_range(self):
        """Filter by stock range"""
        try:
            min_stock = int(input("Minimum stock: "))
            max_stock = int(input("Maximum stock: "))
            
            products = self.service.get_products_in_stock_range(min_stock, max_stock)
            self._display_products_list(
                products, 
                f"Products with stock between {min_stock} and {max_stock}"
            )
        except ValueError as e:
            print(f"✗ {e}")
    
    def _filter_low_stock(self):
        """Filter low stock products"""
        products = self.service.get_low_stock_products(threshold=10)
        self._display_products_list(products, "Products with low stock (< 10)")
    
    def show_all_products(self):
        """Display all products"""
        products = self.service.list_all_products()
        self._display_products_list(products, "All Products in Inventory")
    
    def _display_products_list(self, products: list, title: str = "Products"):
        """Display list of products"""
        if not products:
            print(f"No {title.lower()} found")
            return
        
        print(f"\n{title}:")
        print("-"*70)
        print(f"{'ID':<15} {'Name':<25} {'Price':<10} {'Stock':<8} {'Status':<10}")
        print("-"*70)
        
        for product in products:
            print(f"{product.id:<15} {product.name:<25} ${product.price:<9.2f} "
                  f"{product.stock:<8} {product.statement:<10}")
        
        print("-"*70)
        print(f"Total inventory value: ${self.service.get_total_inventory_value():.2f}")
    
    def import_from_api(self):
        """Import products from external API"""
        print("\nImport from API")
        print("Make sure API server is running: python api_server.py")
        
        try:
            import requests
        except ImportError:
            print("✗ Error: 'requests' library required. Install with: pip install requests")
            return
        
        url = input("Enter API URL (default: http://localhost:5000/api/products): ").strip()
        if not url:
            url = "http://localhost:5000/api/products"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if not isinstance(data, list):
                print("✗ Invalid API response format")
                return
            
            imported = 0
            for item in data:
                try:
                    self.service.add_product(
                        item.get('id', ''),
                        item.get('name', ''),
                        item.get('prize', '0'),
                        item.get('stock', '0'),
                        item.get('statement', 'active')
                    )
                    imported += 1
                except ValueError:
                    continue  # Skip invalid products
            
            print(f"✓ Successfully imported {imported} products from API")
        
        except requests.exceptions.ConnectionError:
            print(f"✗ Could not connect to API at {url}")
            print("  Make sure the API server is running")
        except Exception as e:
            print(f"✗ Error importing from API: {e}")
    
    def _get_valid_statement(self) -> str:
        """Get and validate statement input"""
        while True:
            statement = input("Status (active/inactive): ").strip().lower()
            if statement in ['active', 'inactive']:
                return statement
            print("Please enter 'active' or 'inactive'")
    
    def run(self):
        """Run main application loop"""
        print("\n" + "="*60)
        print("Welcome to Inventory Management System")
        print("Using SQLite Database")
        print("="*60)
        
        while True:
            self.print_menu()
            option = input("\nOption: ").strip()
            
            if option == "0":
                print("\nGoodbye!")
                break
            elif option == "1":
                self.register_products()
            elif option == "2":
                self.find_product()
            elif option == "3":
                self.filter_products()
            elif option == "4":
                self.show_all_products()
            elif option == "5":
                self.import_from_api()
            else:
                print("✗ Invalid option")

def main():
    """Entry point"""
    app = InventoryApp()
    app.run()

if __name__ == '__main__':
    main()
