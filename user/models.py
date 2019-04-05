from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 30)
    address = models.CharField(max_length = 50)
    telephone = models.DecimalField(max_digits = 11, decimal_places = 0)
    head_portrait = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name
