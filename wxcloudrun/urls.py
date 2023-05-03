"""wxcloudrun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from wxcloudrun import views
from django.conf.urls import url


urlpatterns = (
    # 计数器接口
    # url(r'^^api/count(/)?$', views.counter),

    # 获取主页
    # url(r'(/)?$', views.index),

    # 获取主页
    url(r'api/demo?$', views.demo),
    url(r'api/demo2?$', views.my_view),
    url(r'api/bili_summary$', views.bili_summary),
)
