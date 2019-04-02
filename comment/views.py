from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import Sum, Count, Avg

from comment.models import Comment
from cloth.models import Cloth
from user.models import User

from datetime import datetime, timedelta, timezone
import json

def get_comment_info(comment):
    comment_info = dict(id = comment.id,
                        user = str(comment.user),
                        cloth = str(comment.cloth),
                        content = comment.content,
                        create_time = comment.create_time.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S"), )
    return json.dumps(comment_info, ensure_ascii = False)

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
            
        elif query_type == 'modify':
            content = request.GET['content']
            
            comment_id = int(request.GET['comment'])
            comment = Comment.objects.get(id = comment_id)
            
            comment.content = content
            comment.save()
            
            return HttpResponse(json.dumps(dict(request_info = "UPDATED!"), ensure_ascii = False))
            
        elif query_type == 'get_content_by_id':
            comment_id = int(request.GET['comment'])
            comment = Comment.objects.get(id = comment_id)
            comment_info = dict(content = comment.content, )
            
            return HttpResponse(json.dumps(comment_info, ensure_ascii = False))
            
        elif query_type == 'query_number_by_user':
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            
            return HttpResponse(json.dumps(dict(number = len(user.comment_set.all())), ensure_ascii = False))
            
        elif query_type == 'query_number_by_cloth':
            cloth_name = request.GET['cloth']
            cloth = Cloth.objects.get(name = cloth_name)
            
            return HttpResponse(json.dumps(dict(number = len(cloth.comment_set.all())), ensure_ascii = False))
            
        elif query_type == 'query_user_by_time':
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            
            i = int(request.GET['i'])
            
            comment = user.comment_set.all().order_by('-create_time')[i - 1]
            
            return HttpResponse(get_comment_info(comment))
            
        elif query_type == 'query_cloth_by_time':
            cloth_name = request.GET['cloth']
            cloth = Cloth.objects.get(name = cloth_name)
            
            i = int(request.GET['i'])
            
            comment = cloth.comment_set.all().order_by('-create_time')[i - 1]
            
            return HttpResponse(get_comment_info(comment))
            
        else:
            return HttpResponse(json.dumps(dict(request_info = 'WRONG TYPE!'), ensure_ascii = False))
        
    except Exception as e:
        return HttpResponse(json.dumps(dict(request_info = str(e) + '\n' + 'ERROR!'), ensure_ascii = False))

