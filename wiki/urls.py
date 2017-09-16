from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^search/', include('search.urls')),
    url(r'^admin/', admin.site.urls),
]
