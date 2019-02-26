from django.db import models

class Cloth(models.Model):
    name = models.CharField(max_length = 30)
    intro = models.CharField(max_length = 1000)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    disc_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    designer = models.ForeignKey('designer.Designer', on_delete = models.CASCADE, )
    publish_time = models.DateTimeField(auto_now = False, auto_now_add = True)
    
    def __str__(self):
        return self.name
    
