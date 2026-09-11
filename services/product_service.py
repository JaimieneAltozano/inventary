"""Product service - Business logic layer"""
from typing import List, Optional
from models.product import Product
from inventary.repositories.product_repository import ProductRepository

class ProductService:
    """Service for product business logic"""
    
    def __init__(self, repository: ProductRepository):
        """Initialize service with repository
        
        Args:
            repository: Product repository instance
        """
        self.repository = repository
    
    def add_product(self, id: str, name: str, price: float, 
                   stock: int, statement: str) -> Product:
        """Add a new product with validation
        
        Args:
            id: Product ID
            name: Product name
            price: Product price
            stock: Stock quantity
            statement: Status (active/inactive)
            
        Returns:
            Product: Created product
            
        Raises:
            ValueError: If validation fails
        """
        product = Product(id, name, price, stock, statement.lower().strip())
        product.validate()
        return self.repository.create(product)
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """Get product by ID
        
        Args:
            product_id: Product ID
            
        Returns:
            Product or None: Product if found
            
        Raises:
            ValueError: If product not found
        """
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID '{product_id}' not found")
        return product
    
    def list_all_products(self) -> List[Product]:
        """Get all products
        
        Returns:
            List[Product]: All products
        """
        return self.repository.get_all()
    
    def search_by_name(self, name: str) -> List[Product]:
        """Search products by name
        
        Args:
            name: Name to search (partial match supported)
            
        Returns:
            List[Product]: Matching products
            
        Raises:
            ValueError: If no products found
        """
        if not name or not name.strip():
            raise ValueError("Search term cannot be empty")
        
        results = self.repository.find_by_name(name)
        if not results:
            raise ValueError(f"No products found with name containing '{name}'")
        return results
    
    def update_product(self, id: str, name: str, price: float,
                      stock: int, statement: str) -> Product:
        """Update product with validation
        
        Args:
            id: Product ID
            name: New product name
            price: New price
            stock: New stock quantity
            statement: New status
            
        Returns:
            Product: Updated product
            
        Raises:
            ValueError: If validation fails or product not found
        """
        product = Product(id, name, price, stock, statement.lower().strip())
        product.validate()
        return self.repository.update(product)
    
    def delete_product(self, product_id: str) -> bool:
        """Delete a product
        
        Args:
            product_id: Product ID to delete
            
        Returns:
            bool: True if deleted
            
        Raises:
            ValueError: If product not found
        """
        if not self.repository.delete(product_id):
            raise ValueError(f"Product with ID '{product_id}' not found")
        return True
    
    def get_active_products(self) -> List[Product]:
        """Get all active products
        
        Returns:
            List[Product]: Active products
        """
        return self.repository.filter_by_statement('active')
    
    def get_inactive_products(self) -> List[Product]:
        """Get all inactive products
        
        Returns:
            List[Product]: Inactive products
        """
        return self.repository.filter_by_statement('inactive')
    
    def get_products_by_status(self, statement: str) -> List[Product]:
        """Get products filtered by status
        
        Args:
            statement: Status to filter ('active' or 'inactive')
            
        Returns:
            List[Product]: Filtered products
            
        Raises:
            ValueError: If invalid statement
        """
        statement = statement.lower().strip()
        if statement not in ['active', 'inactive']:
            raise ValueError("Statement must be 'active' or 'inactive'")
        return self.repository.filter_by_statement(statement)
    
    def get_products_in_stock_range(self, min_stock: int, max_stock: int) -> List[Product]:
        """Get products within stock range
        
        Args:
            min_stock: Minimum stock
            max_stock: Maximum stock
            
        Returns:
            List[Product]: Products in range
            
        Raises:
            ValueError: If range is invalid
        """
        if min_stock < 0 or max_stock < 0:
            raise ValueError("Stock values cannot be negative")
        if min_stock > max_stock:
            raise ValueError("Minimum stock cannot exceed maximum stock")
        
        return self.repository.filter_by_stock_range(min_stock, max_stock)
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock
        
        Args:
            threshold: Stock threshold (default 10)
            
        Returns:
            List[Product]: Products below threshold
        """
        if threshold < 0:
            raise ValueError("Threshold cannot be negative")
        return self.repository.get_low_stock(threshold)
    
    def get_total_inventory_value(self) -> float:
        """Calculate total inventory value
        
        Returns:
            float: Total value (price * stock for all products)
        """
        total = 0.0
        for product in self.list_all_products():
            total += float(product.price) * int(product.stock)
        return total
    
    def get_product_count(self) -> int:
        """Get total number of products
        
        Returns:
            int: Total products
        """
        return self.repository.count()
