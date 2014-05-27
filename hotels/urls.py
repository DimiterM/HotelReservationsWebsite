from django.conf.urls import patterns, url

from hotels import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<page_num>\d+)/$', views.index, name='index'),  
    url(r'^login/$', views.login, name='login'),
    url(r'^hotel-info/(?P<hotel_id>\d+)/$', views.hotel_info, name='hotel-info'),
    url(r'^reserve/(?P<hotel_id>\d+)/$', views.reserve, name='reserve'),
)
