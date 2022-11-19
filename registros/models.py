from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Registro(models.Model):
        # Categoria
    CATEGORIA = (
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
    )

    # Relacion uno a muchos
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=200, null=True, choices=CATEGORIA)
    hora_actual = models.TimeField(null=True)
    fecha_creado = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return self.estado
