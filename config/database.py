"""Database configuration and management."""

import os
import sqlite3
from contextlib import contextmanager


class DatabaseManager:
    """Manages SQLite database connection and initialization."""

    def __init__(self, db_name: str = "inventory.db"):
        """Initialize the database manager.

        Args:
            db_name: Name or path of the SQLite database file.
        """
        self.db_name = db_name
        self.init_db()

    def init_db(self) -> None:
        """Create the products table if it does not exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL,
                    statement TEXT NOT NULL
                        CHECK(statement IN ('active', 'inactive')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()

    @contextmanager
    def get_connection(self):
        """Create and safely close a database connection.

        Yields:
            sqlite3.Connection: SQLite database connection.
        """
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row

        try:
            yield conn
        finally:
            conn.close()

    def database_exists(self) -> bool:
        """Check whether the database file exists.

        Returns:
            True if the database file exists, otherwise False.
        """
        return os.path.exists(self.db_name)

    def get_db_stats(self) -> dict:
        """Get basic database statistics.

        Returns:
            A dictionary containing the total number of products,
            total inventory value, and database file name.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM products")
            total_products = cursor.fetchone()[0]

            cursor.execute("SELECT SUM(price * stock) FROM products")
            total_inventory_value = cursor.fetchone()[0]

        return {
            "total_products": total_products,
            "total_inventory_value": total_inventory_value or 0.0,
            "database_file": self.db_name,
        }
