from django.db import models

class Designer(models.Model):
    name = models.CharField(max_length = 30, unique=True)
    intro = models.CharField(max_length = 1000, default='null')
    is_active = models.BooleanField(default=False)
    email = models.CharField(max_length=50, default='0', unique=True)
    password = models.CharField(max_length=50, default='0')
    telephone = models.CharField(max_length=11, default='0')
    
    def __str__(self):
        return self.name
