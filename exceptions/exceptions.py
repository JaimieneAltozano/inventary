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