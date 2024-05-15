from django.db import models
class LecturaTemperatura(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    temperatura = models.FloatField()

