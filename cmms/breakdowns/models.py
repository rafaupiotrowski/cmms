from django.db import models

# Create your models here.

class Machine(models.Model):
    name = models.TextField(blank=False, default='', unique=True)
    
    def __str__(self):
        return self.name
