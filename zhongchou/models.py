from django.db import models

# user cloth number finished
class ZhongChou(models.Model):
    user = models.ManyToManyField('user.User', through = 'ZhongChouDetail')
    cloth = models.ForeignKey('cloth.Cloth', on_delete = models.CASCADE, )
    total_number = models.IntegerField()
    paid_number = models.IntegerField()
    finished = models.BooleanField()
    all_paid = models.BooleanField()
    start_time = models.DateTimeField(auto_now = False, auto_now_add = True)
    last_time = models.DateTimeField(auto_now = True, auto_now_add = False)

class ZhongChouDetail(models.Model):
    user = models.ForeignKey('user.User', on_delete = models.CASCADE, )
    zhongchou = models.ForeignKey('ZhongChou', on_delete = models.CASCADE, )
    number = models.IntegerField()
    paid = models.BooleanField()
