from django.db import models

class Cloth(models.Model):
    name = models.CharField(max_length = 30, unique = True)
    intro = models.CharField(max_length = 1000)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    disc_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    designer = models.ForeignKey('designer.Designer', on_delete = models.CASCADE, )
    publish_time = models.DateTimeField(auto_now = False, auto_now_add = True)
    TYPE_CHOICE = {('UG', '上衣'), ('PT', '裤子'), ('CT', '帽子'), ('SH', "鞋子"), ('OT', '其它')}
    cloth_type = models.CharField(max_length = 5, choices = TYPE_CHOICE, default='null')
    cloth_id = models.CharField(max_length = 10, default = '0')
    number = models.IntegerField(default=0)
    
    def __str__(self):
        return self.cloth_id
    
'''
id = type + num
'''