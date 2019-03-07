from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import Sum, Count, Avg

from comment.models import Comment
from cloth.models import Cloth
from user.models import User

from datetime import datetime, timedelta, timezone
import json

def comment(request):
    try:
        query_type = request.GET['type']
        
        if query_type == 'create':
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            
            cloth_name = request.GET['cloth']
            cloth = Cloth.objects.get(name = cloth_name)
            
            content = request.GET['content']
            
            Comment.objects.create(user = user, cloth = cloth, content = content)
            
            return HttpResponse(json.dumps(dict(request_info = "CREATED!"), ensure_ascii = False))
            
        elif query_type == 'get_content':
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            
            cloth_name = request.GET['cloth']
            cloth = Cloth.objects.get(name = cloth_name)
            
            comment = Comment.objects.get(user = user, name = name)
            comment_info = dict(content = comment.content, )
            
            return HttpResponse(json.dumps(comment_info, ensure_ascii = False))
            
        else:
            return HttpResponse(json.dumps(dict(request_info = 'WRONG TYPE!'), ensure_ascii = False))
        
    except Exception as e:
        return HttpResponse(json.dumps(dict(request_info = str(e) + '\n' + 'ERROR!'), ensure_ascii = False))

