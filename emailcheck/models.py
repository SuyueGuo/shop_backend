from django.db import models

# Create your models here.
class EmailCheck(models.Model):
    code = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    TYPE_CHOICE = {('RE', '用户注册'), ('FG', '修改密码')}
    send_type = models.CharField(max_length=10, choices=TYPE_CHOICE)