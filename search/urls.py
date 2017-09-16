from django.conf.urls import url

from . import views

app_name = 'search'

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
    url(r'output/$', views.output, name = 'output'),
    url(r'^detail/(?P<people_id>[0-9]+)/$', views.detail, name = 'detail'),
]
