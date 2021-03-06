from django.conf.urls import patterns, url

from hotels import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<page_num>\d+)/$', views.index, name='index'),  
    url(r'^login/$', views.login_view, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/hotels/'}),
    url(r'^hotel-info/(?P<hotel_id>\d+)/$', views.hotel_info, name='hotel-info'),
    url(r'^reserve/(?P<hotel_id>\d+)/$', views.reserve, name='reserve'),
)
