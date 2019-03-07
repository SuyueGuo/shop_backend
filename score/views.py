from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import Sum, Count, Avg

from score.models import Score
from user.models import User
from cloth.models import Cloth

import json

def score(request):
    try:
        query_type = request.GET['type']
        
        if query_type == 'modify':
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            
            cloth_name = request.GET['cloth']
            cloth = Cloth.objects.get(name = cloth_name)
            
            score = int(request.GET['score'])
            
            arr = Score.objects.filter(user = user, cloth = cloth)
            
            if len(arr) == 0:
                Score.objects.create(user = user, cloth = cloth, score = score)
                return HttpResponse(json.dumps(dict(request_info = 'CREATED!'), ensure_ascii = False))
            elif len(arr) == 1:
                arr[0].score = score
                arr[0].save()
                return HttpResponse(json.dumps(dict(request_info = 'UPDATED!'), ensure_ascii = False))
            else:
                return HttpResponse(json.dumps(dict(request_info = 'ERROR!'), ensure_ascii = False))
            
        elif query_type == 'get_user_score':
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            
            cloth_name = request.GET['cloth']
            cloth = Cloth.objects.get(name = cloth_name)
            
            result = dict()
            arr = Score.objects.filter(user = user, cloth = cloth)
            
            if len(arr) == 0:
                result['score'] = 0
            elif len(arr) == 1:
                result['score'] = arr[0].score
            else:
                return HttpResponse(json.dumps(dict(request_info = 'ERROR!'), ensure_ascii = False))
            
            return HttpResponse(json.dumps(result, ensure_ascii = False))
            
        elif query_type == 'get_avg_score':
            cloth_name = request.GET['cloth']
            cloth = Cloth.objects.get(name = cloth_name)
            
            result = cloth.score_set.all().values('score').aggregate(avg_score = Avg('score'))
            
            return HttpResponse(json.dumps(result, ensure_ascii = False))
            
        else:
            return HttpResponse(json.dumps(dict(request_info = 'WRONG TYPE!'), ensure_ascii = False))
        
    except Exception as e:
        return HttpResponse(json.dumps(dict(request_info = str(e) + '\n' + 'ERROR!'), ensure_ascii = False))

