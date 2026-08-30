# ⚡ QUICK REFERENCE - Guía Rápida

## 🎯 ¿Qué archivo usar?

### Para Aprender
```bash
python main.py
```
- ✅ Código simple y directo
- ✅ Fácil de entender
- ✅ Perfecto para principiantes

### Para Producción ⭐ RECOMENDADO
```bash
python main_refactored.py
```
- ✅ Base de datos SQLite
- ✅ Arquitectura profesional
- ✅ Listo para empresa

### Con Servidor API
```bash
# Terminal 1: Iniciar servidor API
python api_server.py

# Terminal 2: Iniciar aplicación
python main_refactored.py
```

## 📖 ¿Qué documentación leer?

| Necesidad | Archivo |
|-----------|---------|
| Entender qué es esto | README.md |
| Aprender arquitectura | ARCHITECTURE.md |
| Migrar a versión nueva | REFACTORING_GUIDE.md |
| Ver estructura proyecto | PROJECT_STRUCTURE.md |
| Configurar API | API_SETUP.md |
| Resumen cambios | SUMMARY.md |
| Esta guía rápida | QUICK_START.md |

## 🏗️ Capas del Proyecto

### Interfaz de Usuario
📄 **main_refactored.py** - CLI interactiva

### Lógica de Negocio
📄 **service_product.py** - Reglas de negocio

### Acceso a Datos
📄 **repository_product.py** - Operaciones CRUD

### Modelo de Datos
📄 **models_product.py** - Estructura Product

### Configuración BD
📄 **config_db.py** - Conexión SQLite

## 💾 Base de Datos

### Ubicación
```
c:\Users\violy\OneDrive\Desktop\M5\prueba\inventory.db
```

### Crear tabla (Auto)
La tabla se crea automáticamente la primera vez que ejecutas la app.

### Ver contenido (Command Line)
```bash
# SQLite CLI
sqlite3 inventory.db
sqlite> SELECT * FROM products;
sqlite> .quit
```

## 🔧 Instalación Rápida

```bash
# 1. Entrar a carpeta
cd c:\Users\violy\OneDrive\Desktop\M5\prueba

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar app
python main_refactored.py
```

## 📋 Menú Principal

```
Opción 0 → Salir
Opción 1 → Registrar productos
Opción 2 → Buscar producto
Opción 3 → Filtrar productos
Opción 4 → Ver todos
Opción 5 → Importar desde API
```

## 🔍 Ejemplos Rápidos

### Buscar por ID
```
Opción 2 → Opción 1 → Ingresar "DELL-001"
```

### Buscar por nombre
```
Opción 2 → Opción 2 → Ingresar "Laptop"
```

### Filtrar por estado
```
Opción 3 → Opción 1 → Ingresar "active"
```

### Filtrar por stock
```
Opción 3 → Opción 2 → Min: 10 → Max: 50
```

### Importar API
```
Opción 5 → Presionar Enter (URL por defecto)
```

## ✅ Validaciones

| Campo | Regla | Ejemplo Válido |
|-------|-------|---|
| ID | No vacío, único | "PROD-001" |
| Name | No vacío | "Laptop Dell" |
| Price | Número >= 0 | 1299.99 |
| Stock | Entero >= 0 | 15 |
| Status | 'active' o 'inactive' | "active" |

## 🐛 Si Algo Falla

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Database locked"
- Cierra otra instancia de la app
- Reinicia

### "API connection failed"
```bash
# Iniciar servidor API primero
python api_server.py
```

### "Invalid status"
- Solo aceptan: "active" o "inactive"
- Caso insensitivo

## 📊 Cambios vs Versión Original

| Característica | Antes | Ahora |
|---|---|---|
| Almacenamiento | RAM | SQLite |
| Persistencia | No | Sí ✅ |
| Arquitectura | Simple | Modular |
| Validación | Básica | Completa |
| Testeable | No | Sí ✅ |
| Escalable | No | Sí ✅ |

## 🚀 Próximas Acciones

1. **Inmediato**: Usar `main_refactored.py`
2. **Esta semana**: Leer ARCHITECTURE.md
3. **Próximo mes**: Agregar tests
4. **Futuro**: API REST con FastAPI

## 📞 Ayuda Rápida

### Ver todo en GitHub-style
```bash
ls -la
```

### Ver estructura
```bash
tree /F
```

### Ver archivos Python
```bash
dir *.py
```

### Ver base de datos
```bash
ls -la inventory.db
```

## 🎓 Ruta de Aprendizaje

### Día 1: Entender
- Leer README.md
- Ejecutar `main_refactored.py`
- Registrar 5 productos
- Buscar y filtrar

### Día 2: Aprender Arquitectura
- Leer ARCHITECTURE.md
- Revisar `service_product.py`
- Revisar `repository_product.py`

### Día 3: Profundizar
- Leer REFACTORING_GUIDE.md
- Modificar `service_product.py`
- Agregar método nuevo

### Semana 2: Proyecto
- Crear tests (pytest)
- Agregar más features
- Documentar cambios

## 💡 Tips Profesionales

✅ Siempre valida entrada del usuario
✅ Maneja excepciones elegantemente  
✅ Usa la capa de service, nunca repository directo
✅ Documenta cambios que hagas
✅ Haz backup de `inventory.db`
✅ Prueba antes de producción

## 🎯 Objetivos Logrados ✅

- [x] SQLite integrado
- [x] Arquitectura modular
- [x] Validaciones robustas
- [x] Documentación completa
- [x] Código profesional
- [x] Fácil de mantener
- [x] Fácil de escalar
- [x] Producción-ready

## 📱 Comandos Útiles

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar app profesional
python main_refactored.py

# Ejecutar servidor API
python api_server.py

# Ver estado base de datos
sqlite3 inventory.db "SELECT COUNT(*) FROM products;"

# Backup base de datos
copy inventory.db inventory.backup.db

# Restaurar backup
copy inventory.backup.db inventory.db
```

## 🎁 Bonus: Consejos Extra

1. **Variables de entorno** - Crea `.env` para configuraciones
2. **Logging** - Agrega logs para debugging
3. **Caching** - Cachea búsquedas frecuentes
4. **Tests** - Escribe tests mientras desarrollas
5. **CI/CD** - Automatiza testing
6. **Docker** - Containeriza para deployment
7. **Documentation** - Documenta bien desde el inicio

## ✨ ¡Listo para Empezar!

```bash
cd c:\Users\violy\OneDrive\Desktop\M5\prueba
pip install -r requirements.txt
python main_refactored.py
```

**¡Disfruta tu aplicación profesional! 🚀**
