# Refactorización a Arquitectura Profesional y Escalable

## Problema con la Estructura Actual

La arquitectura actual tiene limitaciones:

1. **Lógica mezclada**: Interfaz de usuario, lógica de negocio y persistencia en archivos separados pero sin separación clara de responsabilidades
2. **Difícil de testear**: Acoplamiento fuerte entre componentes
3. **Difícil de escalar**: Agregar nuevas características requiere modificar múltiples archivos
4. **Gestión de datos en memoria**: Los datos se pierden si la aplicación falla
5. **Duplicación de código**: Validaciones y operaciones repetidas

## Arquitectura Propuesta: Clean Architecture + Repository Pattern

```
proyecto/
├── config/
│   ├── __init__.py
│   └── database.py          # Configuración de SQLite
├── models/
│   ├── __init__.py
│   └── product.py           # Clase Product (entidad)
├── repositories/
│   ├── __init__.py
│   └── product_repository.py # Acceso a datos (CRUD)
├── services/
│   ├── __init__.py
│   └── product_service.py    # Lógica de negocio
├── exceptions/
│   ├── __init__.py
│   └── exceptions.py         # Excepciones personalizadas
├── ui/
│   ├── __init__.py
│   └── cli.py               # Interfaz de usuario
├── api/
│   ├── __init__.py
│   └── client.py            # Cliente API externo
├── main.py                   # Punto de entrada
├── api_server.py            # API REST (sin cambios)
└── requirements.txt         # Dependencias
```

## Ventajas de esta Arquitectura

| Aspecto | Actual | Propuesta |
|--------|--------|----------|
| **Separación de responsabilidades** | ❌ Mezclada | ✅ Clara |
| **Testabilidad** | ❌ Difícil | ✅ Excelente (inyección de dependencias) |
| **Escalabilidad** | ❌ Limitada | ✅ Altamente escalable |
| **Persistencia** | ❌ En memoria | ✅ SQLite con transacciones |
| **Mantenibilidad** | ❌ Complicada | ✅ Simple y clara |
| **Reutilización** | ❌ Baja | ✅ Alta |
| **Cambio de BD** | ❌ Requiere refactor total | ✅ Solo cambiar repository |
| **API REST** | ✅ Presente | ✅ Presente |

## Componentes Principales

### 1. **config/database.py** - Gestión de Conexión
```python
import sqlite3
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_name='inventory.db'):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Crear tabla si no existe"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL,
                    statement TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()
```

### 2. **models/product.py** - Clase de Entidad
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Product:
    id: str
    name: str
    price: float
    stock: int
    statement: str
    created_at: datetime = None
    updated_at: datetime = None
    
    def validate(self):
        """Validar datos del producto"""
        if not self.id:
            raise ValueError("ID cannot be empty")
        if not self.name:
            raise ValueError("Name cannot be empty")
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.stock < 0:
            raise ValueError("Stock cannot be negative")
        if self.statement not in ['active', 'inactive']:
            raise ValueError("Statement must be 'active' or 'inactive'")
```

### 3. **repositories/product_repository.py** - Acceso a Datos
```python
from models.product import Product
from exceptions.exceptions import ProductNotFoundError

class ProductRepository:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create(self, product: Product):
        """Crear nuevo producto"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO products (id, name, price, stock, statement)
                VALUES (?, ?, ?, ?, ?)
            ''', (product.id, product.name, product.price, 
                  product.stock, product.statement))
            conn.commit()
    
    def get_by_id(self, product_id: str):
        """Obtener producto por ID"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            row = cursor.fetchone()
            if not row:
                raise ProductNotFoundError(f"Product {product_id} not found")
            return self._row_to_product(row)
    
    def get_all(self):
        """Obtener todos los productos"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products')
            return [self._row_to_product(row) for row in cursor.fetchall()]
    
    def update(self, product: Product):
        """Actualizar producto"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products 
                SET name=?, price=?, stock=?, statement=?
                WHERE id=?
            ''', (product.name, product.price, product.stock, 
                  product.statement, product.id))
            if cursor.rowcount == 0:
                raise ProductNotFoundError(f"Product {product.id} not found")
            conn.commit()
    
    def delete(self, product_id: str):
        """Eliminar producto"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            if cursor.rowcount == 0:
                raise ProductNotFoundError(f"Product {product_id} not found")
            conn.commit()
    
    def search_by_name(self, name: str):
        """Buscar productos por nombre"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM products WHERE name LIKE ?',
                (f'%{name}%',)
            )
            return [self._row_to_product(row) for row in cursor.fetchall()]
    
    def filter_by_statement(self, statement: str):
        """Filtrar por estado"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM products WHERE statement = ?',
                (statement,)
            )
            return [self._row_to_product(row) for row in cursor.fetchall()]
    
    @staticmethod
    def _row_to_product(row):
        """Convertir fila de BD a objeto Product"""
        return Product(
            id=row[0], name=row[1], price=row[2],
            stock=row[3], statement=row[4],
            created_at=row[5], updated_at=row[6]
        )
```

### 4. **services/product_service.py** - Lógica de Negocio
```python
from models.product import Product
from exceptions.exceptions import ValidationError

class ProductService:
    def __init__(self, repository):
        self.repository = repository
    
    def add_product(self, id: str, name: str, price: float, 
                    stock: int, statement: str) -> Product:
        """Agregar nuevo producto con validación"""
        product = Product(id, name, price, stock, statement.lower())
        product.validate()
        self.repository.create(product)
        return product
    
    def find_product(self, product_id: str):
        """Buscar producto por ID"""
        return self.repository.get_by_id(product_id)
    
    def find_by_name(self, name: str):
        """Buscar productos por nombre"""
        results = self.repository.search_by_name(name)
        if not results:
            raise ValueError(f"No products found with name '{name}'")
        return results
    
    def get_all_products(self):
        """Obtener todos los productos"""
        return self.repository.get_all()
    
    def update_product(self, id: str, name: str, price: float,
                      stock: int, statement: str) -> Product:
        """Actualizar producto con validación"""
        product = Product(id, name, price, stock, statement.lower())
        product.validate()
        self.repository.update(product)
        return product
    
    def delete_product(self, product_id: str):
        """Eliminar producto"""
        self.repository.delete(product_id)
    
    def filter_active(self):
        """Obtener productos activos"""
        return self.repository.filter_by_statement('active')
    
    def filter_inactive(self):
        """Obtener productos inactivos"""
        return self.repository.filter_by_statement('inactive')
    
    def get_low_stock_products(self, threshold: int = 10):
        """Obtener productos con stock bajo"""
        all_products = self.repository.get_all()
        return [p for p in all_products if p.stock <= threshold]
```

### 5. **exceptions/exceptions.py** - Excepciones Personalizadas
```python
class InventoryException(Exception):
    """Excepción base"""
    pass

class ProductNotFoundError(InventoryException):
    """Producto no encontrado"""
    pass

class ValidationError(InventoryException):
    """Error de validación"""
    pass

class DatabaseError(InventoryException):
    """Error en la base de datos"""
    pass
```

### 6. **main.py** - Punto de Entrada (Refactorizado)
```python
from config.database import DatabaseManager
from repositories.product_repository import ProductRepository
from services.product_service import ProductService
from ui.cli import InventoryUI

def main():
    # Inicializar componentes (inyección de dependencias)
    db_manager = DatabaseManager('inventory.db')
    repository = ProductRepository(db_manager)
    service = ProductService(repository)
    
    # Iniciar interfaz de usuario
    ui = InventoryUI(service)
    ui.run()

if __name__ == '__main__':
    main()
```

## Beneficios para Mantenimiento y Testing

### Testing (Ejemplo)
```python
# tests/test_product_service.py
import pytest
from models.product import Product
from services.product_service import ProductService
from unittest.mock import Mock

def test_add_product_valid():
    mock_repo = Mock()
    service = ProductService(mock_repo)
    
    service.add_product('PROD-001', 'Test', 10.0, 5, 'active')
    mock_repo.create.assert_called_once()

def test_add_product_invalid_statement():
    mock_repo = Mock()
    service = ProductService(mock_repo)
    
    with pytest.raises(ValueError):
        service.add_product('PROD-001', 'Test', 10.0, 5, 'invalid')
```

### Cambiar de Base de Datos
Si necesitas cambiar a PostgreSQL, solo creas un nuevo `DatabaseManager`:
```python
class PostgresManager:  # Misma interfaz
    def init_db(self): ...
    def get_connection(self): ...
```

No necesitas cambiar `repository` ni `service`.

## Plan de Implementación (Gradual)

**Fase 1** (Actual): Código funcional
**Fase 2**: Agregar capas de abstracción (repository, service)
**Fase 3**: Migrar UI a clase separada
**Fase 4**: Agregar tests unitarios
**Fase 5**: Considerar framework web (FastAPI, Django)

## Conclusión

Una arquitectura modularizada permite:
- ✅ Código más limpio y profesional
- ✅ Fácil de extender sin refactoring mayor
- ✅ Tests unitarios efectivos
- ✅ Cambios en BD sin afectar lógica
- ✅ Preparado para crecer a escala empresarial
