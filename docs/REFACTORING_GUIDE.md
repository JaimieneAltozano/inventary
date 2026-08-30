# Guía de Uso - Arquitectura Refactorizada

## ¿Qué es esto?

Este es un ejemplo de cómo refactorizar tu proyecto con una **arquitectura profesional y escalable** usando:
- ✅ **SQLite** para persistencia de datos
- ✅ **Clean Architecture** (separación de responsabilidades)
- ✅ **Repository Pattern** (acceso a datos)
- ✅ **Service Layer** (lógica de negocio)
- ✅ **Dependency Injection** (código desacoplado)

## Archivos Principales

### Capa de Datos (Data Layer)
- **`config_db.py`** - Gestión de conexión a SQLite
- **`models_product.py`** - Definición de entidad Product
- **`repository_product.py`** - Operaciones CRUD

### Capa de Negocio (Business Layer)
- **`service_product.py`** - Lógica de negocio

### Capa de Presentación (UI Layer)
- **`main_refactored.py`** - Interfaz de usuario mejorada

## Estructura del Código

```
┌─────────────────────────────────────┐
│     Interfaz de Usuario (UI)        │
│      (main_refactored.py)           │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│     Lógica de Negocio (Service)     │
│      (service_product.py)           │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│     Acceso a Datos (Repository)     │
│   (repository_product.py)           │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│    Base de Datos (SQLite)           │
│      (config_db.py)                 │
└─────────────────────────────────────┘
```

## Instalación y Uso

### 1. Instalar dependencias
```bash
pip install requests flask
```

### 2. Ejecutar la aplicación refactorizada
```bash
python main_refactored.py
```

### 3. (Opcional) Ejecutar servidor API
En otra terminal:
```bash
python api_server.py
```

## Comparación: Antes vs Después

### ANTES (Código Original)
```python
# main.py - Todo mezclado
import functions

products_list = []  # En memoria

if option == "1":
    functions.product(name, id, price, stock, statement)
    print(products_list)

# functions.py
products = []

def product(info1, info2, info3, info4, info5):
    products.append({...})  # Sin validación, sin persistencia

def find_by_id(product_id):
    for product_item in products:  # Búsqueda lineal
        if product_item["ID"] == product_id:
            return product_item
```

**Problemas:**
- ❌ Datos en memoria (se pierden al cerrar)
- ❌ Sin separación de responsabilidades
- ❌ Difícil de testear
- ❌ Búsqueda ineficiente
- ❌ Sin validaciones robustas

### DESPUÉS (Arquitectura Refactorizada)
```python
# main_refactored.py - Interfaz clara
class InventoryApp:
    def __init__(self):
        self.db_manager = DatabaseManager('inventory.db')
        self.repository = ProductRepository(self.db_manager)
        self.service = ProductService(self.repository)
    
    def register_products(self):
        self.service.add_product(id, name, price, stock, statement)

# service_product.py - Lógica de negocio
class ProductService:
    def add_product(self, id, name, price, stock, statement):
        product = Product(id, name, price, stock, statement)
        product.validate()  # Validación centralizada
        return self.repository.create(product)

# repository_product.py - Acceso a datos
class ProductRepository:
    def create(self, product):
        with self.db.get_connection() as conn:
            cursor.execute('''INSERT INTO products...''')
            # Usa índices, transacciones, etc.

# config_db.py - Base de datos
class DatabaseManager:
    def init_db(self):
        # Crea tabla con constraints
```

**Ventajas:**
- ✅ Datos persistentes en SQLite
- ✅ Separación clara de capas
- ✅ Fácil de testear (inyección de dependencias)
- ✅ Búsqueda eficiente (índices de BD)
- ✅ Validaciones robustas
- ✅ Código profesional y escalable

## Cambios Principales en la BD

### Esquema SQLite
```sql
CREATE TABLE products (
    id TEXT PRIMARY KEY,           -- Identificador único
    name TEXT NOT NULL,            -- Nombre del producto
    price REAL NOT NULL,           -- Precio (decimal)
    stock INTEGER NOT NULL,        -- Stock (entero)
    statement TEXT CHECK(statement IN ('active', 'inactive')), -- Estado
    created_at TIMESTAMP,          -- Fecha de creación
    updated_at TIMESTAMP           -- Fecha de actualización
)
```

### Beneficios de SQLite
- 📦 Archivo único (`inventory.db`)
- 🔒 Integridad de datos (constraints)
- ⚡ Rápido para datos pequeños/medianos
- 🔄 Transacciones ACID
- 📊 SQL queries complejas

## Ejemplos de Uso

### Crear producto (con validación automática)
```python
service.add_product(
    'LAPTOP-001',
    'Dell XPS 15',
    1299.99,
    15,
    'active'
)
# ✓ Se valida automáticamente
# ✗ Si el estado no es 'active' o 'inactive', lanza ValueError
```

### Buscar por ID (rápido con índices)
```python
product = service.get_product('LAPTOP-001')
# Busca en BD con índice (O(log n)) en vez de lineal (O(n))
```

### Filtrar por rango de stock (con SQL)
```python
low_stock = service.get_products_in_stock_range(0, 10)
# SELECT * FROM products WHERE stock BETWEEN 0 AND 10
```

## Cómo Escalar

### Cambiar a PostgreSQL
Solo necesitas cambiar `config_db.py`:
```python
import psycopg2

class DatabaseManager:
    def __init__(self, dsn='postgresql://...'):
        self.dsn = dsn
    
    @contextmanager
    def get_connection(self):
        conn = psycopg2.connect(self.dsn)
        yield conn
        conn.close()
```

**Resto del código no cambia** ✅

### Agregar autenticación
```python
# Agregar nueva capa sin cambiar existentes
class AuthService:
    def validate_user(self, username, password):
        # Nueva lógica de negocio
        pass

# En main_refactored.py
auth_service = AuthService()
if auth_service.validate_user(user, pwd):
    app.run()
```

### Crear API REST
```python
# Usar service en FastAPI
from fastapi import FastAPI
from service_product import ProductService

app = FastAPI()

@app.get("/api/products")
def get_products(service: ProductService):
    return service.list_all_products()
```

## Testing

### Antes (Difícil de testear)
```python
# No se puede mockear
def test_find_product():
    functions.products = [...]  # Modificar variable global
    result = functions.find_by_id('001')
    assert result  # Frágil
```

### Después (Fácil de testear)
```python
# Con inyección de dependencias
def test_find_product():
    mock_repo = Mock()
    service = ProductService(mock_repo)
    
    service.get_product('001')
    mock_repo.get_by_id.assert_called_once_with('001')
```

## Recomendaciones

1. **Comienza gradualmente**: No necesitas cambiar todo de una vez
2. **Migra datos**: Puedes importar datos del anterior al nuevo
3. **Tests**: Agrega tests a medida que refactorizas
4. **Documentación**: Documenta API del servicio
5. **Logging**: Agrega logs para debugging

## Próximos Pasos

1. ✅ Refactorizar con arquitectura (YA HECHO)
2. ⬜ Agregar tests unitarios
3. ⬜ Crear API REST con FastAPI
4. ⬜ Agregar autenticación
5. ⬜ Migrar a PostgreSQL
6. ⬜ Dockerizar la aplicación

## Conclusión

Con esta arquitectura:
- 🎯 Código más **profesional**
- 📈 Más **escalable**
- 🧪 Más **testeable**
- 🔄 Más **mantenible**
- 📚 Mejor **documentado**

¿Preguntas? Revisa los archivos comentados o la guía ARCHITECTURE.md
