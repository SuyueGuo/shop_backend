from django.shortcuts import render
from django.http import HttpResponse

from zhongchou.models import ZhongChou, ZhongChouDetail
from cloth.models import Cloth
from user.models import User
from trade.models import Trade

from datetime import datetime, timedelta, timezone
import json

limit_of_zhongchou = 100 # 众筹上限

'''
user cloth number finished
create(cloth) # 创建众筹，返回id
add(id, user, number) # 众筹数+number，并检查finished
pay(id, uesr) # user支付了第id个众筹的费用
state(id) # 返回finished
info(id, user) # 返回第id个众筹里，user的相关信息
query_number_by_user(user) # 询问关于user众筹的数量
query_number_by_cloth(cloth) # 询问关于cloth众筹的数量
query_user_by_time(sort_by, user, i) # 询问user最近第i个众筹的编号（按创立或最后申请的时间, create/last）
query_cloth_by_time(sort_by, cloth, i) # 询问cloth最近第i个众筹的编号（按创立或最后申请的时间, create/last）
'''

def all_paid_zhongchou(zhongchou):
    pass


def get_zhongchou_info(zhongchou):
    zhongchou_info = dict(id = zhongchou.id,
                          cloth = str(zhongchou.cloth),
                          total_number = zhongchou.total_number,
                          finished = zhongchou.finished,
                          start_time = zhongchou.start_time.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S"),
                          last_time = zhongchou.last_time.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S"), )
    return json.dumps(zhongchou_info, ensure_ascii = True)


def zhongchou(request):
    try:
        query_type = request.GET['type']
        
        if query_type == 'create':
            cloth_name = request.GET['cloth']
            cloth = Cloth.objects.get(name = cloth_name)
            
            zhongchou = ZhongChou.objects.create(cloth = cloth, total_number = 0, paid_number = 0, finished = False, all_paid = False)
            
            return HttpResponse(json.dumps(dict(zhongchou_id = zhongchou.id, request_info = "CREATED!"), ensure_ascii = False))
            
        elif query_type == 'add':
            zhongchou_id = int(request.GET['id'])
            zhongchou = ZhongChou.objects.get(id = zhongchou_id)
            
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            
            number = int(request.GET['number'])
            
            if zhongchou.finished == True:
                return HttpResponse(json.dumps(dict(request_info = "FULL!"), ensure_ascii = False))
            
            ZhongChouDetail.objects.create(user = user, zhongchou = zhongchou, number = number, paid = False)
            zhongchou.total_number += number
            
            if zhongchou.total_number >= limit_of_zhongchou:
                zhongchou.finished = True
            
            zhongchou.save()
            
            return HttpResponse(json.dumps(dict(request_info = "ADDED!"), ensure_ascii = False))
            
        elif query_type == 'pay':
            zhongchou_id = int(request.GET['id'])
            zhongchou = ZhongChou.objects.get(id = zhongchou_id)
            
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            
            zhongchou_detail = ZhongChouDetail.objects.get(zhongchou = zhongchou, user = user)
            
            if zhongchou.finished == False:
                return HttpResponse(json.dumps(dict(request_info = "NOT FINISHED!"), ensure_ascii = False))
            
            if zhongchou_detail.paid == True:
                return HttpResponse(json.dumps(dict(request_info = "HAVE PAID!"), ensure_ascii = False))
            zhongchou_detail.paid = True
            zhongchou_detail.save()
            
            zhongchou.paid_number += zhongchou_detail.number
            
            if zhongchou.paid_number >= zhongchou.total_number:
                zhongchou.all_paid = True
                all_paid_zhongchou(zhongchou)
            
            zhongchou.save()
            
            return HttpResponse(json.dumps(dict(request_info = "OK!"), ensure_ascii = False))
            
        elif query_type == 'state_of_zhongchou':
            zhongchou_id = int(request.GET['id'])
            zhongchou = ZhongChou.objects.get(id = zhongchou_id)
            
            zhongchou_info = dict(finished = str(zhongchou.finished),
                                  all_paid = str(zhongchou.all_paid), )
            
            return HttpResponse(json.dumps(zhongchou_info, ensure_ascii = False))
        
        elif query_type == 'get_info':
            zhongchou_id = int(request.GET['id'])
            zhongchou = ZhongChou.objects.get(id = zhongchou_id)
            
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            
            cloth = zhongchou.cloth
            
            zhongchou_detail = ZhongChouDetail.objects.get(zhongchou = zhongchou, user = user)
            
            zhongchou_info = dict(cloth = str(cloth),
                                  number = zhongchou_detail.number,
                                  paid = zhongchou_detail.paid, )
            
            return HttpResponse(json.dumps(zhongchou_info))
            
        elif query_type == 'query_number_by_user':
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            
            return HttpResponse(json.dumps(dict(number = len(user.zhongchou_set.all())), ensure_ascii = False))
            
        elif query_type == 'query_number_by_cloth':
            cloth_name = request.GET['cloth']
            cloth = Cloth.objects.get(name = cloth_name)
            
            return HttpResponse(json.dumps(dict(number = len(cloth.zhongchou_set.all())), ensure_ascii = False))
            
        elif query_type == 'query_user_by_time':
            sort_by = '-' + request.GET['sort_by']
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            i = int(request.GET['i'])
            
            zhongchou = user.zhongchou_set.all().order_by(sort_by)[i - 1]
            
            return HttpResponse(get_zhongchou_info(zhongchou))
            
        elif query_type == 'query_cloth_by_time':
            sort_by = '-' + request.GET['sort_by']
            cloth_name = request.GET['cloth']
            cloth = Cloth.objects.get(name = cloth_name)
            i = int(request.GET['i'])
            
            zhongchou = cloth.zhongchou_set.all().order_by(sort_by)[i - 1]
            
            return HttpResponse(get_zhongchou_info(zhongchou))
            
        else:
            return HttpResponse(json.dumps(dict(request_info = 'WRONG TYPE!'), ensure_ascii = False))
        
    except Exception as e:
        return HttpResponse(json.dumps(dict(request_info = str(e) + '\n' + 'ERROR!'), ensure_ascii = False))
        
