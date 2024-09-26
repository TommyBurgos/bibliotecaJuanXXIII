# myapp/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model  # Importa el modelo de usuario
from .models import Inventario, HistorialInventario

@receiver(post_save, sender=Inventario)
def registro_cambio_inventario(sender, instance, created, **kwargs):
    if created:
        accion = 'Creado'
    else:
        accion = 'Actualizado'
    HistorialInventario.objects.create(
        libro=instance.libro,
        cantidad_cambio=instance.cantActual,
        usuario=get_user_model().objects.get(pk=1),  # Cambia según sea necesario
        accion=accion
    )

@receiver(post_delete, sender=Inventario)
def registro_borrado_inventario(sender, instance, **kwargs):
    HistorialInventario.objects.create(
        libro=instance.libro,
        cantidad_cambio=instance.cantActual,
        usuario=get_user_model().objects.get(pk=1),  # Cambia según sea necesario
        accion='Eliminado'
    )
