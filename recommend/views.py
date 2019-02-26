from django.shortcuts import render
from django.http import HttpResponse

from score.models import Score
from user.models import User
from cloth.models import Cloth
from rbm.models import RBM

import numpy as np
import json

'''
推荐：   
recommend
train() # 训练模型
get_recommend(user, begin, end) # 获取推荐给user中前begin到end名的商品名和概率
'''

score_table = [0.0, 0.0, 0.2, 0.5, 0.8, 1.0]

def get_train_data():
    train_data = np.zeros((User.objects.latest('id').id, Cloth.objects.latest('id').id))
    for score_info in Score.objects.all():
        user = score_info.user
        cloth = score_info.cloth
        score = score_info.score
        train_data[user.id - 1, cloth.id - 1] = score_table[score]
    return train_data

def recommend(request):
    try:
        query_type = request.GET['type']
        
        if query_type == 'train':
            train_data = get_train_data()
            rbm = RBM(n_visible = train_data.shape[1])
            rbm.fit(train_data)
            rbm.save('data')
            return HttpResponse(json.dumps(dict(request_info = 'OK'), ensure_ascii = False))
            
        elif query_type == 'get_recommend':
            user_name = request.GET['user']
            user = User.objects.get(name = user_name)
            
            begin = int(request.GET['begin'])
            end = int(request.GET['end'])
            
            train_data = get_train_data()
            rbm = RBM(n_visible = train_data.shape[1])
            rbm.load('data')
            
            prob_arr = rbm.predict(train_data[user.id - 1])
            total_result = [(float(x), i) for i, x in enumerate(prob_arr)]
            result = sorted(total_result, reverse = True)[begin - 1 : end]
            result = list(map(lambda t : (t[0], t[1] + 1), result))
            
            return HttpResponse(json.dumps(result, ensure_ascii = False))
            
        else:
            return HttpResponse(json.dumps(dict(request_info = 'WRONG TYPE!'), ensure_ascii = False))
        
    except Exception as e:
        return HttpResponse(json.dumps(dict(request_info = str(e) + '\n' + 'ERROR!'), ensure_ascii = False))

