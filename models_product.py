"""Product model and data classes"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Product:
    """Product entity model"""
    id: str
    name: str
    price: float
    stock: int
    statement: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def validate(self) -> bool:
        """Validate product data integrity
        
        Raises:
            ValueError: If validation fails
            
        Returns:
            bool: True if valid
        """
        if not self.id or not self.id.strip():
            raise ValueError("Product ID cannot be empty")
        
        if not self.name or not self.name.strip():
            raise ValueError("Product name cannot be empty")
        
        try:
            price = float(self.price)
            if price < 0:
                raise ValueError("Price cannot be negative")
        except (ValueError, TypeError):
            raise ValueError("Price must be a valid number")
        
        try:
            stock = int(self.stock)
            if stock < 0:
                raise ValueError("Stock cannot be negative")
        except (ValueError, TypeError):
            raise ValueError("Stock must be a valid integer")
        
        statement = str(self.statement).lower().strip()
        if statement not in ['active', 'inactive']:
            raise ValueError("Statement must be 'active' or 'inactive'")
        
        return True
    
    def to_dict(self) -> dict:
        """Convert product to dictionary
        
        Returns:
            dict: Product data as dictionary
        """
        return {
            'ID': self.id,
            'Name': self.name,
            'Prize': self.price,
            'Stock': self.stock,
            'Statement': self.statement.lower(),
            'Created': self.created_at,
            'Updated': self.updated_at
        }
    
    @staticmethod
    def from_row(row: tuple) -> 'Product':
        """Create Product from database row
        
        Args:
            row: Database row tuple
            
        Returns:
            Product: Product instance
        """
        return Product(
            id=row[0],
            name=row[1],
            price=float(row[2]),
            stock=int(row[3]),
            statement=row[4],
            created_at=row[5],
            updated_at=row[6]
        )
