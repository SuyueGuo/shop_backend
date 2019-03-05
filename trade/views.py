from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import Sum, Count, Avg

from trade.models import Trade
from cloth.models import Cloth
from user.models import User

from datetime import datetime, timedelta, timezone
import json

'''
cloth user cloth_number total_price time
create(cloth, user, color, size) # 创建交易
query_id(id) # 询问id号交易
query_sum_by_user(user) # 询问关于user交易的数量和交易额
query_sum_by_cloth(cloth) # 询问关于cloth交易的数量和交易额
query_user_by_time(user, i) # 询问user最近第i个交易的信息
query_cloth_by_time(cloth, i) # 询问cloth最近第i个交易的信息
'''

def get_trade_info(trade):
    trade_info = dict(id = trade.id,
                      cloth = str(trade.cloth),
                      user = str(trade.user),
                      cloth_number = trade.cloth_number,
                      total_price = str(trade.total_price),
                      color = str(trade.color),
                      size = str(trade.size),
                      time = trade.time.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S"), )
    return json.dumps(trade_info, ensure_ascii = False)

def trade(request):
    try:
        query_type = request.GET['type']
        if query_type == 'create':
            cloth_name = request.GET['cloth']
            user_name = request.GET['user']
            color = request.GET['color']
            size = request.GET['size']
            
            cloth = Cloth.objects.get(cloth_name)
            user = User.objects.get(user_name)
            
            cloth_number = int(request.GET['cloth_number'])
            total_price = request.GET['total_price']
            
            trade = Trade.objects.create(cloth = cloth,
                                         user = user,
                                         cloth_number = cloth_number,
                                         total_price = total_price,
                                         color = color,
                                         size = size)
            
            return HttpResponse(json.dumps(dict(traid_id = traid.id, request_info = "CREATED!"), ensure_ascii = False))
            
        elif query_type == 'query_id':
            trade_id = request.GET['id']
            trade = Trade.objects.get(id = trade_id)
            
            return HttpResponse(get_trade_info(trade))
            
        elif query_type == 'query_sum_by_user':
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            
            trade_info = Trade.objects.filter(user = user).values('user__name').annotate(count = Count('user'), sum_price = Sum('total_price'))
            tmp = list(trade_info)
            if tmp:
                trade_info = dict(user = tmp[0]['user__name'],
                                  count = tmp[0]['count'],
                                  sum_price = "%.2f" % float(tmp[0]['sum_price']))
            else:
                trade_info = dict(user = user_name, count = 0, sum_price = '0.00')
            
            return HttpResponse(json.dumps(trade_info, ensure_ascii = False))
            
        elif query_type == 'query_sum_by_cloth':
            cloth_name = request.GET['cloth']
            cloth = Cloth.objects.get(name = cloth_name)
            
            trade_info = Trade.objects.filter(cloth = cloth).values('cloth__name').annotate(count = Count('cloth'), sum_price = Sum('total_price'))
            tmp = list(trade_info)
            if tmp:
                trade_info = dict(cloth = tmp[0]['cloth__name'],
                                  count = tmp[0]['count'],
                                  sum_price = "%.2f" % float(tmp[0]['sum_price']))
            else:
                trade_info = dict(cloth = cloth_name, count = 0, sum_price = '0.00')
            
            return HttpResponse(json.dumps(trade_info, ensure_ascii = False))
            
        elif query_type == 'query_user_by_time':
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            i = int(request.GET['i'])
            
            trade = Trade.objects.filter(user = user).order_by('-time')[i - 1]
            
            return HttpResponse(get_trade_info(trade))
            
        elif query_type == 'query_cloth_by_time':
            cloth_name = request.GET['cloth']
            cloth = Cloth.objects.get(name = cloth_name)
            i = int(request.GET['i'])
            
            trade = Trade.objects.filter(cloth = cloth).order_by('-time')[i - 1]
            
            return HttpResponse(get_trade_info(trade))
            
        else:
            return HttpResponse(json.dumps(dict(request_info = 'WRONG TYPE!'), ensure_ascii = False))
        
    except Exception as e:
        return HttpResponse(json.dumps(dict(request_info = str(e) + '\n' + 'ERROR!'), ensure_ascii = False))

