from django.db import models
from django.contrib.auth.models import AbstractUser
from myapp.models import Libro
import datetime
# Create your models here.
class Rol(models.Model):
    nombre=models.CharField(max_length=100)
    descripcion=models.CharField(max_length=200)
    def __str__(self):
        return self.nombre

class User(AbstractUser):
    picture=models.ImageField('Imagen',upload_to='users/', max_length=255, null=True, blank=True, default='users/cr7.jpg')  
    nacimiento = models.DateField(default=datetime.date.today)
    ciudad=models.CharField(max_length=100, blank=True)
    direccion=models.CharField(max_length=300, blank=True)
    rol=models.ForeignKey(Rol,on_delete=models.CASCADE,default=2)
    libros_leidos = models.ManyToManyField(Libro, related_name='usuarios_que_leyeron', blank=True)
    
    

