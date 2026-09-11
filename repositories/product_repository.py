"""Product repository - Data access layer"""
from typing import List, Optional
from models.product import Product
from config.database import DatabaseManager

class ProductRepository:
    """Repository for product CRUD operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize repository with database manager
        
        Args:
            db_manager: Database connection manager
        """
        self.db = db_manager
    
    def create(self, product: Product) -> Product:
        """Create a new product
        
        Args:
            product: Product instance to save
            
        Returns:
            Product: Saved product
            
        Raises:
            ValueError: If product ID already exists
        """
        product.validate()
        
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO products (id, name, price, stock, statement)
                    VALUES (?, ?, ?, ?, ?)
                ''', (product.id, product.name, float(product.price), 
                      int(product.stock), product.statement.lower()))
                conn.commit()
            return product
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"Product with ID '{product.id}' already exists")
            raise
    
    def get_by_id(self, product_id: str) -> Optional[Product]:
        """Get product by ID
        
        Args:
            product_id: Product ID to search
            
        Returns:
            Product or None: Product if found, None otherwise
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            row = cursor.fetchone()
            if row:
                return Product.from_row(row)
            return None
    
    def get_all(self) -> List[Product]:
        """Get all products
        
        Returns:
            List[Product]: List of all products
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
            return [Product.from_row(row) for row in cursor.fetchall()]
    
    def update(self, product: Product) -> Product:
        """Update an existing product
        
        Args:
            product: Product instance with updated data
            
        Returns:
            Product: Updated product
            
        Raises:
            ValueError: If product not found
        """
        product.validate()
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products 
                SET name=?, price=?, stock=?, statement=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            ''', (product.name, float(product.price), int(product.stock), 
                  product.statement.lower(), product.id))
            
            if cursor.rowcount == 0:
                raise ValueError(f"Product with ID '{product.id}' not found")
            
            conn.commit()
        
        return self.get_by_id(product.id)
    
    def delete(self, product_id: str) -> bool:
        """Delete a product
        
        Args:
            product_id: Product ID to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def find_by_name(self, name: str) -> List[Product]:
        """Search products by name (partial match, case-insensitive)
        
        Args:
            name: Name to search
            
        Returns:
            List[Product]: Matching products
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM products WHERE LOWER(name) LIKE LOWER(?) ORDER BY created_at DESC',
                (f'%{name}%',)
            )
            return [Product.from_row(row) for row in cursor.fetchall()]
    
    def filter_by_statement(self, statement: str) -> List[Product]:
        """Filter products by status (active/inactive)
        
        Args:
            statement: Status to filter ('active' or 'inactive')
            
        Returns:
            List[Product]: Products with specified status
        """
        statement = statement.lower().strip()
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM products WHERE statement = ? ORDER BY created_at DESC',
                (statement,)
            )
            return [Product.from_row(row) for row in cursor.fetchall()]
    
    def filter_by_stock_range(self, min_stock: int, max_stock: int) -> List[Product]:
        """Filter products by stock range
        
        Args:
            min_stock: Minimum stock quantity
            max_stock: Maximum stock quantity
            
        Returns:
            List[Product]: Products within stock range
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM products WHERE stock BETWEEN ? AND ? ORDER BY stock ASC',
                (min_stock, max_stock)
            )
            return [Product.from_row(row) for row in cursor.fetchall()]
    
    def get_low_stock(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock
        
        Args:
            threshold: Stock threshold
            
        Returns:
            List[Product]: Products below threshold
        """
        return self.filter_by_stock_range(0, threshold)
    
    def count(self) -> int:
        """Get total number of products
        
        Returns:
            int: Total product count
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM products')
            return cursor.fetchone()[0]
