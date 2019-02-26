from django.db import models

class Trade(models.Model):
    cloth = models.ForeignKey('cloth.Cloth', on_delete = models.CASCADE, )
    user = models.ForeignKey('user.User', on_delete = models.CASCADE, )
    cloth_number = models.IntegerField()
    total_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    time = models.DateTimeField(auto_now = False, auto_now_add = True)
    
    
'''
cloth user cloth_number total_price time
create(cloth, user) # 创建交易
query_id(id) # 询问id号交易
query_sum_by_user(user) # 询问关于user交易的数量和交易额
query_sum_by_cloth(cloth) # 询问关于cloth交易的数量和交易额
query_user_by_time(user, i) # 询问user最近第i个交易的信息
query_cloth_by_time(cloth, i) # 询问cloth最近第i个交易的信息
'''
