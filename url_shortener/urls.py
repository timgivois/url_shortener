from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^transform$', views.transform, name='transform'),
    url(r'^view$', views.view, name='view'),
    url(r'^.*$', views.redirect_short_url, name='index'),
]
