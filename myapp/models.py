from django.db import models

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
        
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True, blank=True, related_name='libros')

    def __str__(self):
        return self.nombre

