from django.shortcuts import render
from django.http import HttpResponse

from cloth.models import Cloth
from designer.models import Designer

from datetime import datetime, timedelta, timezone
import json

def cloth(request):
    try:
        query_type = request.GET['type']
        if query_type == 'create':
            name = request.GET['name']
            intro = request.GET['intro']
            price = request.GET['price']
            disc_price = request.GET['disc_price']
            cloth_type = request.GET['cloth_type']
            number = request.GET['number']

            type_num = "%8d" % len(Cloth.objects.filter(cloth_type=cloth_type))
            cloth_id = cloth_type + type_num

            designer_name = request.GET['designer']
            designer = Designer.objects.get(name=designer_name)

            if len(Cloth.objects.filter(cloth_id=cloth_id)):
                return HttpResponse(json.dumps(dict(request_info='EXISTED!'), ensure_ascii=False))

            Cloth.objects.create(name=name,
                                 intro=intro,
                                 price=price,
                                 disc_price=disc_price,
                                 designer=designer,
                                 cloth_id=cloth_id,
                                 cloth_type=cloth_type,
                                 number=number)

            return HttpResponse(json.dumps(dict(request_info='CREATED!'), ensure_ascii=False))

        elif query_type == 'modify':
            name = request.GET['name']
            intro = request.GET['intro']
            price = request.GET['price']
            disc_price = request.GET['disc_price']
            number = request.GET['number']

            designer_name = request.GET['designer']
            designer = Designer.objects.get(name=designer_name)

            cloth = Cloth.objects.get(name=name)
            cloth.intro = intro
            cloth.price = price
            cloth.disc_price = disc_price
            cloth.designer = designer
            cloth.number = number
            cloth.save()

            return HttpResponse(json.dumps(dict(request_info='UPDATED!'), ensure_ascii=False))

        elif query_type == 'get_info_by_name':
            name = request.GET['name']
            cloth = Cloth.objects.get(name=name)

            cloth_info = dict(intro=cloth.intro,
                              price="%.2f" % float(cloth.price),
                              disc_price="%.2f" % float(cloth.disc_price),
                              designer=str(cloth.designer),
                              publish_time=cloth.publish_time.astimezone(timezone(timedelta(hours=8))).strftime(
                                  "%Y-%m-%d %H:%M:%S"), )

            return HttpResponse(json.dumps(cloth_info, ensure_ascii=False))

        elif query_type == 'get_info_by_id':
            cloth_id = int(request.GET['id'])
            cloth = Cloth.objects.get(cloth_id=cloth_id)

            cloth_info = dict(name=cloth.name,
                              intro=cloth.intro,
                              price="%.2f" % float(cloth.price),
                              disc_price="%.2f" % float(cloth.disc_price),
                              designer=str(cloth.designer),
                              publish_time=cloth.publish_time.astimezone(timezone(timedelta(hours=8))).strftime(
                                  "%Y-%m-%d %H:%M:%S"), )

            return HttpResponse(json.dumps(cloth_info, ensure_ascii=False))

        elif query_type == 'get_number':
            return HttpResponse(json.dumps(dict(cloth_number=str(len(Cloth.objects.filter()))), ensure_ascii=False))

        else:
            return HttpResponse(json.dumps(dict(request_info='WRONG TYPE!'), ensure_ascii=False))

    except Exception as e:
        return HttpResponse(json.dumps(dict(request_info=str(e) + '\n' + 'ERROR!'), ensure_ascii=False))
