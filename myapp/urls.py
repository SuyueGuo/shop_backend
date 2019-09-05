"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from user import views as user_views
from cloth import views as cloth_views
from trade import views as trade_views
from zhongchou import views as zhongchou_views
from designer import views as designer_views
from score import views as score_views
from recommend import views as recommend_views
from comment import views as comment_views
from emailcheck import views as emailcheck_views

urlpatterns = [
    path('user/', user_views.user, name = 'user'),
    path('cloth/', cloth_views.cloth, name = 'cloth'),
    path('trade/', trade_views.trade, name = 'trade'),
    path('zhongchou/', zhongchou_views.zhongchou, name = 'zhongchou'),
    path('designer/', designer_views.designer, name = 'designer'),
    path('score/', score_views.score, name = 'score'),
    path('recommend/', recommend_views.recommend, name = 'recommend'),
    path('comment/', comment_views.comment, name = 'comment'),
    path('emailcheck/', emailcheck_views.emailcheck, name = 'emailcheck'),
    path('admin/', admin.site.urls),
]
