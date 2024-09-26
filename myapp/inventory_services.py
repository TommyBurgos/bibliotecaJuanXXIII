from django.core.exceptions import ValidationError
from .models import Libro, Inventario, HistorialInventario

def registrar_historial(libro, cantidad_cambio, usuario, accion):
    HistorialInventario.objects.create(
        libro=libro,
        cantidad_cambio=cantidad_cambio,
        usuario=usuario,
        accion=accion
    )

def prestar_libro(libro, usuario):
    inventario = Inventario.objects.get(libro=libro)
    
    if inventario.cantActual > 0:
        inventario.cantActual -= 1
        inventario.save()
        registrar_historial(libro, -1, usuario, 'prestamo')
    else:
        raise ValidationError("No hay libros disponibles para prestar.")

def devolver_libro(libro, usuario):
    inventario = Inventario.objects.get(libro=libro)
    inventario.cantActual += 1
    inventario.save()
    registrar_historial(libro, 1, usuario, 'devolucion')
