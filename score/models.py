from django.db import models

class Score(models.Model):
    user = models.ForeignKey('user.User', on_delete = models.CASCADE, )
    cloth = models.ForeignKey('cloth.Cloth', on_delete = models.CASCADE, )
    score = models.IntegerField()
