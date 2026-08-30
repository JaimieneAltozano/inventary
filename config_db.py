"""Database configuration and management"""
import sqlite3
from contextlib import contextmanager
import os

class DatabaseManager:
    """Manages SQLite database connection and initialization"""
    
    def __init__(self, db_name: str = 'inventory.db'):
        """Initialize database manager
        
        Args:
            db_name: Name of the SQLite database file
        """
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Create tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL,
                    statement TEXT NOT NULL CHECK(statement IN ('active', 'inactive')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections
        
        Yields:
            sqlite3.Connection: Database connection
        """
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Access columns by name
        try:
            yield conn
        finally:
            conn.close()
    
    def database_exists(self) -> bool:
        """Check if database file exists"""
        return os.path.exists(self.db_name)
    
    def get_db_stats(self) -> dict:
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM products')
            count = cursor.fetchone()[0]
            cursor.execute('SELECT SUM(price * stock) FROM products')
            total_value = cursor.fetchone()[0]
        
        return {
            'total_products': count,
            'total_inventory_value': total_value or 0.0,
            'database_file': self.db_name
        }
