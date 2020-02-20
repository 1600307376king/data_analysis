"""data_analysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url, include
from data.views.views import *
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

router = routers.DefaultRouter()
# router.register(r'md', common.ModuleNameList, basename='md')
router.register(r'cpu', CpuMessageSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    #
    # path('add/', common.add_latest_info),
    path('system/', get_system_info),
    path('fs/', get_first_system_info),
    # path('index/', common.index),
    path('home/', home),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^memory/$', memory_list),
    path('memory/<int:pk>/', memory_control),
    url(r'^ssd/$', SolidStateDiskList.as_view()),
    url(r'^ssd/(?P<pk>[0-9]+)/$', SolidStateControl.as_view()),
    url(r'^net/$', NetList.as_view()),
    url(r'^net/(?P<pk>[0-9]+)/$', NetControl.as_view()),
    url(r'^net2/$', NetToList.as_view()),
    url(r'^net2/(?P<pk>[0-9]+)/$', NetToControl.as_view()),
    url(r'^user/$', MyUserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', MyUserControl.as_view()),
    url(r'^sys/$', SystemInfoList.as_view()),
]


# urlpatterns = format_suffix_patterns(urlpatterns)
