from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.
class Genero(models.Model):
    nombre=models.CharField(max_length=150)
    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.TextField(max_length=150)
    fechaNacimiento=models.DateField()
    fechaFallecimiento = models.DateField(null=True, blank=True)
    pequenaBiografia=models.TextField(max_length=500)
    foto = models.ImageField(upload_to='autores/', default='autores/defecto.png')

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    nombre = models.TextField(max_length=300)    
    fechaPublicacion= models.DateField()
    descripcion=models.TextField(max_length=500, default="Descripción no disponible")
    generos = models.ManyToManyField(Genero, related_name='libros')
    imgPortada = models.ImageField(upload_to='libros/', default='libros/defectoLibro.png')
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True, blank=True, related_name='libros')
    


    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantActual = models.IntegerField()
    cantMin = models.IntegerField()
    cantMax = models.IntegerField()
    ubicacion = models.CharField(max_length=255, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.libro.nombre} - {self.cantActual} disponibles"
    
    def clean(self):
        if self.cantMin >= self.cantMax:
            raise ValidationError("La cantidad mínima debe ser menor que la cantidad máxima.")
        if not (self.cantMin <= self.cantActual <= self.cantMax):
            raise ValidationError("La cantidad actual debe estar entre la cantidad mínima y máxima.")

class LibroDigital(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    imgPortada = models.ImageField(upload_to='libros/digital/portadas', default='libros/defectoLibro.png')
    archivo_pdf = models.FileField(upload_to='libros/digital/pdf/')
    fecha_publicacion = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titulo

    # Opción para obtener la URL del archivo PDF si es necesario
    def obtener_pdf_url(self):
        if self.archivo_pdf:
            return self.archivo_pdf.url
        return None

class HistorialInventario(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad_cambio = models.IntegerField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accion = models.CharField(max_length=20)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

#SOLICITUDES
class SolicitudLibro(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]
    
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solicitudes')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='solicitudes')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)  # Para que el administrador agregue comentarios

    def __str__(self):
        return f"Solicitud de {self.estudiante.username} para {self.libro.nombre}"