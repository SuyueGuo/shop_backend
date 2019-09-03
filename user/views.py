from django.shortcuts import render
from django.http import HttpResponse

from user.models import User
import json

def get_user_info(user):
    return json.dumps(dict(address = user.address,
                           telephone = str(user.telephone),
                           head_portrait = user.head_portrait,
                           user_id = user.user_id,
                           name = user.name,))

def user(request):
    try:
        query_type = request.GET['type']
        if query_type == 'create':
            name = request.GET['name']
            address = request.GET['address']
            telephone = int(request.GET['telephone'])
            head_portrait = request.GET['head_portrait']

            user_id = str(telephone)
            
            arr = User.objects.filter(user_id = user_id)
            if len(arr) == 0:
                User.objects.create(user_id = user_id,
                                    name = name,
                                    address = address,
                                    telephone = telephone,
                                    head_portrait = head_portrait)
                return HttpResponse(json.dumps(dict(request_info = 'CREATED!'), ensure_ascii = False))
            elif len(arr) == 1:
                return HttpResponse(json.dumps(dict(request_info = 'EXISTED!'), ensure_ascii = False))
            else:
                return HttpResponse(json.dumps(dict(request_info = 'ERROR!'), ensure_ascii = False))
            
        elif query_type == 'modify':
            name = request.GET['name']
            address = request.GET['address']
            telephone = int(request.GET['telephone'])
            head_portrait = request.GET['head_portrait']

            user_id = str(telephone)
            
            arr = User.objects.filter(user_id = user_id)
            if len(arr) == 1:
                arr[0].name = name
                arr[0].address = address
                arr[0].telephone = telephone
                arr[0].head_portrait = head_portrait
                arr[0].save()
                return HttpResponse(json.dumps(dict(request_info = 'UPDATED!'), ensure_ascii = False))
            else:
                return HttpResponse(json.dumps(dict(request_info = 'ERROR!'), ensure_ascii = False))
            
        elif query_type == 'get_info_by_name':
            name = request.GET['name']
            arr = User.objects.filter(name = name)
            if len(arr) == 1:
                return HttpResponse(get_user_info(arr[0]))
            else:
                return HttpResponse(json.dumps(dict(request_info = 'ERROR!'), ensure_ascii = False))
            
        elif query_type == 'get_info_by_id':
            user_id = int(request.GET['id'])
            arr = User.objects.filter(user_id = user_id)
            if len(arr) == 1:
                return HttpResponse(get_user_info(arr[0]))
            else:
                return HttpResponse(json.dumps(dict(request_info = 'ERROR!'), ensure_ascii = False))
            
        else:
            return HttpResponse(json.dumps(dict(request_info = 'WRONG TYPE!'), ensure_ascii = False))
        
    except Exception as e:
        return HttpResponse(json.dumps(dict(request_info = str(e) + '\n' + 'ERROR!'), ensure_ascii = False))

