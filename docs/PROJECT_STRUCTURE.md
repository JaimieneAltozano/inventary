# Estructura del Proyecto - Versión Refactorizada

## Árbol de Directorios

```
proyecto/
├── main.py                          # Original (mantener por compatibilidad)
├── main_refactored.py               # ✨ NUEVO - Versión mejorada
├── api_server.py                    # Servidor API (sin cambios)
│
├── ARCHIVOS DE CONFIGURACIÓN
├── config_db.py                     # ✨ NUEVO - Gestión de BD SQLite
├── requirements.txt                 # ✨ NUEVO - Dependencias
│
├── MODELOS DE DATOS
├── models_product.py                # ✨ NUEVO - Entidad Product
│
├── CAPA DE DATOS (Data Access)
├── repository_product.py            # ✨ NUEVO - Operaciones CRUD
│
├── CAPA DE NEGOCIO (Business Logic)
├── service_product.py               # ✨ NUEVO - Lógica de negocio
│
├── ARCHIVOS ORIGINALES
├── functions.py                     # Original (sin BD)
│
├── DOCUMENTACIÓN
├── README.md                        # ✅ Actualizado
├── ARCHITECTURE.md                  # ✨ NUEVO - Guía de arquitectura
├── REFACTORING_GUIDE.md            # ✨ NUEVO - Cómo usar la refactorización
├── API_SETUP.md                     # Guía de API
│
└── DATOS
    └── inventory.db                 # ✨ NUEVO - Base de datos SQLite (auto-creada)
```

## Comparación: Estructura Anterior vs Refactorizada

### ANTERIOR
```
proyecto/
├── main.py              (UI + Lógica + todo mezclado)
├── functions.py         (Más lógica)
├── api_server.py        (API)
└── docs/
    └── README.md
```

**Problemas:**
- Responsabilidades mezcladas
- Sin persistencia
- Difícil de testear
- Acoplamiento fuerte

### REFACTORIZADA
```
proyecto/
├── main_refactored.py       (SOLO UI)
├── service_product.py       (SOLO lógica de negocio)
├── repository_product.py    (SOLO acceso a datos)
├── models_product.py        (SOLO estructuras de datos)
├── config_db.py            (SOLO configuración de BD)
└── api_server.py            (API separada)
```

**Ventajas:**
- Responsabilidades claras
- Persistencia en SQLite
- Fácil de testear
- Bajo acoplamiento
- Arquitectura profesional

## Cuándo Usar Cada Archivo

| Necesidad | Usar | Por qué |
|-----------|------|--------|
| Aprender el proyecto | `main.py` | Es simple y directo |
| Usar en producción | `main_refactored.py` | Más robusto y profesional |
| Entender arquitectura | `ARCHITECTURE.md` | Explicación detallada |
| Migrar a nueva versión | `REFACTORING_GUIDE.md` | Paso a paso |
| Usar sin BD | `functions.py` | Para prototipos rápidos |
| Con persistencia | `repository_product.py` | Para datos reales |
| Lógica de negocio | `service_product.py` | Para reglas complejas |

## Diagrama de Capas

### Arquitectura Original
```
┌─────────────────────────────┐
│       main.py               │
│   (UI + Lógica + Datos)     │
├─────────────────────────────┤
│    functions.py             │
│   (Más UI + Lógica)         │
├─────────────────────────────┤
│    En memoria (perdible)    │
└─────────────────────────────┘
```

### Arquitectura Refactorizada
```
┌─────────────────────────────────────┐
│    Presentación (UI)                │
│    main_refactored.py               │
├─────────────────────────────────────┤
│    Negocio (Business Logic)         │
│    service_product.py               │
├─────────────────────────────────────┤
│    Datos (Data Access)              │
│    repository_product.py            │
├─────────────────────────────────────┤
│    Modelo (Data Model)              │
│    models_product.py                │
├─────────────────────────────────────┤
│    Configuración (Config)           │
│    config_db.py                     │
├─────────────────────────────────────┤
│    Base de Datos (SQLite)           │
│    inventory.db                     │
└─────────────────────────────────────┘
```

## Flujo de Datos

### Registrar un Producto

```
Usuario selecciona opción 1
         ↓
  main_refactored.py::register_products()
         ↓
  service_product.py::add_product()
    (Valida datos)
         ↓
  repository_product.py::create()
         ↓
  config_db.py::get_connection()
         ↓
  inventory.db (INSERT)
         ↓
  ✓ Producto guardado en BD
```

### Buscar un Producto

```
Usuario selecciona opción 2
         ↓
  main_refactored.py::_search_by_id()
         ↓
  service_product.py::get_product()
    (Valida que existe)
         ↓
  repository_product.py::get_by_id()
         ↓
  config_db.py::get_connection()
         ↓
  inventory.db (SELECT con índice)
         ↓
  ✓ Producto encontrado
```

### Filtrar Productos

```
Usuario selecciona opción 3
         ↓
  main_refactored.py::_filter_by_status()
         ↓
  service_product.py::get_products_by_status()
    (Valida parámetros)
         ↓
  repository_product.py::filter_by_statement()
         ↓
  config_db.py::get_connection()
         ↓
  inventory.db (SELECT WHERE status = ?)
         ↓
  ✓ Productos filtrados
```

## Base de Datos (SQLite)

### Ubicación del archivo
```
c:\Users\violy\OneDrive\Desktop\M5\prueba\inventory.db
```

### Tabla productos
```
┌──────────────────────────────────────────────────────┐
│                  products (tabla)                    │
├──────────┬──────────┬───────────┬──────────┬─────────┤
│ id (PK)  │ name     │ price     │ stock    │ state   │
├──────────┼──────────┼───────────┼──────────┼─────────┤
│ DELL-001 │ Laptop   │ 1299.99   │ 15       │ active  │
│ LOG-001  │ Mouse    │ 99.99     │ 45       │ active  │
│ KEY-001  │ Keyboard │ 159.99    │ 32       │ active  │
└──────────┴──────────┴───────────┴──────────┴─────────┘
```

### Beneficios de SQLite vs Memoria

| Característica | En Memoria | SQLite |
|---|---|---|
| Persistencia | ❌ Se pierden datos | ✅ Datos permanentes |
| Transacciones | ❌ No | ✅ ACID completo |
| Índices | ❌ Búsqueda O(n) | ✅ Búsqueda O(log n) |
| Constraints | ❌ No | ✅ Integridad de datos |
| Escalabilidad | ⚠️ Limitada | ✅ Millones de registros |
| Backup | ❌ Complejo | ✅ Solo copiar archivo |
| Concurrencia | ❌ Limitada | ✅ Bloqueos inteligentes |

## Dependencias del Proyecto

### Versión Original
```
(Sin dependencias externas)
```

### Versión Refactorizada
```
flask==2.3.3          # Para API server
requests==2.31.0      # Para cliente HTTP
sqlite3               # Incluido en Python ✅
```

## Cómo Empezar

### Opción 1: Rápido y Simple
```bash
python main.py
# Usa versión original
# Datos en memoria (se pierden)
```

### Opción 2: Profesional y Escalable
```bash
pip install -r requirements.txt
python main_refactored.py
# Usa SQLite
# Datos persistentes
# Arquitectura profesional
```

### Opción 3: Con API completa
```bash
pip install -r requirements.txt

# Terminal 1: API server
python api_server.py

# Terminal 2: Aplicación
python main_refactored.py
```

## Migración de Datos

Para migrar datos del `main.py` original al `main_refactored.py`:

### Opción A: Importar desde API
1. Registra productos en `main.py`
2. Exporta a archivo JSON
3. Crea endpoint en API que devuelva esos datos
4. Usa opción 5 en `main_refactored.py` para importar

### Opción B: Importar directamente
```python
# Script auxiliar
from service_product import ProductService
from config_db import DatabaseManager
from repository_product import ProductRepository

db = DatabaseManager()
repo = ProductRepository(db)
service = ProductService(repo)

# Importar desde función.products
for product in functions.products:
    service.add_product(
        product['ID'],
        product['Name'],
        product['Prize'],
        product['Stock'],
        product['Statement']
    )
```

## Próximos Pasos de Mejora

1. **Tests Unitarios**
   ```python
   # tests/test_service.py
   def test_add_product_valid():
       service = ProductService(mock_repo)
       result = service.add_product('1', 'Test', 10, 5, 'active')
       assert result.id == '1'
   ```

2. **API REST Completa**
   ```python
   # Reemplazar api_server.py con FastAPI
   from fastapi import FastAPI
   app = FastAPI()
   
   @app.post("/products")
   def create(product: ProductSchema):
       return service.add_product(...)
   ```

3. **Autenticación**
   ```python
   # Agregar JWT, OAuth2, etc.
   @app.get("/products", dependencies=[Depends(verify_token)])
   def get_products():
       return service.list_all_products()
   ```

4. **Documentación Swagger**
   ```python
   # FastAPI genera automáticamente
   # http://localhost:8000/docs
   ```

## Referencias

- [ARCHITECTURE.md](ARCHITECTURE.md) - Explicación detallada de la arquitectura
- [REFACTORING_GUIDE.md](REFACTORING_GUIDE.md) - Guía de uso de la nueva versión
- [README.md](README.md) - Información general del proyecto
- [API_SETUP.md](API_SETUP.md) - Cómo usar el servidor API
