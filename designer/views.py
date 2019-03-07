from django.shortcuts import render
from django.http import HttpResponse

from cloth.models import Cloth
from designer.models import Designer

import json

def designer(request):
    try:
        query_type = request.GET['type']
        
        if query_type == 'create':
            name = request.GET['name']
            intro = request.GET['intro']
            
            if len(Designer.objects.filter(name = name)):
                return HttpResponse(json.dumps(dict(request_info = 'EXISTED!'), ensure_ascii = False))
            
            Designer.objects.create(name = name, intro = intro)
            
            return HttpResponse(json.dumps(dict(request_info = 'CREATED!'), ensure_ascii = False))
            
        elif query_type == 'modify':
            name = request.GET['name']
            intro = request.GET['intro']
            
            designer = Designer.objects.get(name = name)
            designer.intro = intro
            designer.save()
            
            return HttpResponse(json.dumps(dict(request_info = 'UPDATED!'), ensure_ascii = False))
            
        elif query_type == 'get_info_by_name':
            name = request.GET['name']
            designer = Designer.objects.get(name = name)
            
            cloth_number = len(designer.cloth_set.all())
            
            designer_info = dict(cloth_number = cloth_number,
                                 intro = designer.intro, )
            
            return HttpResponse(json.dumps(designer_info, ensure_ascii = False))
            
        elif query_type == 'get_info_by_id':
            designer_id = int(request.GET['id'])
            designer = Designer.objects.get(id = designer_id)
            
            cloth_number = len(designer.cloth_set.all())
            
            designer_info = dict(cloth_number = cloth_number,
                                 intro = designer.intro, )
            
            return HttpResponse(json.dumps(designer_info, ensure_ascii = False))
            
        elif query_type == 'get_cloth_by_time':
            name = request.GET['name']
            designer = Designer.objects.get(name = name)
            
            i = int(request.GET['i'])
            
            cloth = designer.cloth_set.all().order_by('-publish_time')[i - 1]
            
            return HttpResponse(json.dumps(dict(cloth_name = str(cloth)), ensure_ascii = False))
            
        else:
            return HttpResponse(json.dumps(dict(request_info = 'WRONG TYPE!'), ensure_ascii = False))
        
    except Exception as e:
        return HttpResponse(json.dumps(dict(request_info = str(e) + '\n' + 'ERROR!'), ensure_ascii = False))

