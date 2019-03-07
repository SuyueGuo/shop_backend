from django.db import models

class Comment(models.Model):
    user = models.ForeignKey('user.User', on_delete = models.CASCADE, )
    cloth = models.ForeignKey('cloth.Cloth', on_delete = models.CASCADE, )
    content = models.CharField(max_length = 1000)
    create_time = models.DateTimeField(auto_now = False, auto_now_add = True)
